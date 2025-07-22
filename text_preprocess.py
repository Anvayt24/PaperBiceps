from pydoc import text
import re

def clean_text(text):

    text = re.sub(r'\n{2,}', '\n', text) # Remove multiple empty lines
    text = re.sub(r'\[\d+\]', '' , text) # Remove citation brackets
    text = re.sub(r'\[\d+\]', '' , text)
    text = re.sub(r'•\s+', '', text) # Remove bullet points
    text = re.sub(r'^\s*[\d]+\.\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
     
    return text.strip()

