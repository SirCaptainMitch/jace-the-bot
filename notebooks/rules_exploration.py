from rich.console import Console
import nltk

nltk.download('punkt')

console = Console()


with open('../.cache/gatherer_rules/20231013.txt', 'r', encoding='utf8') as f:
    rules = f.read()


# Splitting Text into Sentences
def split_text_into_sentences(text):
    s = nltk.sent_tokenize(text)
    return s


sentences = split_text_into_sentences(rules)

console.print(sentences)
