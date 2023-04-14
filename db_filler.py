import sqlite3 as sq
from db_creator import create_db


def fill_db(lesson_list):
    create_db()
    with sq.connect("lessons.db") as con:
        cur = con.cursor()
        for lesson in lesson_list:
            cur.execute(f"""
                    INSERT INTO lesson (
                                        lesson_id,
                                        student_group,
                                        teacher,
                                        subject,
                                        duration,
                                        timeslot_start,
                                        timeslot_end
                    )
                    VALUES (
                            {lesson.id},
                            '{lesson.student_group.name}',
                            '{lesson.teacher.name}',
                            '{lesson.subject}',
                            {lesson.duration},
                            {lesson.timeslot.start},
                            {lesson.timeslot.end}
                    )
            """)
