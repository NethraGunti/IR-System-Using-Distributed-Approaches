_______________________________________________________________________________________________________

I N F O R M A T I O N  &nbsp;  R E T R I E V A L  &nbsp;  S Y S T E M  &nbsp;  U S I N G  &nbsp;  D I S T R I B U T E D  &nbsp;  A P P R O A C H E S
_______________________________________________________________________________________________________

Contributors
------------------------------

Nethra Gunti - S20180010061 / nethra.g18@iiits.in

------------------------------
GitHub Repo Link
------------------------------

https://github.com/NethraGunti/IR-System-Using-Distributed-Approaches

------------------------------
KEY POINTS TO REMEMBER
------------------------------

> This project has been done in `python 3.8.x`

> The database used is `POSTGRESQL`

> In order to incorporate the Distributed Approaches, `Celery` has been used as the Distributed System. Almost every operation has been perfomed only using Celery

> This Celery application used `Rabbitmq Server` as the message broker and `Redis Server` as its backend. So make sure you have both the servers up and running.

> Do not run any operations other than search because other processes take a lot of time and configuration

> The steps to test the remaining features have been mentioned below

_______________________________________________________________________________________________________

INTRODUCTION
------------------------------

This project contains the implementation of a domain specific IR system built using distributed approaches. The database consists of around 300,000 questions tagged `python` from StackOverFlow crawled using the `StackAPI` along side `Celery`. The task implementd in this application is returning questions similar to the input query

_______________________________________________________________________________________________________

COMPONENTS
------------------------------

Following are the comoponents of this IR system:

1.  Web Crawling (using STACKAPI)
2.  Data Cleaning (removing stop words and tokenization)
2.  Inverted Indexing
3.  Boolean Retrieval
4.  Ranked Retrieval
5.  Search


------------------------------
DATABASE SCHEMA
------------------------------

> Question -> < link, original, clean >

	description: table containing all the original questions, their cleaned versions and the link to the questions


> IDF-> < word, idf >

	description: table containing all the unique words and the Inverse Document Frequenct (IDF)


> TermFrequency -> < word, qid, tf >

	description: table containing the word reference form table IDF and its termfrequency in question with id=qid


------------------------------
RUNNING CELERY
------------------------------


Inorder to run the Celery workers, run the following command in the directory containing the celery app. Run as many workers as required.

For crawling:
``` celery -A define_distributed worker --loglevel=info --pool=gevent --concurrency=200 -n unique_name@%h```


For others:
``` celery -A assign02 worker --loglevel=info --pool=solo -n unique_name@%h ```

Note:
1. Every worker should have a unique name
2. Running more workers than required will result in reduced performance
3. In case of failure, empty the queue and rerun the command

_______________________________________________________________________________________________________

WORKFLOW & RESULTS
------------------------------

1. `Crawling` has been done using `StackAPI` and 4 Celery workers using celery concurrency at 200. The crawled data is written into `question.txt` and split into 4 parts for ease in computation (question_p1.txt, question_p2.txt, question_p3.txt, question_p4.txt)

2. `Cleaning` has been done using the `nltk` library support. This cleaned data from the 4 raw data files is written into their corresponding json files.

3. After setting up django and the database, the json files were loaded into the database.

4. All Celery Taks from here are defined in `tasks.py` while those of crawling and cleaning are defined in `define_distributed.py`

5. After loading the database, the unique words and their terf frequencies were calculed simultaneously, using celery.

6. Then the Inverse Document Frequency for these words was also calculated using celery.

7. After all the ranking components were calculated, the search algorithm was written.

8. The way the search algorithm works is that it recieves the result of boolean retrieval from distributed processes and then ranks them using the same.

**Test input-output case can be viewed in `Output` directory. The best search time out of 3 ran tests was 0.54 seconds.**

_______________________________________________________________________________________________________

STEPS TO RUN A SEARCH
------------------------------

> Install PostgreSQL

> Create a postgresql user with name and password as _dcassign02_ and a databset named _DcAssign02_.

> ```pg_dump -U dcassign02 -W -F t DcAssign02 < dump.sql``` (Link to database dump: https://drive.google.com/file/d/1YCEm-Eh3OCYaeAhBSOJynlrtuzG5ELdx/view?usp=sharing)

> Install RabbitMQ and Redis servers

> `pip install requirements.txt`

> `cd assign02`

> python manage.py runserver

> run celery worker in another terminal (`celery -A assign02 worker --loglevel=info --pool=solo -n worker1@%h`)

> Visit `http://127.0.0.1:8000/` on your web browser

> Enter search query