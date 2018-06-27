import os
import pickle

dirname = os.path.dirname(__file__)
directory_1 = os.path.join(dirname,'100')
directory_2 = os.path.join(dirname,'100_graphml')

class DCS:
    def __init__(self,sent_id,sentence):
        self.sent_id = sent_id
        self.sentence = sentence
        self.dcs_chunks = []
        self.lemmas = []
        self.cng = []

##for filename in os.listdir(directory_1):
##    print(filename)
##    if filename.endswith('.p'):
##        output_load = pickle.load(open('100/'+filename, "rb"), encoding='utf-8')
##        print(output_load)
##        print('Sentence Id:',output_load.sent_id)
##        print('Sentence:',output_load.sentence)
##        print('Chunks:',output_load.dcs_chunks)
##        print('Lemmas:',output_load.lemmas)
##        print('Morphological class (CNG):',output_load.cng)

for filename in os.listdir(directory_2):
    print(filename)
    f = open(filename)
    
    
