from django.contrib import admin
from .models import Survey,Poll,PollOption,SurveyQuestion,ShortAnswer,MultipleChoiceOption

admin.site.register(Survey)
admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(SurveyQuestion)
admin.site.register(ShortAnswer)
admin.site.register(MultipleChoiceOption)


