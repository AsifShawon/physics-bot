import spacy
nlp = spacy.load("en_core_web_md")
doc1 = nlp("Hello")
doc2 = nlp("Hi there")
print("Similarity:", doc1.similarity(doc2))
