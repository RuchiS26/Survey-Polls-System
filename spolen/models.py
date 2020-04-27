from django.db import models
from django.contrib.auth.models import User

TYPE_CHOICES = [
	('Short Answer','Short Answer'),
	('Multiple Choice Opition', 'Multiple Choice Opition'),
]


class Poll(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	title = models.CharField(max_length = 256)
	question = models.CharField(max_length = 256)
	slug = models.SlugField(unique = True)
	date_posted = models.DateField(auto_now_add = True)
	public = models.BooleanField(default = False)
	closed = models.BooleanField(default = False)

	def __str__(self):
		return str(self.title)

class PollOption(models.Model):
	poll = models.ForeignKey(Poll, on_delete = models.CASCADE)
	option = models.CharField(max_length = 256)
	votes = models.PositiveIntegerField(default = 0)

	def __str__(self):
		return str(self.option) + " | " + str(self.poll)

class Survey(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	title = models.CharField(max_length = 128)
	breif = models.CharField(max_length = 128,default = "Survey")
	description = models.TextField(max_length = 1024)
	slug = models.SlugField(unique = True)
	date_posted = models.DateField(auto_now_add = True)
	public = models.BooleanField(default = True)
	closed = models.BooleanField(default = False)
	responses = models.PositiveIntegerField(default = 0)

	def __str__(self):
		return str(self.title)

class SurveyQuestion(models.Model):
	survey = models.ForeignKey(Survey, on_delete = models.CASCADE)
	question = models.CharField(max_length = 256)
	question_type = models.CharField(choices = TYPE_CHOICES, default = 'Short Answer', max_length = 256)

	def __str__(self):
		return str(self.survey)+" | "+str(self.question)

class ShortAnswer(models.Model):
	question = models.ForeignKey(SurveyQuestion, on_delete = models.CASCADE)
	answer = models.CharField(max_length = 256)

	def __str__(self):
		return str(self.question)

class MultipleChoiceOption(models.Model):
	question = models.ForeignKey(SurveyQuestion, on_delete = models.CASCADE)
	option = models.CharField(max_length = 256)
	votes = models.PositiveIntegerField(default = 0)

	def __str__(self):
		return str(self.question)

class PollAccess(models.Model):
	poll = models.ForeignKey(Poll, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.poll)

class SurveyAccess(models.Model):
	survey = models.ForeignKey(Survey, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.survey)
