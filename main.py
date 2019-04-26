import sys
from fetch_estekhare import *

# db = os.getcwd() + "/estexare.db"
db = "./estexare.db"
print(f"DB file: {db}")

try:
    conn = sqlite3.connect(db)
except Error as e:
    print(e)
    sys.exit(e)

cur = conn.cursor()

# create the table
create_table_query = """
    create table if not exists estexare (
        sure text,
        aye text,
        sure_no integer,
        aye_no integer,
        fi_result text,
        fi_comment text,
        fa_result text,
        fa_comment text,
        en_result text,
        en_comment text
    )
    """
cur.execute(create_table_query)

MAX_RECORDS = 610  # 302
MAX_FAILED_TRIES = 100

current_count_of_records_query = "select * from estexare"
cur.execute(current_count_of_records_query)
rows = cur.fetchall()

record_count = len(rows)
failed_tries = 0

print(f"Number of current records is {record_count}.\n\n")

check_if_aye_exists_query = """
    select * from estexare
    where sure_no = ? and aye_no = ?
    """
insert_estexare_query = """
    insert into estexare 
    (sure, aye, sure_no, aye_no, fi_result, fi_comment, fa_result, fa_comment, en_result, en_comment)
    values
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
while record_count <= MAX_RECORDS and failed_tries <= MAX_FAILED_TRIES:
    one_estexare = get_estekhare_data()

    sure_no = one_estexare['finglish']['sure_no']
    aye_no = one_estexare['finglish']['aye_no']

    cur.execute(check_if_aye_exists_query,
                (sure_no, aye_no))

    rows = cur.fetchall()
    already_exists = len(rows) > 0

    print(f"Sure No: {sure_no}")
    print(f"Aye No: {aye_no}")

    if already_exists:
        failed_tries += 1
        print("=====Already exists!\n")
        continue

    cur.execute(insert_estexare_query,
                (one_estexare['finglish']['sure'],
                 one_estexare['finglish']['aye'],
                 sure_no,
                 aye_no,
                 one_estexare['finglish']['result'],
                 one_estexare['finglish']['comment'],
                 one_estexare['farsi']['result'],
                 one_estexare['farsi']['comment'],
                 one_estexare['english']['result'],
                 one_estexare['english']['comment']))
    record_count += 1
    print(f"Record no {record_count} inserted.\n")

conn.commit()

final_count_query = "select * from estexare"
cur.execute(final_count_query)
rows = cur.fetchall()
final_count = len(rows)
print(f"Now we have {final_count} records in our DB.")
print(f"Number of already existed records have been fetched: {failed_tries}\n\n")
