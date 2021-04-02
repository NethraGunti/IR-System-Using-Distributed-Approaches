import os
import json
import time
from collections import Counter

from celery import Celery

from irdc.models import Question, IDF, TermFrequency

BACKEND_URL = 'redis://localhost:6379'
BROKER_URL = 'amqp://localhost'
celery_app = Celery('Crawler', broker=BROKER_URL, backend=BACKEND_URL, include=['assign02.tasks'])

@celery_app.task(trail=True)
def _write_json_to_db(json_file):
    f = open(os.path.dirname(__file__) + '/../../'+json_file, "r")
    dump = json.loads(f.read())
    for i in dump:
        try:
            Question.objects.get(link=i['link'])
        except:
            Question.objects.create(
                link=i['link'],
                original=i['original'],
                clean=i['clean']
            ).save()

@celery_app.task(trail=True)
def _write_unique_words_and_tf(qid):
    question = Question.objects.get(id=qid)
    words = question.clean.split(" ")
    counter = Counter(words)
    print(counter)
    for word in words:
        try:
            wordid = IDF.objects.get(word=word)
        except:
            try:
                wordid = IDF.objects.create(word=word)
                wordid.save()
            except:
                pass
        try:
            tfid = TermFrequency.objects.get(word=wordid, qid=question)
        except:
            try:
                tfid = TermFrequency.objects.create(
                    word=wordid,
                    qid=question,
                    tf=counter[word]
                )
                tfid.save()
            except:
                pass

@celery_app.task(trail=True)
def _write_idf(idfid):
    obj = IDF.objects.get(id=idfid)
    obj.set_idf()


@celery_app.task(trail=True)
def _search_postings(word):
    idfid = IDF.objects.get(word=word)
    term_frequencies = TermFrequency.objects.filter(word=idfid).values('qid')
    ids = []
    for i in term_frequencies:
        ids.extend(i.values())
    return ids

@celery_app.task(trail=True)
def _get_tfidf(words, qid):
    tf = []
    for word in words:
        idf = IDF.objects.get(word=word)
        try:
            frequencies = TermFrequency.objects.filter(
                word=idf,
                qid=qid
            ).first()
            tf.append(
                idf.idf * frequencies.tf
            )
        except:
            tf.append(0)
    return sum(tf)