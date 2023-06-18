from optapy import problem_fact, planning_id
from optapy import planning_entity, planning_variable

from optapy import planning_solution, planning_entity_collection_property, \
                   problem_fact_collection_property, \
                   value_range_provider, planning_score
from optapy.score import HardSoftScore
from db_filler import fill_db
from show_timetable import show_timetable
from constants_and_functions import *



@problem_fact
class Teacher:
    def __init__(self, id, name, slots, lesson_list=None, possible_years={1, 2, 3},
                 min_lessons=4, max_lessons=10, max_days=2, sem_wishes=None, lab_wishes=None):
        self.id = id
        self.name = name
        self.slots = slots
        self.lesson_list = lesson_list
        self.possible_years = possible_years
        self.max_days = max_days
        self.min_lessons = min_lessons
        self.max_lessons = min(max_lessons, len(slots), max_days * PAIR_DAILY)
        self.slots_set = set(slots)
        self.sem_wishes = sem_wishes
        self.lab_wishes = lab_wishes
        if sem_wishes:
            self.sem_wishes = set(sem_wishes)
        else:
            self.sem_wishes = None
        if lab_wishes:
            self.lab_wishes = set(lab_wishes)
        else:
            self.lab_wishes = None
        self.any_wishes = bool(sem_wishes) or bool(lab_wishes)
        # max_lessons_from_lesson_list = 0
        # for subject in lesson_list.keys():
        #     if 'lab' in subject:
        #         max_lessons_from_lesson_list += 2 * lesson_list[subject][1]
        #     else:
        #         max_lessons_from_lesson_list += lesson_list[subject][1]
        # self.max_lessons = min(self.max_lessons, max_lessons_from_lesson_list)

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return f"{self.id}.{self.name}"

@problem_fact
class StudentGroup:
    def __init__(self, id, name, slots, year, lesson_list=None):
        self.id = id
        self.name = name
        self.slots = slots
        self.year = year
        self.lesson_list = lesson_list
        self.slots_set = set(slots)

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return f"{self.id}.{self.name}"


@problem_fact
class Timeslot:
    def __init__(self, id, start, duration):
        self.id = id
        self.start = start
        self.duration = duration
        self.end = start + duration - 1
        self.week_day = calculate_week_day(start)
        self.lesson_num = calculate_lesson_num(start)
        self.start_end_set = {self.start, self.end}

    @planning_id
    def get_id(self):
        return self.id

    def start_end_set(self):
        return {self.start, self.end}

    def __str__(self):
        return f"Timeslot({self.id}:{self.start}-{self.end})"


@planning_entity
class Lesson:
    def __init__(self, id, subject, student_group, duration=1, possible_timeslots=None, timeslot=None, teacher=None, possible_teacher_list=None):
        self.id = id
        self.subject = subject
        self.teacher = teacher
        self.student_group = student_group
        self.timeslot = timeslot
        self.duration = duration
        self.possible_timeslots = possible_timeslots
        self.possible_teacher_list = possible_teacher_list

    # def refresh(self):
    #     try:
    #         self.week_day = calculate_week_day(self.timeslot.id)
    #         self.lesson_num = calculate_lesson_num(self.timeslot.id)
    #     except: pass

    # def __setattr__(self, key, value):
    #     if key == 'timeslot':
    #         print(1)

    @planning_id
    def get_id(self):
        return self.id

    @planning_variable(Timeslot, value_range_provider_refs=["timeslotPosRange"])
    def get_timeslot(self):
        return self.timeslot

    @value_range_provider(range_id="timeslotPosRange", value_range_type=Timeslot)
    def get_possible_timeslot_list(self):
        return self.possible_timeslots

    def set_timeslot(self, new_timeslot):
        self.timeslot = new_timeslot


    @planning_variable(Teacher, value_range_provider_refs=["teacherPosRange"])
    def get_teacher(self):
        return self.teacher

    @value_range_provider(range_id="teacherPosRange", value_range_type=Teacher)
    def get_possible_teacher_list(self):
        return self.possible_teacher_list


    def set_teacher(self, new_teacher):
        self.teacher = new_teacher

    # @planning_variable(StudentGroup, ["studentGroupRange"])
    # def get_studentGroup(self):
    #     return self.studentGroup
    #
    # def set_studentGroup(self, new_studentGroup):
    #     self.studentGroup = new_studentGroup

    def __str__(self):
        return f"Lesson(id={self.id}, " \
               f"{self.timeslot}, " \
               f"student_group={self.student_group}, " \
               f"subject={self.subject}, " \
               f"teacher={self.teacher}, " \
               f"duration={self.duration})"
        # return f"""cur.execute("INSERT INTO lessons VALUES ({self.student_group.id}, '{self.subject}', {self.teacher.id})")"""

def format_list(a_list):
    return '\n'.join(map(str, a_list))



@planning_solution
class TimeTable:
    def __init__(self, timeslot_list, lesson_list, teacher_list, studentGroup_list, score=None):
        self.timeslot_list = timeslot_list
        self.teacher_list = teacher_list
        self.lesson_list = lesson_list
        self.studentGroup_list = studentGroup_list
        self.score = score

    @problem_fact_collection_property(Timeslot)
    @value_range_provider("timeslotRange")
    def get_timeslot_list(self):
        return self.timeslot_list

    @problem_fact_collection_property(Teacher)
    @value_range_provider("teacherRange")
    def get_teacher_list(self):
        return self.teacher_list

    @problem_fact_collection_property(StudentGroup)
    @value_range_provider("studentGroupRange")
    def get_studentGroup_list(self):
        return self.studentGroup_list

    @planning_entity_collection_property(Lesson)
    def get_lesson_list(self):
        return self.lesson_list

    @planning_score(HardSoftScore)
    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score


    def write_to_db(self):
        fill_db(self.lesson_list)
    def __str__(self):

        fill_db(self.lesson_list)
        show_timetable()
        # return f"{format_list(self.lesson_list)}\n"\
        #        f"score={str(self.score.toString()) if self.score is not None else 'None'}"
        return f"score={str(self.score.toString()) if self.score is not None else 'None'}"



