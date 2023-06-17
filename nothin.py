import sqlite3 as sq

with sq.connect("lessons.db") as con:
    cur = con.cursor()
    cur.execute("""SELECT * FROM teacher""")
    result = cur.fetchall()
    for i in result:
        print(i)

# with open('teacherinfo.csv', newline='') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     teacher_list = []
#     for i, row in enumerate(reader):
#         techer_timeslot_list = list(always_timeslot_set.difference(set(map(int, row[7].split(',')))))
#         teacher_list.append(Teacher(i + 1, row[0][:15], techer_timeslot_list,
#                                     possible_years=set(map(int, row[1].split(','))),
#                                     min_lessons=int(row[2]), max_lessons=int(row[3]), max_days=int(row[4])))