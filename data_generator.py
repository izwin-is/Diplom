from problem_classes import Timeslot, Teacher, Lesson, TimeTable, StudentGroup
from constants_and_functions import *
import csv
import sqlite3 as sq

# studentGroup_quantity = [[9, 14, 5, 8, 8, 3], # Реальное их количество
#                          [11, 15, 6, 8, 10, 7],
#                          [0, 14, 7, 0, 0, 0]]
studentGroup_quantity = [[10, 14, 6, 9, 10, 7],
                         [12, 15, 6, 8, 10, 7],
                         [0, 14, 7, 0, 0, 0]]
# studentGroup_name_list = []
# for year in range(1, 4):
#     for faculty in range(1, 7):
#         for studentGroup_number in range(1, studentGroup_quantity[year-1][faculty-1] + 1):
#             studentGroup_name_list.append(f'{year}-{faculty}-{studentGroup_number}')
# Захардкодил, чтобы долго не считало
# studentGroup_name_list = ['1-1-1', '1-1-2', '1-1-3', '1-1-4', '1-1-5', '1-1-6', '1-1-7', '1-1-8', '1-1-9', '1-2-1',
#                           '1-2-2', '1-2-3', '1-2-4', '1-2-5', '1-2-6', '1-2-7', '1-2-8', '1-2-9', '1-2-10', '1-2-11',
#                           '1-2-12', '1-2-13', '1-2-14', '1-3-1', '1-3-2', '1-3-3', '1-3-4', '1-3-5', '1-4-1', '1-4-2',
#                           '1-4-3', '1-4-4', '1-4-5', '1-4-6', '1-4-7', '1-4-8', '1-5-1', '1-5-2', '1-5-3', '1-5-4',
#                           '1-5-5', '1-5-6', '1-5-7', '1-5-8', '1-6-1', '1-6-2', '1-6-3', '2-1-1', '2-1-2', '2-1-3',
#                           '2-1-4', '2-1-5', '2-1-6', '2-1-7', '2-1-8', '2-1-9', '2-1-10', '2-1-11', '2-2-1', '2-2-2',
#                           '2-2-3', '2-2-4', '2-2-5', '2-2-6', '2-2-7', '2-2-8', '2-2-9', '2-2-10', '2-2-11', '2-2-12',
#                           '2-2-13', '2-2-14', '2-2-15', '2-3-1', '2-3-2', '2-3-3', '2-3-4', '2-3-5', '2-3-6', '2-4-1',
#                           '2-4-2', '2-4-3', '2-4-4', '2-4-5', '2-4-6', '2-4-7', '2-4-8', '2-5-1', '2-5-2', '2-5-3',
#                           '2-5-4', '2-5-5', '2-5-6', '2-5-7', '2-5-8', '2-5-9', '2-5-10', '2-6-1', '2-6-2', '2-6-3',
#                           '2-6-4', '2-6-5', '2-6-6', '2-6-7', '3-2-1', '3-2-2', '3-2-3', '3-2-4', '3-2-5', '3-2-6',
#                           '3-2-7', '3-2-8', '3-2-9', '3-2-10', '3-2-11', '3-2-12', '3-2-13', '3-2-14', '3-3-1', '3-3-2',
#                           '3-3-3', '3-3-4', '3-3-5', '3-3-6', '3-3-7']
studentGroup_name_list = ['1-1-1', '1-1-2', '1-1-3', '1-1-4', '1-1-5', '1-1-6', '1-1-7', '1-1-8', '1-1-9', '1-1-10',
                          '1-2-1', '1-2-2', '1-2-3', '1-2-4', '1-2-5', '1-2-6', '1-2-7', '1-2-8', '1-2-9', '1-2-10',
                          '1-2-11', '1-2-12', '1-2-13', '1-2-14', '1-3-1', '1-3-2', '1-3-3', '1-3-4', '1-3-5', '1-3-6',
                          '1-4-1', '1-4-2', '1-4-3', '1-4-4', '1-4-5', '1-4-6', '1-4-7', '1-4-8', '1-4-9', '1-5-1',
                          '1-5-2', '1-5-3', '1-5-4', '1-5-5', '1-5-6', '1-5-7', '1-5-8', '1-5-9', '1-5-10', '1-6-1',
                          '1-6-2', '1-6-3', '1-6-4', '1-6-5', '1-6-6', '1-6-7', '2-1-1', '2-1-2', '2-1-3', '2-1-4',
                          '2-1-5', '2-1-6', '2-1-7', '2-1-8', '2-1-9', '2-1-10', '2-1-11', '2-1-12', '2-2-1', '2-2-2',
                          '2-2-3', '2-2-4', '2-2-5', '2-2-6', '2-2-7', '2-2-8', '2-2-9', '2-2-10', '2-2-11', '2-2-12',
                          '2-2-13', '2-2-14', '2-2-15', '2-3-1', '2-3-2', '2-3-3', '2-3-4', '2-3-5', '2-3-6', '2-4-1',
                          '2-4-2', '2-4-3', '2-4-4', '2-4-5', '2-4-6', '2-4-7', '2-4-8', '2-5-1', '2-5-2', '2-5-3',
                          '2-5-4', '2-5-5', '2-5-6', '2-5-7', '2-5-8', '2-5-9', '2-5-10', '2-6-1', '2-6-2', '2-6-3',
                          '2-6-4', '2-6-5', '2-6-6', '2-6-7', '3-2-1', '3-2-2', '3-2-3', '3-2-4', '3-2-5', '3-2-6',
                          '3-2-7', '3-2-8', '3-2-9', '3-2-10', '3-2-11', '3-2-12', '3-2-13', '3-2-14', '3-3-1', '3-3-2',
                          '3-3-3', '3-3-4', '3-3-5', '3-3-6', '3-3-7']
