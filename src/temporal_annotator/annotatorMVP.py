from __future__ import annotations
from pathlib import Path
import lxml.etree as ET


class Tei2goInlineAnnotator:
    """MVP: anota entidades TIMEX detectadas pelo TEI2GO embrulhando-as em <TIMEX3>.
    - TEI2GO puro (sem EntityRuler extra, sem normalização de value)
    - tid global (t1, t2, ...)
    - processa o texto do elemento e as tails dos filhos (não entra recursivamente nos filhos)
    """

    def __init__(self, xpath: str = ".//verse"):
        self.xpath = xpath
        self._t = 1
        self._nlp = self._load_pipeline()


    def _load_pipeline(self):
        try:
            import spacy
        except Exception as e:
            raise RuntimeError(
                "spaCy não encontrado. Instale na sua venv:\n"
                "  pip install 'spacy==3.2.6' lxml\n"
                '  pip install "en_tei2go @ https://huggingface.co/hugosousa/en_tei2go/resolve/main/en_tei2go-any-py3-none-any.whl"'
            ) from e
        try:
            return spacy.load("en_tei2go")  # TEI2GO puro
        except Exception as e:
            raise RuntimeError("Falha ao carregar o modelo 'en_tei2go'.") from e

    def _next_tid(self) -> str:
        tid = f"t{self._t}"
        self._t += 1
        return tid

    # ---------- anotação ----------
    def _annotate_segment(self, parent_el, insert_after_idx: int, segment_text: str) -> int:
        """Insere <TIMEX3 tid=...>...<TIMEX3> como filhos de parent_el, com base nas entidades do trecho."""
        if not segment_text:
            return insert_after_idx

        doc = self._nlp(segment_text)
        ents = [e for e in doc.ents if e.label_ == "TIMEX"]
        ents.sort(key=lambda e: e.start_char)

        # Sem entidades → apenas texto
        if not ents:
            if insert_after_idx == -1:
                parent_el.text = (parent_el.text or "") + segment_text
            else:
                holder = parent_el[insert_after_idx]
                holder.tail = (holder.tail or "") + segment_text
            return insert_after_idx

        pos = 0
        cursor = insert_after_idx
        first_written = False

        def ensure_anchor():
            nonlocal first_written
            if not first_written:
                if insert_after_idx == -1:
                    if parent_el.text is None:
                        parent_el.text = ""
                else:
                    holder = parent_el[insert_after_idx]
                    if holder.tail is None:
                        holder.tail = ""
                first_written = True

        def put_text(s: str):
            nonlocal cursor
            if not s:
                ensure_anchor()
                return
            if insert_after_idx == -1 and not first_written:
                parent_el.text = (parent_el.text or "") + s
            elif not first_written:
                holder = parent_el[insert_after_idx]
                holder.tail = (holder.tail or "") + s
            else:
                parent_el[cursor].tail = (parent_el[cursor].tail or "") + s
            ensure_anchor()

        for ent in ents:
            if ent.start_char > pos:
                put_text(segment_text[pos:ent.start_char])

            timex_el = ET.Element("TIMEX3", tid=self._next_tid())
            timex_el.text = segment_text[ent.start_char:ent.end_char]
            parent_el.insert(cursor + 1, timex_el)
            cursor += 1
            pos = ent.end_char
            ensure_anchor()

        if pos < len(segment_text):
            put_text(segment_text[pos:])

        ensure_anchor()
        return cursor

    def _annotate_element_inline(self, el):
        # 1) texto principal do elemento
        cursor = self._annotate_segment(el, -1, el.text or "")
        # 2) tails de cada filho (não entra recursivamente no conteúdo dos filhos)
        i = 0
        while i < len(el):
            child = el[i]
            # não reanotar dentro de TIMEX3 já existente
            if isinstance(child.tag, str) and child.tag.endswith("TIMEX3"):
                cursor = i
                i = cursor + 1
                continue
            cursor = self._annotate_segment(el, i, child.tail or "")
            i = cursor + 1

    # ---------- API pública ----------
    def annotate_file(self, in_path: Path, out_path: Path) -> None:
        parser = ET.XMLParser(remove_blank_text=False)
        tree = ET.parse(str(in_path), parser)
        root = tree.getroot()

        targets = root.xpath(self.xpath)
        for el in targets:
            if isinstance(el.tag, str) and el.tag.endswith("TIMEX3"):
                continue
            self._annotate_element_inline(el)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        tree.write(str(out_path), encoding="utf-8", xml_declaration=True)

    def annotate_string(self, xml_string: str) -> str:
        parser = ET.XMLParser(remove_blank_text=False)
        root = ET.fromstring(xml_string.encode("utf-8"), parser=parser)
        for el in root.xpath(self.xpath):
            if isinstance(el.tag, str) and el.tag.endswith("TIMEX3"):
                continue
            self._annotate_element_inline(el)
        return ET.tostring(root, encoding="unicode", xml_declaration=True)
