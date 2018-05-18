<<<<<<< HEAD
from django.urls import path, re_path
=======
from django.urls import path,re_path
>>>>>>> f2391f19ed892a55e69cf6071e722279bc118ad8
from . import views


app_name = 'annotatorapp'

urlpatterns = [
	path('', views.index, name='index'),
	path('wordtable/',views.wordtableview,name='wordtableview'),
	path('linetable/',views.sentenceview,name='sentenceview'),
	path('wordsinsentencetable/',views.wordsinsentenceview,name='wordsinsentenceview'),
	path('presentdata/',views.presentdataview,name='presentdataview'),
	re_path(r'select/(?P<sent_id>[0-9]+)/(?P<wordoption_id>[0-9]+)/$',views.select_wordoptionview,name='select_wordoption'),
	re_path(r'eliminate/(?P<sent_id>[0-9]+)/(?P<wordoption_id>[0-9]+)/$',views.eliminate_wordoptionview,name='eliminate_wordoption'),
	re_path(r'refresh/(?P<sent_id>[0-9]+)/$',views.reset_allselectionview,name='reset_allselection'),
	path('presentdata/ajax/save_data/',views.save_dragdata,name='save_dragdata'),
	path('presentdata/ajax/get_data/',views.get_dragdata,name='get_dragdata'),
	]