always_timeslot_list = list(range(1, NUM_DAYS * PAIR_DAILY + 1))
always_timeslot_set = set(always_timeslot_list)


def create_timeslot_list():
    single_timeslot_list = [Timeslot(i + 1, i + 1, 1) for i in range(NUM_DAYS * PAIR_DAILY)]
    id = NUM_DAYS * PAIR_DAILY + 1
    starts_double_lessons = [i + 1 for i in range(NUM_DAYS * PAIR_DAILY) if (i + 1) % PAIR_DAILY]
    double_timeslot_list = []
    for i in starts_double_lessons:
        double_timeslot_list.append(Timeslot(id, i, 2))
        id += 1
    return single_timeslot_list, double_timeslot_list


def create_teacher_list():
    with sq.connect("lessons.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT * FROM teacher""")
        result = cur.fetchall()
        teacher_list = []
        for teacher in result:
            teacher_timeslot_list = list(always_timeslot_set.difference(set(map(int, teacher[6].split(',')))))
            teacher_list.append(Teacher(teacher[0], teacher[1][:15], teacher_timeslot_list,
                                        possible_years=set(map(int, teacher[2].split(','))),
                                        min_lessons=teacher[3], max_lessons=teacher[4], max_days=teacher[5]))
    return teacher_list


def create_studentGroup_list():
    return [StudentGroup(i + 1, name, always_timeslot_list, int(name[0]))
            for i, name in enumerate(studentGroup_name_list)]


def find_studentGroup_by_name(lesson_student_group_name, studentGroup_list):
    for studentGroup in studentGroup_list:
        if lesson_student_group_name == studentGroup.name:
            return studentGroup


def find_timeslot_by_start(start, timeslot_list):
    for timeslot in timeslot_list:
        if timeslot.start == start:
            return timeslot

def find_teacher_by_id(teacher_id, teacher_list):
    for teacher in teacher_list:
        if teacher.id == teacher_id:
            return teacher

