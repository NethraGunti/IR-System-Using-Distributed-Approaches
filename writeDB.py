import json
import psycopg2

count = 1

with psycopg2.connect("dbname=DcAssign02 user=dcassign02 password=dcassign02") as conn:
    with conn.cursor() as cur:
        with open('clean_p1.json') as my_file:
            data = json.load(my_file)
            cur.execute(
            """
                insert into irdc_question 
                select * from json_populate_recordset(%d::irdc_question, %s)
            """ % (count, json.dumps(data), )
            )
            count += 1

print(count)