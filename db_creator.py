import sqlite3 as sq

def create_db():
    with sq.connect("lessons.db") as con:
        cur = con.cursor()
        cur.execute("""DROP TABLE IF EXISTS lesson""")

        cur.execute("""CREATE TABLE IF NOT EXISTS lesson (
        lesson_id INTEGER PRIMARY KEY,
        student_group TEXT,
        teacher_id INTEGER,
        subject TEXT,
        duration INTEGER DEFAULT 1,
        timeslot_start INTEGER,
        timeslot_end INTEGER,
        week_day TEXT
        )""")