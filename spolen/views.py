from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Poll, Survey, PollOption, PollAccess, SurveyAccess, SurveyQuestion, MultipleChoiceOption, ShortAnswer
from .forms import PollForm, SurveyForm
from django.views.decorators.csrf import csrf_exempt
import json

@login_required(login_url = 'accounts:accounts-login')
def spolen_index(request):
	polls = Poll.objects.filter(closed = False).filter(public = True).order_by('date_posted')
	polls_cl = Poll.objects.filter(user = request.user).filter(closed = True).order_by('date_posted')
	surveys = Survey.objects.filter(closed = False).filter(public = True).order_by('date_posted')
	surveys_cl = Survey.objects.filter(user = request.user).filter(closed = True).order_by('date_posted')
	entpoll = 'poll'
	entsurvey = 'survey'
	return render(request, "spolen/spolen-index.html", {'polls':polls,'surveys':surveys, 'polls_cl':polls_cl, 'surveys_cl':surveys_cl,'entpoll':entpoll,'entsurvey':entsurvey})

@login_required(login_url = 'accounts:accounts-login')
def spolen_create_poll(request):
	if request.method == 'POST':
		pollform = PollForm(request.POST)
		if(pollform.is_valid()):
			instance = pollform.save(commit = False)
			instance.user = request.user
			poll_count = Poll.objects.all().count()
			slug = str(request.user)+'poll-'+str(poll_count)
			instance.slug = slug

			instance.save()

			return render(request,'spolen/spolen-poll-options.html',{'poll_title':instance.title,'poll_slug': instance.slug,'obj':'poll'})

	else:
		pollform = PollForm()

	return render(request, 'spolen/spolen-create-poll.html',{'pollform':pollform})

@login_required(login_url = 'accounts:accounts-login')
def spolen_add_poll_options(request,slug):
	
	poll = Poll.objects.get(slug = slug)
	option = request.GET.get('option',None)

	PollOption.objects.create(poll = poll, option = option)

	message = "Option added to Poll"
	return render(request,'spolen/spolen-poll-messages.html',{'message':message})


@login_required(login_url = 'accounts:accounts-login')
def spolen_polls_participate(request,slug):

	poll = Poll.objects.get(slug = slug)
	if( PollAccess.objects.filter(poll = poll ).filter(user = request.user).exists() or poll.user == request.user or poll.closed):
		messages.info(request,f"Poll already answered or is created by you or is closed!")
		return redirect('spolen:spolen-index')

	else:
		options = PollOption.objects.filter(poll = poll)
		return render(request, 'spolen/spolen-poll-participate.html',{'poll':poll, 'options':options})

@login_required(login_url = 'accounts:accounts-login')
def spolen_polls_vote(request,slug,option):

	poll = Poll.objects.get(slug = slug)
	option = PollOption.objects.get(Q(poll = poll) and Q(option__exact = option))
	option.votes = int(option.votes) + 1
	option.save()
	
	user = request.user
	PollAccess.objects.create(poll = poll, user = user)

	return render(request,'spolen/spolen-poll-complete.html')


@login_required(login_url = 'accounts:accounts-login')
def spolen_create_survey(request):

	if request.method == 'POST':

		surveyform = SurveyForm(request.POST)
		if(surveyform.is_valid()):

			instance = surveyform.save(commit = False)
			instance.user = request.user
			
			survey_count = Survey.objects.all().count()
			slug = str(request.user)+'survey-'+str(survey_count)
			instance.slug = slug

			instance.save()

			return render(request, 'spolen/spolen-survey-add-questions.html', {'survey_slug': instance.slug, 'survey_title': instance.title, 'obj':'survey'})

	else:
		surveyform = SurveyForm()

	return render(request, 'spolen/spolen-create-survey.html', {'surveyform':surveyform})

@login_required(login_url = 'accounts:accounts-login')
def spolen_add_survey_questions(request,slug):

	survey = Survey.objects.get(slug = slug)
	question = request.GET.get('question',None)
	q_type = request.GET.get('q_type', None)

	SurveyQuestion.objects.create(survey = survey, question = question, question_type = q_type)


	if(q_type == "Short Answer"):
		message = "Question added"
	else:
		message = "Add options for question"

	return render(request,'spolen/spolen-messages.html',{'message':message,'question':question,'q_type':q_type,'survey_slug':survey.slug})

@login_required(login_url = 'accounts:accounts-login')
def spolen_add_survey_questions_options(request,slug,ques,qtype):

	survey = Survey.objects.get(slug = slug)
	option = request.GET.get('option', None)
	q_type = qtype
	question = SurveyQuestion.objects.last()

	MultipleChoiceOption.objects.create(question = question, option = option)

	message = "Option Added"

	return render(request, 'spolen/spolen-messages.html',{'message':message,'question':question,'survey_slug':survey.slug,'q_type':q_type})

