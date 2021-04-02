import json
import time

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from django.http import HttpResponse
from django.shortcuts import render, redirect

from irdc.models import Question, IDF
from irdc.tasks import _write_json_to_db, _write_unique_words_and_tf, _write_idf, _search_postings, _get_tfidf
from irdc.forms import SearchForm


def _writer_main(request):
    # print('Starting Task')
    # TASKS = []
    # start_time = time.time()
    # clean_files = ['clean_p1.json', 'clean_p2.json', 'clean_p3.json', 'clean_p4.json']
    # TASKS.extend(
    #     [_write_json_to_db.apply_async(
    #         args=[f]
    #         ) for f in clean_files
    #     ]
    # )
    # end_time = time.time() - start_time
    # print('Ended Task')
    # return HttpResponse("Wrote JSON objects to db in {} seconds".format(str(end_time)))
    return HttpResponse("TASK HAS BEEN HIDDEN! IN CASE YOU WANT TO REWRITE THE DB, REMOVE ALL THE ROWS FROM THE DB AND EDIT THE SOURCE CODE TO RUN IT AGAIN")


#write uniuqe words to db from questions and simultaneously calc tf
def get_unique_words(request):
    # TASKS = []
    # print('Starting Task')
    # start_time = time.time()
    # questions = Question.objects.all()
    # for q in questions:
    #     TASKS.append(
    #         _write_unique_words_and_tf.apply_async(
    #             args=[q.id]
    #             )
    #     )
    # end_time = time.time() - start_time
    # print('Ended Task')
    # return HttpResponse("Calculated Term frequencies in {} seconds".format(str(end_time)))
    return HttpResponse("TASK HAS BEEN HIDDEN! IN CASE YOU WANT TO REWRITE THE DB, REMOVE ALL THE ROWS FROM THE DB AND EDIT THE SOURCE CODE TO RUN IT AGAIN")


def calc_idf(request):
    # TASKS = []
    # print('Starting Task')
    # start_time = time.time()
    # TASKS.extend(
    #     [
    #         _write_idf.apply_async(
    #             args=[f.id]
    #         ) for f in IDF.objects.all()
    #     ]
    # )
    # end_time = time.time() - start_time
    # print('Ended Task')
    # return HttpResponse("Calculated IDF in {} seconds".format(str(end_time)))
    return HttpResponse("TASK HAS BEEN HIDDEN! IN CASE YOU WANT TO REWRITE THE DB, REMOVE ALL THE ROWS FROM THE DB AND EDIT THE SOURCE CODE TO RUN IT AGAIN")



STOP_WORDS = {'I', 'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'}
def get_postings(sentence):
    # sentence  = input("Enter Query: ")
    start_time = time.time()
    tokenized_sentence = word_tokenize(sentence)
    cleaned_tokens = [w.lower() for w in tokenized_sentence if not w.lower() in STOP_WORDS]
    N = len(cleaned_tokens)
    common_docs = {}
    TASKS = []
    for word in cleaned_tokens:
        TASKS.append(
            _search_postings.apply_async(
                args=[word]
            )
        )
    for i in range(N):
        w = cleaned_tokens[i]
        common_docs[w] = TASKS[i].wait(timeout=None, interval=0.5)
    
    sorted_docs = sorted(common_docs.values(), key=lambda item: len(item))
    common = set(sorted_docs[0])
    for i in range(N):
        temp = set(sorted_docs[i])
        common = common.intersection(temp)
        if len(common) > 0:
            continue
        else:
            break
    common = list(common)
    if len(common) == 0:
        common = []
        common.extend([sorted_docs[i] for i in range(N)])
    
    results = calc_tfidf(cleaned_tokens, common)
    end_time = time.time() - start_time
    print('Search Completed in {}'.format(str(end_time)))
    return ([Question.objects.get(id=qid) for qid in results], end_time)


def calc_tfidf(words, common):
    TASKS = []
    for qid in common:
        TASKS.append(
            _get_tfidf.apply_async(
                args=[words, qid]
            )
        )
    tfidf = {}
    for i in range(len(common)):
        tfidf[common[i]] = TASKS[i].wait(timeout=None, interval=0.5)
    ranked_ques = sorted(tfidf.keys(), key=lambda x:tfidf[x])
    return ranked_ques


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            results, end_time = get_postings(sentence=query)
            return render(request, 'irdc/results.html', {'results':results, 'endtime':end_time})

    else:
        form = SearchForm()
    return render(request, 'irdc/search.html', {'form':form})