from optapy import problem_fact, planning_id
from optapy import planning_entity, planning_variable

week_days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
times = ['1', '2', '3', '4', '5', '6', '7']


def slots_to_table(slots):
    string = ''
    for slot in slots:
        string += f'{week_days[slot // 7]}: {times[slot % 7]}\n'
    return string


def get_day_name(slot):
    return week_days[slot // 7]


def get_lesson_number(slot):
    return times[slot % 7]


# @problem_fact
# class Teacher:
#     def __init__(self, id, name, slots):
#         self.id = id
#         self.name = name
#         self.slots = slots
#
#     @planning_id
#     def get_id(self):
#         return self.id
#
#     def __str__(self):
#         return f"{self.id}. {self.name}\n"
#
#
# @problem_fact
# class Group:
#     def __init__(self, id, name, slots):
#         self.id = id
#         self.name = name
#         self.slots = slots
#
#     @planning_id
#     def get_id(self):
#         return self.id
#
#     def __str__(self):
#         return f"{self.id}. {self.name}\n"


@problem_fact
class Timeslot:
    def __init__(self, id, slot_num):
        self.id = id
        self.slot_num = slot_num

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return (
            f"Timeslot("
            f"id={self.id}, "
            f"day_of_week={get_day_name(self.slot)}, "
            f"end_time={get_lesson_number(self.slot)})"
        )


@planning_entity
class Lesson:
    def __init__(self, id, subject, teacher, student_group, timeslot=None):
        self.id = id
        self.subject = subject
        self.teacher = teacher
        self.student_group = student_group
        self.timeslot = timeslot

    @planning_id
    def get_id(self):
        return self.id

    @planning_variable(Timeslot, ["timeslotRange"])
    def get_timeslot(self):
        return self.timeslot

    def set_timeslot(self, new_timeslot):
        self.timeslot = new_timeslot


    def __str__(self):
        return (
            f"Lesson("
            f"id={self.id}, "
            f"timeslot={self.timeslot}, "
            f"teacher={self.teacher}, "
            f"subject={self.subject}, "
            f"student_group={self.student_group}"
            f")"
        )


from optapy import planning_solution, planning_entity_collection_property, \
                   problem_fact_collection_property, \
                   value_range_provider, planning_score
from optapy.score import HardSoftScore

def format_list(a_list):
    return ',\n'.join(map(str, a_list))

@planning_solution
class TimeTable:
    def __init__(self, timeslot_list, lesson_list, score=None):
        self.timeslot_list = timeslot_list
        self.lesson_list = lesson_list
        self.score = score

    @problem_fact_collection_property(Timeslot)
    @value_range_provider("timeslotRange")
    def get_timeslot_list(self):
        return self.timeslot_list


    @planning_entity_collection_property(Lesson)
    def get_lesson_list(self):
        return self.lesson_list

    @planning_score(HardSoftScore)
    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def __str__(self):
        return (
            f"TimeTable("
            f"timeslot_list={format_list(self.timeslot_list)},\n"
            f"lesson_list={format_list(self.lesson_list)},\n"
            f"score={str(self.score.toString()) if self.score is not None else 'None'}"
            f")"
        )