def generate_problem_with_initial_solution():
    single_timeslot_list, double_timeslot_list = create_timeslot_list()
    timeslot_list = single_timeslot_list + double_timeslot_list
    teacher_list = create_teacher_list()
    studentGroup_list = create_studentGroup_list()

    teacher_to_year_1_list = [teacher for teacher in teacher_list if 1 in teacher.possible_years]
    teacher_to_year_2_list = [teacher for teacher in teacher_list if 2 in teacher.possible_years]
    teacher_to_year_3_list = [teacher for teacher in teacher_list if 3 in teacher.possible_years]
    teacher_to_year_list = [teacher_to_year_1_list, teacher_to_year_2_list, teacher_to_year_3_list]

    with sq.connect("lessons.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT * FROM lesson""")
        lesson_db_list = cur.fetchall()
        lesson_list = [None] * len(lesson_db_list)
        for lesson_index in range(len(lesson_db_list)):
            lesson_id = lesson_db_list[lesson_index][0]
            lesson_subject = lesson_db_list[lesson_index][3]
            lesson_student_group_name = lesson_db_list[lesson_index][1]
            studentGroup = find_studentGroup_by_name(lesson_student_group_name, studentGroup_list)
            lesson_teacher = find_teacher_by_id(lesson_db_list[lesson_index][2], teacher_list)
            if lesson_subject == 'sem':
                lesson_timeslot = find_timeslot_by_start(lesson_db_list[lesson_index][5], single_timeslot_list)
                lesson_list[lesson_index] = Lesson(lesson_id,
                                                   'sem',
                                                   studentGroup,
                                                   duration=1,
                                                   possible_timeslots=single_timeslot_list,
                                                   possible_teacher_list=teacher_to_year_list[studentGroup.year - 1],
                                                   timeslot=lesson_timeslot,
                                                   teacher=lesson_teacher
                                                   )
            else:
                lesson_timeslot = find_timeslot_by_start(lesson_db_list[lesson_index][5], double_timeslot_list)
                lesson_list[lesson_index] = Lesson(lesson_id,
                                                   'lab',
                                                   studentGroup,
                                                   duration=2,
                                                   possible_timeslots=single_timeslot_list,
                                                   possible_teacher_list=teacher_to_year_list[studentGroup.year - 1],
                                                   timeslot=lesson_timeslot,
                                                   teacher=lesson_teacher
                                                   )
    return TimeTable(timeslot_list, lesson_list, teacher_list, studentGroup_list)


def generate_problem():
    single_timeslot_list, double_timeslot_list = create_timeslot_list()
    timeslot_list = single_timeslot_list + double_timeslot_list
    teacher_list = create_teacher_list()
    studentGroup_list = create_studentGroup_list()

    teacher_to_year_1_list = [teacher for teacher in teacher_list if 1 in teacher.possible_years]
    teacher_to_year_2_list = [teacher for teacher in teacher_list if 2 in teacher.possible_years]
    teacher_to_year_3_list = [teacher for teacher in teacher_list if 3 in teacher.possible_years]
    teacher_to_year_list = [teacher_to_year_1_list, teacher_to_year_2_list, teacher_to_year_3_list]

    lesson_sem_list = [Lesson(i + 1,
                              'sem',
                              studentGroup,
                              possible_timeslots=single_timeslot_list,
                              possible_teacher_list=teacher_to_year_list[studentGroup.year - 1]
                              )
                       for i, studentGroup in enumerate(studentGroup_list)]
    lesson_lab_list_1 = [Lesson(i + 1 + len(lesson_sem_list),
                                'lab',
                                studentGroup,
                                duration=2,
                                possible_timeslots=double_timeslot_list,
                                possible_teacher_list=teacher_to_year_list[studentGroup.year - 1]
                                )
                         for i, studentGroup in enumerate(studentGroup_list)]

    lesson_lab_list_2 = [Lesson(i + 1 + len(lesson_sem_list) + len(lesson_lab_list_1),
                                'lab',
                                studentGroup,
                                duration=2,
                                possible_timeslots=double_timeslot_list,
                                possible_teacher_list=teacher_to_year_list[studentGroup.year - 1]
                                )
                         for i, studentGroup in enumerate(studentGroup_list)]
    lesson_list = lesson_sem_list + lesson_lab_list_1 + lesson_lab_list_2

    return TimeTable(timeslot_list, lesson_list, teacher_list, studentGroup_list)
