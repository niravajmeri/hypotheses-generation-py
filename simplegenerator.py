#Importing configuration
import configparser
config = configparser.ConfigParser()
config.read("config.txt")

word2vec_path = config.get("configuration","word2vec_path")
stanford_corenlp_path = config.get("configuration","stanford_corenlp_path")


# Importing word2vec to find similarity and neighboring words
import gensim
from gensim.models import Word2Vec

model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_path, binary=True) 

from stanfordcorenlp import StanfordCoreNLP

# importing StandfordCoreNLP to tokenize, tag, and ner
nlp = StanfordCoreNLP(stanford_corenlp_path)

sentence = "NCSU students threw stones on Google's server."
sentence_tokens = nlp.word_tokenize(sentence)
sentence_tags = nlp.pos_tag(sentence)
sentence_ner = nlp.ner(sentence)
#sentence_parse = nlp.parse(sentence)
#sentence_dependency = nlp.dependency_parse(sentence)

to_replace_ners = []
to_replace_verbs = []

topk = 10 
replacement_ners = []
replacement_verbs = []

for (i, j) in sentence_ner:
    #print(i, j)
    if(j!='O'):
        print(i, j)
        to_replace_ners.append((i,j))
        similar_ners = model.most_similar(i, [], topk)
        print(similar_ners)
        replacement_ners.append((i, similar_ners))
    
verb_check = 0
        
for (i, j) in sentence_tags:
    if(verb_check == 1):
        verb = verb + '_' + i
        to_replace_verbs = [verb]
        verb_check = 0
        print(verb)
        similar_verbs = model.most_similar(verb, [], topk)
        print(similar_verbs)
        replacement_verbs.append((verb,similar_verbs))
    
    if(j=='VBD'):
        print(i, j)
        verb_check = 1
        verb = i
    
        
nlp.close()


#for (i, j) in to_replace_ners:
#    similar_ners = model.most_similar(i, [], topk)
#    replacements_ners.append((i, similar_ners))

print(replacement_ners)
    
#for verb in replacements_verbs:
#    similar_verbs = model.most_similar(verb, [], topk)
#    replacement_verbs.append((verb,similar_verbs))

print(replacement_verbs)
