from problem_classes import Timeslot, Teacher, Lesson, TimeTable,\
    StudentGroup, studentGroup_name_list, syllabus
from constants_and_functions import *

def count_possibilities_needs(teacher_list):
    # slot_pos_list = [None] * (NUM_DAYS * PAIR_DAILY)
    # for i in range(len(slot_pos_list)):
    sem_pos = 0
    lab_pos = 0
    total_lessons_pos = 0
    for teacher in teacher_list:
        if 'sem' in teacher.lesson_list:
            sem_pos += teacher.lesson_list['sem'][1]
        if 'lab' in teacher.lesson_list:
            lab_pos += teacher.lesson_list['lab'][1]
        total_lessons_pos += teacher.max_lessons

    sem_need = 0
    lab_need = 0
    for lesson_dict_onegroup in syllabus.values():
        if 'sem' in lesson_dict_onegroup:
            sem_need += lesson_dict_onegroup['sem']
        if 'lab' in lesson_dict_onegroup:
            lab_need += lesson_dict_onegroup['lab']

    print(f"sem_pos={sem_pos}, sem_need={sem_need}")
    print(f"lab_pos={lab_pos}, lab_need={lab_need}")
    total_lessons_need = sem_need + 2 * lab_need
    print(f"total_lessons_pos={total_lessons_pos}, total_lessons_need={total_lessons_need}")




def generate_problem():
    single_timeslot_list = [Timeslot(i + 1, i + 1, 1) for i in range(NUM_DAYS * PAIR_DAILY)]
    id = NUM_DAYS * PAIR_DAILY + 1
    starts_double_lessons = [i + 1 for i in range(NUM_DAYS * PAIR_DAILY) if (i + 1) % PAIR_DAILY]
    double_timeslot_list = []
    for i in starts_double_lessons:
        double_timeslot_list.append(Timeslot(id, i, 2))
        id += 1
    timeslot_list = single_timeslot_list + double_timeslot_list
    # timeslot_list = double_timeslot_list
    # for i in double_timeslot_list:
    #     print(i)

    always_timeslot_list = list(range(1, NUM_DAYS * PAIR_DAILY + 1))
    teacher_list = [
        Teacher(1, "Aristotel", [1, 2, 3, 4, 5], lesson_list={'sem': [1, 3], 'lab': [1, 2]}, max_days=1),
        Teacher(2, "Bugulma", always_timeslot_list, lesson_list={'sem': [1, 4], 'lab': [1, 2]}, max_days=1),
        Teacher(3, "Celsius", [1, 2, 6, 7, 11, 12], lesson_list={'sem': [1, 4], 'lab': [1, 2]}),
        Teacher(4, "Decart", always_timeslot_list, lesson_list={'sem': [1, 4], 'lab': [1, 3]}),
        Teacher(5, "Euclid", always_timeslot_list, lesson_list={'sem': [1, 4], 'lab': [1, 3]}),
        Teacher(6, "Faraday", always_timeslot_list, lesson_list={'sem': [1, 4], 'lab': [1, 2]}),
        # Teacher(7, "Gelfand", [6, 7, 8, 9, 10], lesson_list={'sem': [1, 3], 'lab': [1, 2]}, max_days=1),
        # Teacher(8, "Hilbert", always_timeslot_list, lesson_list={'sem': [1, 3], 'lab': [2, 6]}),
        # Teacher(9, "Isildur", always_timeslot_list, lesson_list={'sem': [1, 4], 'lab': [1, 2]}),
    ]
    # count_possibilities_needs(teacher_list)

    studentGroup_list = [
        StudentGroup(1, studentGroup_name_list[0], [1, 2, 5, 6, 9, 10, 11]),
        StudentGroup(2, studentGroup_name_list[1], [8, 9, 11, 12, 13, 14, 15]),
        StudentGroup(3, studentGroup_name_list[2], always_timeslot_list),
        StudentGroup(4, studentGroup_name_list[3], [3, 4, 10, 11]),
        StudentGroup(5, studentGroup_name_list[4], always_timeslot_list),
        StudentGroup(6, studentGroup_name_list[5], always_timeslot_list),
        StudentGroup(7, studentGroup_name_list[6], always_timeslot_list),
        StudentGroup(8, studentGroup_name_list[7], always_timeslot_list),
        StudentGroup(9, studentGroup_name_list[8], always_timeslot_list),
        StudentGroup(10, studentGroup_name_list[9], always_timeslot_list),
        StudentGroup(11, studentGroup_name_list[10], always_timeslot_list),
        StudentGroup(12, studentGroup_name_list[11], always_timeslot_list),
    ]

    lesson_list = []
    lesson_id = 1
    for i, studentGroup in enumerate(studentGroup_list):
        studentGroup_lesson_dict = syllabus[studentGroup.name]
        for lesson_name in studentGroup_lesson_dict.keys():
            for j in range(studentGroup_lesson_dict[lesson_name]):
                if 'lab' in lesson_name:
                    lesson_list.append(Lesson(lesson_id, lesson_name, studentGroup, duration=2,
                                              possible_timeslots=double_timeslot_list))
                else:
                    lesson_list.append(Lesson(lesson_id, lesson_name, studentGroup,
                                              possible_timeslots=single_timeslot_list))
                lesson_id += 1

    count_possibilities_needs(teacher_list)

    return TimeTable(timeslot_list, lesson_list, teacher_list, studentGroup_list)
