import time
from celery.result import ResultBase
from define_ditributed import _crawlSAPI


# Z = 36
TAG = 'python'
# COUNT = 8400*Z
COUNT = 305700
TASKS = []
FINAL_TASKS = []
count = 0
workers = 0
start_time = time.time()

set1 = _crawlSAPI.delay(
    tag=TAG,
    start=count+1,
    end=count + 3    
)
TASKS.append(set1)
count += 3
workers += 1

while count < COUNT//100:
    TASKS.append(_crawlSAPI.apply_async(args=[TAG,count+1,count + 3]))
    count += 3
    workers += 1

for i in range(workers):
    TASKS[i] = TASKS[i].wait(timeout=None, interval=0.5)
    FINAL_TASKS.extend(set([tuple(l) for l in TASKS[i]]))
FINAL_TASKS = set(FINAL_TASKS)

if FINAL_TASKS!=[]:
    fq = open('questions.txt', "a")
    for i in FINAL_TASKS:
        fq.write(i[0]+"\n"+i[1]+"\n")
    fq.close()

end_time = time.time() - start_time
print('Successfully crawled {} questions in {} seconds seconds using {} processes'.format(COUNT*100, end_time, workers))