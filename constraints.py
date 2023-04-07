from problem_classes import Lesson, Teacher, StudentGroup, calculate_week_day
from optapy import constraint_provider
from optapy.constraint import Joiners, ConstraintFactory
from optapy.constraint import ConstraintCollectors
from optapy.score import HardSoftScore


def positive_score(x):
    if x < 0:
        return 0
    return x
@constraint_provider
def define_constraints(constraint_factory):
    return [
        # Hard constraints
        teacher_conflict(constraint_factory),
        teacher_timing(constraint_factory),
        student_group_conflict(constraint_factory),
        student_group_timing(constraint_factory),
        teacher_max_lessons(constraint_factory),
        teacher_max_days(constraint_factory)
        # Soft constraints
        # teacher_max_days(constraint_factory)
        # teacher_room_stability(constraint_factory),
        # teacher_time_efficiency(constraint_factory),
        # student_group_subject_variety(constraint_factory)
    ]


def teacher_max_lessons(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
            .group_by(lambda lesson: lesson.teacher,
                      ConstraintCollectors.count()) \
            .penalize("Too many lessons for teacher",
                      HardSoftScore.ONE_HARD,
                      lambda teacher, count: positive_score(count - teacher.max_lessons))

def teacher_max_days(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
            .group_by(lambda lesson: lesson.teacher,
                      lambda lesson: lesson.timeslot.week_day,
                      ConstraintCollectors.count()) \
            .group_by(lambda teacher, days, count: teacher,
                      ConstraintCollectors.countTri()) \
            .penalize("",
                      HardSoftScore.ONE_HARD,
                      lambda teacher, count: positive_score(count - teacher.max_days))
    # return constraint_factory.for_each(Lesson) \
    #         .group_by(lambda lesson: lesson.teacher,
    #                   lambda lesson: lesson.timeslot.week_day,
    #                   ConstraintCollectors.count_distinct()) \
    #         .penalize("",
    #                   HardSoftScore.ONE_HARD,
    #                   lambda teacher, days, count: positive_score(count - teacher.max_days))
    # return constraint_factory.for_each(Lesson) \
    #         .group_by(lambda lesson: lesson.teacher,
    #                   lambda lesson: lesson.timeslot.week_day,
    #                   ConstraintCollectors.count())\
    #         .penalize("Too many working days for teacher",
    #                   HardSoftScore.ONE_HARD,
    #                   lambda teacher, a, count: positive_score(count - teacher.max_days))
    # return constraint_factory.for_each(Lesson) \
    #         .group_by(lambda lesson: lesson.teacher,
    #                   ConstraintCollectors.conditionally(
    #                       lambda lesson: calculate_week_day(lesson.timeslot.id),
    #                       ConstraintCollectors.count_distinct()
    #                   )
    #         )\
    #         .penalize("Too many working days for teacher",
    #                   HardSoftScore.ONE_HARD,
    #                   lambda teacher, count: positive_score(count - teacher.max_days))

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
def teacher_conflict(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
                .join(Lesson,
                      Joiners.equal(lambda lesson: lesson.timeslot),
                      Joiners.equal(lambda lesson: lesson.teacher),
                      Joiners.less_than(lambda lesson: lesson.id)
                ) \
                .penalize("Teacher conflict", HardSoftScore.ONE_HARD)


def student_group_conflict(constraint_factory: ConstraintFactory):
    # A student can attend at most one lesson at the same time.
    return constraint_factory.for_each(Lesson) \
            .join(Lesson,
                  Joiners.equal(lambda lesson: lesson.timeslot),
                  Joiners.equal(lambda lesson: lesson.student_group.id),
                  Joiners.less_than(lambda lesson: lesson.id)
            ) \
            .penalize("Student group conflict", HardSoftScore.ONE_HARD)