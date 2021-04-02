import math
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
    link = models.CharField(_("link to question"), max_length=500)
    original = models.CharField(_("original question"), max_length=500)
    clean = models.CharField(_("cleaned question"), max_length=500)

    def __str__(self):
        return self.original
    def __unicode__(self):
        return self.original

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class IDF(models.Model):
    word = models.CharField(_("word"), max_length=50, unique=True)
    idf = models.FloatField(_("idf"), default=0)

    def __str__(self):
        return self.word

    def __unicode__(self):
        return self.word

    class Meta:
        verbose_name = 'IDF'
        verbose_name_plural = 'IDFs'

    @staticmethod
    def returnN():
        return Question.objects.all().count()
    
    @property
    def doc_count(self):
        return TermFrequency.objects.filter(word=self).count()

    def set_idf(self):
         self.idf = round(math.log(IDF.returnN()/self.doc_count, 10), 2)
         self.save()
        

class TermFrequency(models.Model):
    word = models.ForeignKey(IDF, verbose_name=_("word"), on_delete=models.CASCADE)
    qid = models.ForeignKey(Question, verbose_name=_("question"), on_delete=models.CASCADE)
    tf = models.IntegerField(_("term frequency"))

    def __str__(self):
        return '{}, {}'.format(self.word, self.qid)

    def __unicode__(self):
        return '{}, {}'.format(self.word, self.qid)

    class Meta:
        verbose_name = 'TermFrequency'
        verbose_name_plural = 'TermFrequencies'
        unique_together = ('word', 'qid')