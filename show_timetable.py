import sqlite3 as sq
from constants_and_functions import *

def print_total_x(line, x=19):
    line = str(line)
    print(f"{line}{' ' * (x - len(line))}", end='')

def print_timetable(teachers_lessons):
    teacher_name_list = teachers_lessons.keys()
    print_total_x('')
    for name in teacher_name_list:
        print_total_x(name)
    print()
    for timeslot in range(1, NUM_DAYS * PAIR_DAILY + 1):
        print_total_x(f'{timeslot}:{calculate_week_day(timeslot)}:{calculate_lesson_num(timeslot)}')
        for name in teacher_name_list:
            if timeslot in teachers_lessons[name]:
                print_total_x(teachers_lessons[name][timeslot])
            else:
                print_total_x('')
        print()


def show_timetable():
    with sq.connect("lessons.db") as con:
        cur = con.cursor()
        cur.execute("SELECT DISTINCT teacher FROM lesson ORDER BY teacher")
        teachers_lessons = dict([(i[0], {}) for i in cur.fetchall()])
        for teacher_name in teachers_lessons.keys():
            cur.execute(f"SELECT * FROM lesson WHERE teacher == '{teacher_name}' AND duration == 1")
            one_timeslot_lesson_list = cur.fetchall()
            for lesson in one_timeslot_lesson_list:
                teachers_lessons[teacher_name][lesson[5]] = f"{lesson[1]}:{lesson[3]}"
            cur.execute(f"SELECT * FROM lesson WHERE teacher == '{teacher_name}' AND duration == 2")
            two_timeslot_lesson_list = cur.fetchall()
            for lesson in two_timeslot_lesson_list:
                teachers_lessons[teacher_name][lesson[5]] = f"{lesson[1]}:{lesson[3]}"
                teachers_lessons[teacher_name][lesson[5] + 1] = f"{lesson[1]}:{lesson[3]}"

        print_timetable(teachers_lessons)

if __name__=='__main__':
    show_timetable()