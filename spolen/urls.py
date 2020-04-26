from django.urls import path
from . import views

app_name = 'spolen'

urlpatterns = [

	path('', views.spolen_index, name = 'spolen-index'),
	
	path('create/poll/',views.spolen_create_poll, name = 'spolen-create-poll'),
	path('create/poll/<str:slug>/options/',views.spolen_add_poll_options, name = 'spolen-add-poll-options'),
	path('polls/<str:slug>/participate/', views.spolen_polls_participate, name = 'spolen-polls-participate'),
	path('polls/<str:slug>/<str:option>/vote/', views.spolen_polls_vote, name = 'spolen-polls-vote'),

	path('create/survey/', views.spolen_create_survey, name = 'spolen-create-survey'),
	path('create/survey/<str:slug>/questions/', views.spolen_add_survey_questions, name = 'spolen-add-survey-questions'),
	path('create/survey/<str:slug>/questions/<str:ques>/<str:qtype>/options/', views.spolen_add_survey_questions_options, name = 'spolen-add-survey-question-options'),
	path('surveys/<str:slug>/participate/', views.spolen_surveys_participate, name = "spolen-surveys-participate"),
	path('surveys/<str:slug>/response/', views.spolen_surveys_response, name = "spolen-surveys-response"),

	path('preview/<str:ent>/<str:slug>/', views.spolen_preview, name = 'spolen-preview'),
	path('publish/<str:ent>/<str:slug>/', views.spolen_publish, name = 'spolen-publish'),
	path('discard/<str:ent>/<str:slug>/', views.spolen_discard, name = 'spolen-discard'),
	path('response/<str:ent>/<str:slug>/', views.spolen_analytics, name = 'spolen-analytics'),
	path('close/<str:ent>/<str:slug>/', views.spolen_close, name = 'spolen-close'),
	path('open/<str:ent>/<str:slug>/', views.spolen_open, name = 'spolen-open'),
	

]
