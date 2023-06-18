import sqlite3 as sq
import csv

with sq.connect("lessons.db") as con:
    cur = con.cursor()
    print('Все данные перезапишутся, введите 1, если хотите перезаписать, 0 иначе')
    flag = int(input())
    if flag:
        cur.execute("""DROP TABLE IF EXISTS teacher""")

        cur.execute("""CREATE TABLE IF NOT EXISTS teacher (
           teacher_id INTEGER PRIMARY KEY,
           name TEXT,
           years TEXT,
           min_lessons INTEGER,
           max_lessons INTEGER,
           max_days INTEGER,
           non_possible_timeslots TEXT,
           wishes_sem TEXT,
           wishes_lab TEXT,
           wishes_general_group TEXT
           )""")

        with open('teacherinfo.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            teacher_list = []
            for i, row in enumerate(reader):
                cur.execute(f"""
                                    INSERT INTO teacher (
                                           name,
                                           years,
                                           min_lessons,
                                           max_lessons,
                                           max_days,
                                           non_possible_timeslots,
                                           wishes_sem,
                                           wishes_lab,
                                           wishes_general_group
                                    )
                                    VALUES (
                                            '{row[0]}',
                                            '{row[1]}',
                                            {row[2]},
                                            {row[3]},
                                            {row[4]},
                                            '{row[7]}',
                                            '{""}',
                                            '{""}',
                                            '{""}'
                                    )
                            """)