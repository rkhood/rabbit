import nltk


def get_sentences(filename='chap1_alice.txt'):

    with open(filename) as f:
        text = f.read()
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(text.strip())
    return sentences


def get_nouns(sentence):

    is_noun = lambda pos: pos[:2] == 'NN'
    tokenized = nltk.word_tokenize(sentence)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]

    if nouns == []:
        nouns = ' '
    return nouns
