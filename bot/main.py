from os import system, name
import spacy
import PyPDF2
import os
import mimetypes
import textract
nlp = spacy.load("es_dep_news_trf")
import es_dep_news_trf
nlp = es_dep_news_trf.load()

def clearScreen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
 
clearScreen()

def getTextFromDocFile(docxFile):
    text = textract.process(docxFile)
    return text

def getTextFromPdfFile(pdfFile):
    pdf = PyPDF2.PdfReader(pdfFile)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

def getDocumentsFromPath(path):
    print(f"Gettings documents from: {path}")
    files = []
    for file in os.listdir(path):
        fileType = mimetypes.guess_type(file)[0]
        if "pdf" in fileType:
            print(f"PDF Document {path+file}")
            files.append({"type":"pdf","document":(path+file)})
        elif "msword" in fileType:
            print(f"Word Document: {path+file}")
            files.append({"type":"doc","document":(path+file)})
        elif "wordprocessingml.document" in fileType:
            print(f"Wordx Document: {path+file}")
            files.append({"type":"doc","document":(path+file)})
    return files

def readFilesfromPath(path):
    files = []
    text = ""
    files = getDocumentsFromPath("docs/")
    for file in files:
        if file["type"] == "doc":
            text = text + str(getTextFromDocFile(file["document"]))
        elif file["type"] == "pdf":
            text = text + getTextFromPdfFile(file["document"])
    text = text.replace("\\n","\n").replace("\\xc3\\xa1","á").replace("\\xc3\\xa9","é").replace("\\xc3\\xad","í").replace("\\xc3\\xb3","ó").replace("\\xc3\\xba","ú")
    return text

path = "docs/"
entities = []
print("Convert docs to text...")
content = readFilesfromPath(path)
print("Reading entities from docs content...")
document = nlp(content)
print(document.ents)
entities = document.ents
print(entities)
loop = True
while loop:
    print("")
    ask = input("Please, write your question, or quit for end: ")
    if "quit" not in ask:
        response = []
        for entity in entities:
            if ask in entity.text:
                response.append(entity.text)
        print(response)
    else:
        loop = False


