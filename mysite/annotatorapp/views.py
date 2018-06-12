from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from . import models,forms,codeforline
from .models import Sentences,WordOptions,Wordsinsentence,User
from .tables import WordOptionsTable,SentencesTable,WordsinsentenceTable
import json 
from django_datatables_view.base_datatable_view import BaseDatatableView

#renders response for index page
def index(request) :
	return render(request,'annotatorapp/index.html',{})

#rende
def lineview(request) :
	return render(request,'annotatorapp/index.html',{})

def wordtableview(request) :
	tabledata = WordOptionsTable(WordOptions.objects.all())
	return render(request,'annotatorapp/tables.html',{'tabledata' : tabledata})
		
def sentenceview(request) :
	tabledata = SentencesTable(Sentences.objects.all())
	return render(request,'annotatorapp/tables.html',{'tabledata' : tabledata})

def wordsinsentenceview(request) :
	tabledata = WordsinsentenceTable(Wordsinsentence.objects.all())
	return render(request,'annotatorapp/tables.html',{'tabledata' : tabledata})

#for rendering response  upon obtaining data
def get_dragdata(request):
	if request.is_ajax() :
		if request.method == 'POST':
			sent_id = json.loads(request.POST['sentid'])
			Sentence1 = Sentences.objects.get(id = sent_id)
			wordsdata = WordOptions.objects.all().filter(sentence = Sentence1)
			data  = codeforline.getsentwordtree(sent_id);
			print(data)
			return HttpResponse(data)
	else:
		raise Http404

#for rendering response upon saving the selected data to database
def save_dragdata(request):
	if request.is_ajax() :
		if request.method == 'POST':
			wp = json.loads(request.POST['wp'])
			wc = json.loads(request.POST['wc'])
			wr = json.loads(request.POST['wr'])
			sent_id = json.loads(request.POST['sentid'])
			Sentence1 = Sentences.objects.get(id = sent_id)
			wordsdata = WordOptions.objects.all().filter(sentence = Sentence1)
			for w in wordsdata :
				try:
					w.isSelected = False
					w.isEliminated = True
					w.parent = -1
					w.relation = ''
					w.children = ''
					w.save()
				except Exception as e:
					print("wordsdata updated in ajex save_dragdata:selection elimination ")
					print(e)
			for i in wp:
				try:
					w = WordOptions.objects.get(id = i)
					w.parent = int(wp[i])
					w.isSelected = True
					w.isEliminated = False
					w.save()
				except Exception as e:
					print("Wordsinsentencenot updated in ajex save_dragdata:wp ")
					print(e)
			for i in wr:
				try:
					w = WordOptions.objects.get(id = i)
					w.relation = wr[i]
					w.isSelected = True
					w.isEliminated = False
					w.save()
				except Exception as e:
					print("Wordsinsentencenot updated in ajex save_dragdata:wr ")
					print(e)
			for i in wc:
				try:
					w = WordOptions.objects.get(id = i)
					w.children = w.children+wc[i]
					w.isSelected = True
					w.isEliminated = False
					w.save()
				except Exception as e:
					print("Wordsinsentencenot updated in ajex save_dragdata:wc ")
					print(e)	
			return HttpResponse("Success!")
	else:
		raise Http404
		
def presentdataview(request) :
	if request.method == "POST":
		Inputlineform = forms.inputlineform(request.POST)
		saveline = True
		if Inputlineform.is_valid():
			print('form is is_valid')
			try:
				Sentence = Sentences(
										line = Inputlineform.cleaned_data['line'],
										linetype = Inputlineform.cleaned_data['linetype'],
									)

				if not codeforline.checksent(Sentence) : # if new sentence appears
					df = codeforline.getdatafromsite(Sentence)
					if saveline :
						Sentence.save()
						codeforline.savedatafromsite(df,Sentence)
						print("Adding Sentences data to Database \n\n")
				if  codeforline.checksent(Sentence) :
					Sentence1 = Sentences.objects.get(line = Sentence.line,linetype=Sentence.linetype)
					wordsdata = WordOptions.objects.all().filter(sentence = Sentence1)
					words = Sentence1.line.split(' ')
					chunknum = {}
					c = 0
					for word in words :
						c = c+1
						chunknum[word] = c
					sent_id = Sentence1.id
					pos = 0
					context  = codeforline.contestofwordsdata(sent_id)
					return render(request,'annotatorapp/presentdata.html',context)
				else :
					wordsdata = codeforline.worddataofsentence(df,Sentence)
					return render(request,'annotatorapp/presentdata.html',{'wordsdata' : wordsdata,'words' : Sentence.line.split(' ')})
			except Exception as e:  
				print("Sentence not inserted : ")
				print(e)
		Sentences1 = Sentences.objects.all()
		for s in Sentences1 :
		 sent_id = s.id
		 break
		return render(request,'annotatorapp/presentdata.html',{'sentid':sent_id})
	else :
		Sentence1 = Sentences.objects.get(id = request.session.get('sent_id'))
		wordsdata = WordOptions.objects.all().filter(sentence = Sentence1)
		words = Sentence1.line.split(' ')
		chunknum = {}
		c = 0
		for word in words :
			c = c+1
			chunknum[word] = c
		sent_id = Sentence1.id
		pos = 0
		context = codeforline.contestofwordsdata(sent_id)
		return render(request,'annotatorapp/presentdata.html',context)
	
def select_wordoptionview(request,sent_id,wordoption_id) :
	wo = WordOptions.objects.get(id=wordoption_id)
	wo.isSelected = True
	request.session['sent_id'] = sent_id
	wo.save()
	return redirect('annotatorapp:presentdataview')			

#for eliminating the conflicting segments
def eliminate_wordoptionview(request,sent_id,wordoption_id) :
	wo = WordOptions.objects.get(id=wordoption_id)
	wo.isEliminated = True
	wo.save()
	request.session['sent_id'] = sent_id
	return redirect('annotatorapp:presentdataview')	

#for resetting every selected segment back to the initial position
def reset_allselectionview(request,sent_id)	:
	#collecting required values
	Sentence1 = Sentences.objects.get(id = sent_id)
	wordsdata = WordOptions.objects.all().filter(sentence = Sentence1	)
	#iterating through the collected values and initializing them
	for wo in wordsdata :
		wo.isSelected = False
		wo.isEliminated=False
		wo.parent = -1
		wo.relation = ''
		wo.children = ''
		wo.save()
	request.session['sent_id'] = sent_id
	return redirect('annotatorapp:presentdataview')

#rendering response for saving details of each data segment clicked by user
def save_data_to_db(request):
	if request.is_ajax():
		if request.method == 'POST':
			#load the data to be saved into model
			it = json.loads(request.POST['it'])
			et = json.loads(request.POST['et'])
			cs = json.loads(request.POST['cs'])
			ss = json.loads(request.POST['ss'])
			user = User(savedSentence=ss,clickSequence=cs,init_time=it,end_time=et)
			user.save()
			return HttpResponse('Success')
	else:
		raise Http404

	