# src/temporal_annotator/quicktest.py
from pathlib import Path
from annotatorMVP import Tei2goInlineAnnotator

def main():
    # calcula o caminho do projeto a partir deste arquivo:
    project_root = Path(__file__).resolve().parents[2]  # .../Temporal-Multi-Document-Summarizer
    in_path  = project_root / "data" / "raw" / "EnglishNIVMatthew40_PW.xml"
    out_path = project_root / "data" / "processed" / "EnglishNIVMatthew40_PW_TEI2GO.xml"

    annot = Tei2goInlineAnnotator(xpath=".//verse")  # anota todos os <verse>
    annot.annotate_file(in_path, out_path)

    print(f"✔ anotado: {out_path}")

if __name__ == "__main__":
    main()
