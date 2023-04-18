from constants_and_functions import *

class Teacher:
    def __init__(self, id, name, slots, lesson_list=None, min_lessons=4, max_lessons=10, max_days=2):
        self.id = id
        self.name = name
        self.slots = slots
        self.lesson_list = lesson_list
        self.max_days = max_days
        self.min_lessons = min_lessons
        self.max_lessons = min(max_lessons, len(slots), max_days * PAIR_DAILY)
        self.slots_set = set(slots)
        max_lessons_from_lesson_list = 0
        for subject in lesson_list.keys():
            if 'lab' in lesson_list[subject]:
                max_lessons_from_lesson_list += 2 * lesson_list[subject][1]
            else:
                max_lessons_from_lesson_list += lesson_list[subject][1]
        self.max_lessons = min(self.max_lessons, max_lessons_from_lesson_list)


always_timeslot_list = list(range(1, NUM_DAYS * PAIR_DAILY + 1))
a = Teacher(1, "Aristotel", always_timeslot_list, lesson_list={'sem': [1, 3], 'lab': [1, 2]})
print(a.max_lessons)