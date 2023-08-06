from damenltk import DameNLTK
from nltk.corpus import PlaintextCorpusReader

dn = DameNLTK()

#corpus_root = '/usr/share/dict'
#path = '/home/davidam/git/python-examples/nlp/nltk/seedtags_exercise_classifying/'

path_exploration = '../dataset/exploration/'
path_headhunters = '../dataset/headhunters/'
path_intelligence = '../dataset/intelligence/'
path_logistics = '../dataset/logistics/'
path_politics = '../dataset/politics/'
path_transportation = '../dataset/transportation/'
path_weapons = '../dataset/weapons/'

exploration = PlaintextCorpusReader(path_exploration, '.*')
headhunters = PlaintextCorpusReader(path_headhunters, '.*')
intelligence = PlaintextCorpusReader(path_intelligence, '.*')
logistics = PlaintextCorpusReader(path_logistics, '.*')
transportation = PlaintextCorpusReader(path_transportation, '.*')
weapons = PlaintextCorpusReader(path_weapons, '.*')

# print(exploration)
# print(exploration.fileids())

for fileid in exploration.fileids():
    num_chars = len(exploration.raw(fileid))
    words = exploration.words(fileid)
    print(words)
    num_words = len(words)
    print("printing number of words")
    print(num_words)
    print(words[0:3])
    words2 = dn.remove_stopwords_from_array(words[0:3])
    print(words2)
    words3 = remove_words_not_included_in_language
    # num_sents = len(exploration.sents(fileid))
    # num_vocab = len(set(w.lower() for w in exploration.words(fileid)))
    # print(round(num_chars/num_words), round(num_words/num_sents), round(num_words/num_vocab), fileid)


#print(exploration.fileids()[0].words())
