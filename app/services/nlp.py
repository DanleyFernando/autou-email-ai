import re
from unidecode import unidecode

STOPWORDS = set('a ao aos as o os um uma umas uns de do da das dos e em no na nas nos por para com sem sob sobre entre mas ou que porque pois se então já muito muitos pouco poucos eu tu ele ela nós vós eles elas você vocês the to of in for on and or is are be am was were been being this that i you he she it we they'.split())

def preprocess(text: str) -> str:
    text = unidecode(text.lower())
    text = re.sub(r'http[s]?://\\S+', ' ', text)
    text = re.sub(r'[^a-z0-9\\s\\-\\?]', ' ', text)
    tokens = [t for t in re.split(r'\\s+', text) if t and t not in STOPWORDS]
    return ' '.join(tokens)
