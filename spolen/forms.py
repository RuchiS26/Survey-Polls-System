from django import forms
from .models import Poll, Survey

class PollForm(forms.ModelForm):
	class Meta:
		model = Poll
		exclude = ('user','slug','closed','public')

class SurveyForm(forms.ModelForm):
	class Meta:
		model = Survey
		fields = ('title', 'breif', 'description')