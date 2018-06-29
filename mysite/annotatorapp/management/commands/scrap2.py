import os
from django.core.management.base import BaseCommand
from annotatorapp.models import Exsentences


dirname = os.path.dirname(__file__)
path = os.path.join(dirname,'answers.txt')

class Command(BaseCommand):
	help = 'Populates the database with example sentences and their solution'
	    
	def extract(self):
		f = open(path,encoding='utf-8')
		for l in f.readlines():
			c=l.split('#')
			line = c[0].rstrip()
			line = line.replace("'","\\'")
			chunks = c[1]
			lemmas = c[2]
			morph_cng = c[3][:-1]
			try:
				xsent = Exsentences(line=line,chunks=chunks,lemmas=lemmas,morph_cng=morph_cng)
				xsent.save()
			except Exception as e:
				print(e)
		f.close()			
	
	def delete_data(self):
		Exsentences.objects.all().delete()

	def handle(self, *args, **options):
		self.delete_data()
		self.extract()	