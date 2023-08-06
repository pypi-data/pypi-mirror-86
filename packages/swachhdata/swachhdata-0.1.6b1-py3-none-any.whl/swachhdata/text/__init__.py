import re
import pandas
from tqdm.auto import trange, tqdm
from bs4 import BeautifulSoup
from html import unescape
import contractions
import emoji
from emoji import UNICODE_EMOJI
import nltk
nltk.download('popular', quiet=True)
import spacy
from gensim.parsing.preprocessing import remove_stopwords
import num2words
import unicodedata
import string
import json
import textblob

from ._text import urlRecast
from ._text import htmlRecast
from ._text import EscapeSequenceRecast
from ._text import MentionRecast
from ._text import ContractionsRecast
from ._text import CaseRecast
from ._text import EmojiRecast
from ._text import HashtagRecast
from ._text import ShortWordsRecast
from ._text import StopWordsRecast
from ._text import NumberRecast
from ._text import AlphabetRecast
from ._text import PunctuationRecast
from ._text import StemmingRecast
from ._text import LemmatizationRecast
from ._text import TokenisationRecast
from ._text import ReCast


__all__ = [
    'urlRecast',
    'htmlRecast',
    'EscapeSequenceRecast',
    'MentionRecast',
    'ContractionsRecast',
    'CaseRecast',
    'EmojiRecast',
    'HashtagRecast',
    'ShortWordsRecast',
    'StopWordsRecast',
    'NumberRecast',
    'AlphabetRecast',
    'PunctuationRecast',
    'StemmingRecast',
    'LemmatizationRecast',
    'TokenisationRecast',
    'ReCast'
]
