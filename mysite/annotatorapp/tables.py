from .models import Sentences,WordOptions,Wordsinsentence
from table import Table
from table.columns import Column


class WordOptionsTable(Table):
	id = Column(field='id',header='#')
	word = Column(field='word',header='word')
	lemma = Column(field='lemma',header='Lemma')
	morph = Column(field='morph',header='Morph')
	aux_info = Column(field='aux_info',header='aux_info')
	pre_verb = Column(field='pre_verb',header='pre_verb')

class SentencesTable(Table):
	id = Column(field='id',header='#')
	line = Column(field='line',header='Sentence')

class WordsinsentenceTable(Table):
	id = Column(field='id',header='#')
	word = Column(field='word',header='word')
	parent = Column(field='parent',header='parent')
	children = Column(field='children',header='children')
	relation = Column(field='relation',header='relation')
	wordoptions = Column(field='wordoptions',header='wordoptions')