from problem_classes import Lesson, Teacher, StudentGroup, calculate_week_day
from optapy import constraint_provider
from optapy.constraint import Joiners, ConstraintFactory
from optapy.constraint import ConstraintCollectors
from optapy.score import HardSoftScore

def fall_in_interval(args):
    if isinstance(args, int):
        return 0
    count, min_lessons, max_lessons = args
    if count < min_lessons:
        return min_lessons - count
    if count > max_lessons:
        return count - max_lessons
    return 0

def positive_score(x):
    if x < 0:
        return 0
    return x

@constraint_provider
def define_constraints(constraint_factory):
    return [
        # Hard constraints
        teacher_conflict(constraint_factory),
        student_group_conflict(constraint_factory),
        # teacher_timing(constraint_factory),
        # lab_duration(constraint_factory),
        # student_group_timing(constraint_factory),
        # teacher_max_lessons_total(constraint_factory),
        # one_teacher_to_group(constraint_factory),
        # lab_start_end(constraint_factory)
        # Soft constraints
        # teacher_max_days(constraint_factory),
        # teacher_min_max_lessons_total(constraint_factory),
        # teacher_min_max_lessons_particular(constraint_factory),
        
        # teacher_min_lessons_total(constraint_factory),
    ]

def one_teacher_to_group(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
            .group_by(lambda lesson: lesson.student_group,
                      lambda lesson: lesson.subject,
                      ConstraintCollectors.count_distinct()) \
            .penalize("More than one teacher to one group",
                      HardSoftScore.ONE_HARD,
                      lambda group, subject, count: positive_score(count - 1))


# Работает правильно, но алгоритм плохо оптимизируется
def teacher_min_max_lessons_total(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
            .group_by(lambda lesson: lesson.teacher,
                      ConstraintCollectors.count()) \
            .penalize("Too many or too few lessons for teacher",
                      HardSoftScore.ONE_SOFT,
                      lambda teacher, count: positive_score(-min(teacher.max_lessons - count,
                                                                 count - teacher.min_lessons)))


def teacher_max_lessons_total(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
            .group_by(lambda lesson: lesson.teacher,
                      ConstraintCollectors.count()) \
            .filter(lambda teacher, count: count - teacher.max_lessons > 0) \
            .penalize("Too many lessons for teacher",
                      HardSoftScore.ONE_HARD,
                      lambda teacher, count: count)


def teacher_min_lessons_total(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
            .group_by(lambda lesson: lesson.teacher,
                      ConstraintCollectors.count()) \
            .filter(lambda teacher, count: teacher.min_lessons - count > 0) \
            .penalize("Too few lessons for teacher",
                      HardSoftScore.ONE_HARD,
                      lambda teacher, count: count)


def teacher_max_days(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
            .group_by(lambda lesson: lesson.teacher,
                      lambda lesson: lesson.timeslot.week_day,
                      ConstraintCollectors.count()) \
            .group_by(lambda teacher, days, count: teacher,
                      ConstraintCollectors.countTri()) \
            .penalize("",
                      HardSoftScore.ONE_SOFT,
                      lambda teacher, count: 3 * positive_score(count - teacher.max_days))


def teacher_timing(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Teacher) \
            .join(Lesson,
                  Joiners.equal(lambda teacher: teacher.id,
                                lambda lesson: lesson.teacher.id)) \
            .filter(lambda teacher, lesson: lesson.timeslot.id not in teacher.slots) \
            .penalize("Teacher is busy", HardSoftScore.ONE_HARD)



def student_group_timing(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(StudentGroup) \
            .join(Lesson,
                  Joiners.equal(lambda student_group: student_group.id,
                                lambda lesson: lesson.student_group.id)) \
            .filter(lambda student_group, lesson: lesson.timeslot.id not in student_group.slots) \
            .penalize("Student Group is busy", HardSoftScore.ONE_HARD)



def lab_duration(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
            .filter(lambda lesson: lesson.duration == 2) \
            .filter(lambda lesson: lesson.timeslot.duration != 2) \
            .penalize("Lab duration", HardSoftScore.ONE_HARD)


def timeslots_intersection(lesson_list):
    sum_set_len = 0
    timeslot_set = set()
    for lesson in lesson_list:
        one_timeslot_set = lesson.timeslot.start_end_set()
        sum_set_len += len(one_timeslot_set)
        timeslot_set = timeslot_set.union(one_timeslot_set)
    # print(sum_set_len - len(timeslot_set))
    return sum_set_len - len(timeslot_set)


def teacher_conflict(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
                .group_by(lambda lesson: lesson.teacher,
                          ConstraintCollectors.to_list()) \
                .penalize("Teacher conflict",
                          HardSoftScore.ONE_HARD,
                          lambda teacher, lesson_list: timeslots_intersection(lesson_list))


def student_group_conflict(constraint_factory: ConstraintFactory):
    # A student can attend at most one lesson at the same time.
    return constraint_factory.for_each(Lesson) \
            .group_by(lambda lesson: lesson.student_group,
                      lambda lesson: lesson.teacher,
                  ConstraintCollectors.to_list()) \
            .penalize("Student group conflict",
                      HardSoftScore.ONE_HARD,
                      lambda student_group, teacher, lesson_list: timeslots_intersection(lesson_list))