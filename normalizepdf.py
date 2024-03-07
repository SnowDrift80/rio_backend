import re
import sys
import time
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize


def set_brackets(text):
    text = '[[' + text
    switch = "open"
    active = False
    new_text = ""
    for i in text:
        new_text += i
        if ord(i) == 10:
            if active == False:
                if switch == "open":
                    new_text += "]]"
                    switch = "closed"
                else:
                    new_text += "[["
                    switch = "open"
                active = True
        else:
            active = False
    if switch == "open":
        new_text += "]]"
    return new_text


def remove_lf(text):
    text = text.replace(" \n \n \n \n", "\k\k")
    text = text.replace("\n \n \n \n ", "\k\k")
    text = text.replace(" \n \n \n", "\k\k")
    text = text.replace("\n \n \n ", "\k\k")
    text = text.replace(" \n \n", "\k\k")
    text = text.replace("\n \n ", "\k\k")
    # text = text.replace("\n ", "\k\k")
    # text = text.replace(" \n", "\k\k")
    text = text.replace("\n", " ")
    cleaned_text = text.replace("\k", "\n\n")

    
    return cleaned_text


def extract_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        pages = reader.pages
        text = ''
        for page in pages:
            text += page.extract_text()

    return text


def write_txt(txt_path, text):
    with open(txt_path, 'w') as file:
        file.write(text)

pdf_path = "docs/passo_a_passo_como_gerar_o_pin.pdf"
text = extract_pdf(pdf_path=pdf_path)
cleaned_text = remove_lf(text)
final_text = set_brackets(cleaned_text)
write_txt("docs/passo_a_passo_como_gerar_o_pin.not", final_text)
print(final_text)
