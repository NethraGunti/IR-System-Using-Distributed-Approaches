from django.contrib import admin
from irdc.models import Question, IDF, TermFrequency

admin.site.register(Question)
admin.site.register(IDF)
admin.site.register(TermFrequency)