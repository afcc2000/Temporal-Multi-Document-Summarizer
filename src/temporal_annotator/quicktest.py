import spacy

# carregar o modelo TEI2GO (inglês)
nlp = spacy.load("en_tei2go")

# texto de teste
text = "On the third day he rose early in the morning. The next day he travelled at 6:00."
doc = nlp(text)

print("Texto:", text)
print("Entidades encontradas:")
for ent in doc.ents:
    print(ent.text, ent.label_)
