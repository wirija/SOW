import spacy

#available models
# en_core_web_trf
# en_core_web_lg

model = spacy.load ("en_core_web_trf")


# Input text
text = "FLAT A, 31/F, BLK 2, ISLAND CREST, 8 FIRST STREET, SAI YING PUN HK, HONG KONG"

# Process the text
doc = model(text)

# Extract named entities
for ent in doc.ents:
    print (ent.label)
    print(ent.text, ent.label_)
