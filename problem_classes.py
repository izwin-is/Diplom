from optapy import problem_fact, planning_id
from optapy import planning_entity, planning_variable

from optapy import planning_solution, planning_entity_collection_property, \
                   problem_fact_collection_property, \
                   value_range_provider, planning_score
from optapy.score import HardSoftScore

PAIR_DAILY = 4
NUM_DAYS = 3
WEEK = ['MON', 'TUE', 'WED']
studentGroup_name_list = ["Б01-901", "Б02-902", "Б03-903", "Б04-904", "Б05-905",
                          "Б06-906", "Б07-907", "Б08-908", "Б09-909"]
syllabus = {
    "Б01-901": {"sem":1, "lab": 1},
    "Б02-902": {"sem":1, "lab": 1},
    "Б03-903": {"sem":1, "lab": 1},
    "Б04-904": {"sem":1, "lab": 1},
    "Б05-905": {"sem":1, "lab": 1},
    "Б06-906": {"sem":1, "lab": 1},
    "Б07-907": {"sem":1, "lab": 1},
    "Б08-908": {"sem":2, "lab": 2},
    "Б09-909": {"sem":4, "lab": 2}
}

def calculate_week_day(slot_id):
    return WEEK[(slot_id - 1) // PAIR_DAILY]
def calculate_lesson_num(slot_id):
    return (slot_id - 1) % PAIR_DAILY + 1
@problem_fact
class Teacher:
    def __init__(self, id, name, slots, lesson_list=None, min_lessons=3, max_lessons=6, max_days=2):
        self.id = id
        self.name = name
        self.slots = slots
        self.lesson_list = lesson_list
        self.max_days = max_days
        self.min_lessons = min_lessons
        self.max_lessons = max_lessons

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return f"{self.id}.{self.name}"

@problem_fact
class StudentGroup:
    def __init__(self, id, name, slots, lesson_list=None):
        self.id = id
        self.name = name
        self.slots = slots
        self.lesson_list = lesson_list

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return f"{self.id}.{self.name}"


@problem_fact
class Timeslot:
    def __init__(self, id):
        self.id = id
        self.week_day = calculate_week_day(id)
        self.lesson_num = calculate_lesson_num(id)

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return f"Timeslot({self.id})"


@planning_entity
class Lesson:
    def __init__(self, id, subject, student_group, timeslot=None, teacher=None):
        self.id = id
        self.subject = subject
        self.teacher = teacher
        self.student_group = student_group
        self.timeslot = timeslot
        self.a = 1

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

    @planning_variable(Timeslot, ["timeslotRange"])
    def get_timeslot(self):
        return self.timeslot

    def set_timeslot(self, new_timeslot):
        self.timeslot = new_timeslot
        # self.a += 1


    @planning_variable(Teacher, ["teacherRange"])
    def get_teacher(self):
        return self.teacher

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
               f"teacher={self.teacher})"
        # return f"""cur.execute("INSERT INTO lessons VALUES ({self.student_group.id}, '{self.subject}', {self.teacher.id})")"""

def format_list(a_list):
    return '\n'.join(map(str, a_list))

def print_total_x(line, x=19):
    line = str(line)
    print(f"{line}{' ' * (x - len(line))}", end='')

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

    def __str__(self):

        self.teacher_list.sort(key=lambda teacher: teacher.id)
        self.timeslot_list.sort(key=lambda timeslot: timeslot.id)
        teacher_id_list = [teacher.id for teacher in self.teacher_list]
        timeslot_id_list = [timeslot.id for timeslot in self.timeslot_list]
        self.lesson_list.sort(key=lambda lesson: (lesson.timeslot.id, lesson.teacher.id))
        print_total_x('')
        for teacher in self.teacher_list:
            print_total_x(teacher.name)
        print()
        # print(teacher_id_list)
        # print(timeslot_id_list)
        lesson_index = 0
        for timeslot_id in timeslot_id_list:
            print_total_x(f"{timeslot_id}:{calculate_week_day(timeslot_id)}:{calculate_lesson_num(timeslot_id)}")
            for teacher_id in teacher_id_list:
                if lesson_index == len(self.lesson_list):
                    break
                elif self.lesson_list[lesson_index].teacher.id != teacher_id or \
                     self.lesson_list[lesson_index].timeslot.id != timeslot_id:
                    print_total_x('')
                else:
                    print_total_x(f"{self.lesson_list[lesson_index].student_group}."
                                  f"{self.lesson_list[lesson_index].subject}")
                    lesson_index += 1
            print()

        return f"{format_list(self.lesson_list)}\n"\
               f"score={str(self.score.toString()) if self.score is not None else 'None'}"

