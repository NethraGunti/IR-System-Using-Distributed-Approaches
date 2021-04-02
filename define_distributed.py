import time
from stackapi import StackAPI, StackAPIError
from celery import Celery
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

BACKEND_URL = 'redis://localhost:6379'
BROKER_URL = 'amqp://localhost'
celery_app = Celery('Crawler', broker=BROKER_URL, backend=BACKEND_URL)

KEY = '1e*14UFc3n18Nf9CPoLzDQ(('
SITE = StackAPI('stackoverflow', key=KEY)
SITE.page_size=100

STOP_WORDS = {'I', 'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'}

@celery_app.task(trail=True)
def _crawlSAPI(tag, start, end, sort='votes', order='desc'):
    QUESTIONS = []
    for i in range(start, end+1):
        try:
            current = SITE.fetch('questions', tagged=tag, sort=sort, order=order, page=i)
            print(current['quota_remaining'])
            for x in current['items']:
                QUESTIONS.append((x['title'], x['link']))
            print('Crawled Page No. {}'.format(i))
        except StackAPIError as e:
            # print(e)
            # print('Error in Fetching Page Number '+str(i))
            continue
    return QUESTIONS


@celery_app.task
def _clean_and_tokenise(sentence):
    tokenized_sentence = word_tokenize(sentence)
    cleaned_tokens = [w.lower() for w in tokenized_sentence if not w.lower() in STOP_WORDS]
    cleaned_sentence = ' '.join(str(e) for e in cleaned_tokens)
    return cleaned_sentence