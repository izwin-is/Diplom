from problem_classes import Timeslot, Teacher, Lesson, TimeTable, StudentGroup


# def generate_problem():
#     timeslot_list = [
#         Timeslot(1),
#         Timeslot(2),
#         Timeslot(3)
#     ]
#     teacher_list = [
#         Teacher(1, "Aleskerov", [1, 2]),
#         Teacher(2, "Bugulma", [2, 3]),
#         Teacher(3, "Celsius", [1, 3])
#     ]
#     studentGroup_list = [
#         StudentGroup(1, "Б01-901", [1, 3]),
#         StudentGroup(2, "Б02-902", [2, 3]),
#         StudentGroup(3, "Б03-903", [1, 2])
#     ]
#     lesson_list = [
#         Lesson(1, "Physics", studentGroup_list[0]),
#         Lesson(2, "Physics", studentGroup_list[0]),
#         Lesson(3, "Physics", studentGroup_list[1]),
#         Lesson(4, "Physics", studentGroup_list[1]),
#         Lesson(5, "Physics", studentGroup_list[2]),
#         Lesson(6, "Physics", studentGroup_list[2])
#     ]

def generate_problem():
    timeslot_list = [
        Timeslot(1),
        Timeslot(2),
        Timeslot(3),
        Timeslot(4),
        Timeslot(5),
        Timeslot(6),
        Timeslot(7),
        Timeslot(8),
        Timeslot(9)

    ]
    teacher_list = [
        Teacher(1, "Aristotel", [1, 2, 3, 7, 8, 9], max_days=1, max_lessons=3),
        Teacher(2, "Bugulma", [2, 3, 4, 5], max_days=1, max_lessons=3),
        Teacher(3, "Celsius", list(range(1, 10)), max_days=1, max_lessons=3),
        Teacher(4, "Decart", list(range(1, 10)), max_days=2, max_lessons=4),
        Teacher(5, "Euclid", list(range(1, 10)), max_days=1, max_lessons=3),
    ]
    studentGroup_list = [
        StudentGroup(1, "Б01-901", list(range(1, 10))),
        StudentGroup(2, "Б02-902", list(range(1, 10))),
        StudentGroup(3, "Б03-903", list(range(1, 10))),
        StudentGroup(4, "Б04-904", list(range(1, 10))),
        StudentGroup(5, "Б05-905", list(range(1, 10))),
        StudentGroup(6, "Б06-906", list(range(1, 10))),
        StudentGroup(7, "Б07-907", [4, 9]),
        StudentGroup(8, "Б08-908", [9]),
        StudentGroup(9, "Б09-909", [9])
    ]
    lesson_list = [
        Lesson(1, "Physics", studentGroup_list[0]),
        Lesson(2, "Physics", studentGroup_list[0]),
        Lesson(3, "Physics", studentGroup_list[1]),
        Lesson(4, "Physics", studentGroup_list[1]),
        Lesson(5, "Physics", studentGroup_list[2]),
        Lesson(6, "Physics", studentGroup_list[2]),
        Lesson(7, "Physics", studentGroup_list[3]),
        Lesson(8, "Physics", studentGroup_list[4]),
        Lesson(9, "Physics", studentGroup_list[4]),
        Lesson(10, "Physics", studentGroup_list[5]),
        Lesson(11, "Physics", studentGroup_list[5]),
        Lesson(12, "Physics", studentGroup_list[6]),
        Lesson(13, "Physics", studentGroup_list[6]),
        Lesson(14, "Physics", studentGroup_list[7]),
        Lesson(15, "Physics", studentGroup_list[8]),
    ]

    return TimeTable(timeslot_list, lesson_list, teacher_list, studentGroup_list)