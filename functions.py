import fitz
import language_tool_python
from googletrans import Translator
import numpy as np
import re
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize


# regex stuff
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"


def fitz_scan(pdf_path):
    """
    function to scan PDFs with columns
    :param kiid_path: path of PDF
    :return: str all text from PDF
    """
    text = ''
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def correct_grammar(txt, language='pl-PL'):
    """
    grammar and spelling correct whole text
    :param txt: str text to correct
    :param language:
    :return: str corrected text
    """
    tool = language_tool_python.LanguageTool('pl-PL')
    txt = tool.correct(txt)
    tool.close()
    return txt


def tanslate(txt):
    """
    runs str thorugh Google Translate
    :param txt:
    :return:
    """
    translator = Translator()
    txt_trans = translator.translate(txt, src='pl', dest='en').text
    return str(txt_trans)

# split into sentences


def split_into_sentences(text):
    """
    splits str into array of sentences
    :param text: text to split
    :return: array of sentences
    """
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\1<prd>",text)
    text = re.sub(websites,"<prd>\1",text)
    text = re.sub(digits + "[.]" + digits,"\1<prd>\2",text)
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\1<stop> \2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\1<prd>\2<prd>\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\1<prd>\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \1<stop> \2",text)
    text = re.sub(" "+suffixes+"[.]"," \1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "!" in text: text = text.replace("!"",""!")
    #if "?" in text: text = text.replace("?"",""?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


def ToString(value):
    return ''.join(value.splitlines())


def stem(txt):
    snowball = SnowballStemmer(language='english')
    tokenized = word_tokenize(txt)
    stem = [snowball.stem(word) for word in tokenized]

    return stem