@login_required(login_url = "accounts:accounts-login")
def spolen_surveys_participate(request,slug):
	survey = Survey.objects.get(slug = slug)

	if( SurveyAccess.objects.filter(survey = survey ).filter(user = request.user).exists() or survey.user == request.user or survey.closed):
		messages.info(request,f"Survey already answered or is created by you or is closed!")
		return redirect('spolen:spolen-index')

	else:
		options = []
		questions = SurveyQuestion.objects.filter(survey = survey)
		for question in questions:
			if(MultipleChoiceOption.objects.filter(question = question).exists()):
				opStack = (MultipleChoiceOption.objects.filter(question = question))
				for obj in opStack:
					newblock = {'question':question, 'option':(obj.option)}
					options.append(newblock)

		return render(request, 'spolen/spolen-surveys-participate.html', {'survey':survey,'questions':questions,'options':options})

@csrf_exempt
@login_required(login_url = "accounts:accounts-login")
def spolen_surveys_response(request,slug):
	survey = Survey.objects.get(slug = slug)
	questions = SurveyQuestion.objects.filter(survey = survey)
	arr = request.POST.get('answers')
	answers = json.loads(arr)
	
	for answer in answers:
		if(answer['q_type'] == "Short Answer"):
			for question in questions:
				if(question.question == answer['question']):
					ShortAnswer.objects.create(question = question, answer = answer['answer'])
		elif(answer['q_type'] == "Multiple Choice Opition"):
			for question in questions:
				if(question.question == answer['question']):
					options = MultipleChoiceOption.objects.filter(question = question)
					for option in options:
						if(option.option == answer['answer']):
							inst = MultipleChoiceOption.objects.get(question = question, option = option.option)
							inst.votes = inst.votes + 1;
							inst.save()
		else:
			test = "failed q_type"

	SurveyAccess.objects.create(survey = survey, user = request.user)
	return render(request,'spolen/spolen-survey-complete.html')

@login_required(login_url = 'accounts:accounts-login')
def spolen_preview(request,ent,slug):

	if(ent == 'poll'):
		ent = Poll.objects.get(slug = slug)
		atts = PollOption.objects.filter(poll = ent)
		obj = 'poll'
	elif(ent == 'survey'):
		ent = Survey.objects.get(slug = slug)
		atts = SurveyQuestion.objects.filter(survey = ent)
		obj = 'survey'

	return render(request, 'spolen/spolen-preview.html', {'obj':obj,'ent':ent,'atts':atts})

@login_required(login_url = 'accounts:accounts-login')
def spolen_publish(request,ent,slug):

	if(ent == 'poll'):
		ent = Poll.objects.get(slug = slug)
		ent.public = True
		ent.save()
		messages.success(request,f'Poll created!')

	elif(ent == 'survey'):
		ent = Survey.objects.get(slug = slug)
		ent.public = True
		ent.save()
		messages.success(request,f'Survey created!')

	return redirect('spolen:spolen-index')

@login_required(login_url = 'accounts:accounts-login')
def spolen_discard(request,ent,slug):

	if(ent == 'poll'):
		ent = Poll.objects.get(slug = slug).delete()
		messages.success(request,f'Poll discarded!')

	return redirect('spolen:spolen-index')

def spolen_analytics(request,ent,slug):

	if(ent == 'poll'):
		poll = Poll.objects.get(slug = slug)
		if(poll.user == request.user):
			options = PollOption.objects.filter(poll = poll).order_by('-votes')

			return render(request, 'spolen/spolen-analytics.html', {'poll':poll,'options':options,'ent':ent})

		else:
			messages.success(request, 'Invalid Access!')
			return redirect('spolen:spolen-index')

	elif(ent == 'survey'):
		saDict = []
		mcqDict = []
		survey = Survey.objects.get(slug = slug)
		if(survey.user == request.user):
			questions = SurveyQuestion.objects.filter(survey = survey)
			for question in questions:
				if(ShortAnswer.objects.filter(question = question).exists()):
					answers = ShortAnswer.objects.filter(question = question)
					for answer in answers:
						newblock = {'question':question,'answer':answer.answer}
						saDict.append(newblock)
				elif(MultipleChoiceOption.objects.filter(question = question).exists()):
					options = MultipleChoiceOption.objects.filter(question = question).order_by('-votes')
					for option in options:
						newblock = {'question':question, 'option':option.option, 'votes':option.votes}
						mcqDict.append(newblock)

			return render(request, 'spolen/spolen-analytics.html', {'survey':survey,'saDict':saDict,'mcqDict':mcqDict,'ent':ent,'questions':questions})

		else:
			messages.success(request, 'Invalid Access!')
			return redirect('spolen:spolen-index')

@login_required(login_url = 'accounts:accounts-login')
def spolen_close(request, ent, slug):
	if ent == "poll":
		poll = Poll.objects.get(slug = slug)
		poll.closed = True
		poll.public = False
		poll.save()

	elif ent == "survey":
		survey = Survey.objects.get(slug = slug)
		survey.closed = True
		survey.public = False
		survey.save()

	messages.success(request, f'Successfully Closed!')
	return redirect('spolen:spolen-index')


@login_required(login_url = 'accounts:accounts-login')
def spolen_open(request, ent, slug):
	if ent == "poll":
		poll = Poll.objects.get(slug = slug)
		poll.closed = False
		poll.public = True
		poll.save()

	elif ent == "survey":
		survey = Survey.objects.get(slug = slug)
		survey.closed = False
		survey.public = True
		survey.save()

	messages.success(request, f'Successfully Opened!')
	return redirect('spolen:spolen-index')