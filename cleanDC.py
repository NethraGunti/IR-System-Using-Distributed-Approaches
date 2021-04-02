import time
import json
from celery.result import ResultBase
from define_ditributed import _clean_and_tokenise

question_files = ['1', '2', '3', '4']
TASKS = []

start_time = time.time()

for f in question_files:
    start_sub = time.time()

    read_file = open('questions_p{}.txt'.format(f), "r")
    current_file = read_file.readlines()
    N = len(current_file)
    DUMP = []
    for i in range(0,N-1,2):
        TASKS.append(_clean_and_tokenise.apply_async(
            args=[current_file[i].strip("\n")]
            )
        )
    for i in range(0, N//2):
        try:
            TASKS[i] = TASKS[i].wait(timeout=None, interval=0.5)
        except AttributeError as e:
            print(e)
            print(TASKS[i])
            exit()
        #TASKS NOW HAS CLEANED AND TOKENISED SENTENCE i
        
        DUMP.append(
            {
                'link' : current_file[(2*i)+1].strip("\n"),
                'original' : current_file[2*i].strip("\n"),
                'clean' : TASKS[i].strip("\n")
            }
        )
    read_file.close()

    DUMP = json.dumps(DUMP)
    with open("clean_p{}.json".format(f), "w") as outfile:
        outfile.write(DUMP)
    
    end_sub = time.time() - start_sub
    print('questions_p{}.txt cleaned in {} seconds'.format(f, str(end_sub)))


end_time = time.time() - start_time
print('Data Cleaning Completed in {} seconds'.format(str(end_time)))