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
        teacher_timing(constraint_factory),
        student_group_timing(constraint_factory),
        teacher_at_least_one_lesson(constraint_factory),
        # teacher_max_lessons_total(constraint_factory),
        # teacher_min_lessons_total(constraint_factory)
        # teacher_max_lessons_total(constraint_factory),
        one_teacher_to_group(constraint_factory),
        # lab_start_end(constraint_factory)
        # Soft constraints
        teacher_max_days(constraint_factory),
        teacher_min_max_lessons_total(constraint_factory),
        teacher_min_max_lessons_particular(constraint_factory),
        one_lesson_per_day(constraint_factory),
        # teacher_min_lessons_total(constraint_factory),
    ]


def timeslots_intersection(lesson_list):
    sum_set_len = 0
    timeslot_set = set()
    for lesson in lesson_list:
        one_timeslot_set = lesson.timeslot.start_end_set
        sum_set_len += len(one_timeslot_set)
        timeslot_set = timeslot_set.union(one_timeslot_set)
    return sum_set_len - len(timeslot_set)


def count_teachers_num(lesson_list):
    teacher_set = set()
    for lesson in lesson_list:
        teacher_set.add(lesson.teacher)
    return len(teacher_set) - 1


def one_teacher_to_group(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
        .group_by(lambda lesson: lesson.student_group,
                  lambda lesson: lesson.subject,
                  ConstraintCollectors.to_list()) \
        .penalize("More than one teacher to one group",
                  HardSoftScore.ONE_HARD,
                  lambda group, subject, lesson_list: count_teachers_num(lesson_list))


def count_subject_discrepancy(teacher, lesson_list):
    actual_subject_dict = {}
    for subject in teacher.lesson_list.keys():
        actual_subject_dict[subject] = 0
    for lesson in lesson_list:
        actual_subject_dict[lesson.subject] += 1
    mis_score = 0
    for subject in actual_subject_dict.keys():
        if subject in teacher.lesson_list:
            mis_score += positive_score(-min(teacher.lesson_list[subject][1] - actual_subject_dict[subject],
                                        actual_subject_dict[subject] - teacher.lesson_list[subject][0]))
        else:
            mis_score += actual_subject_dict[subject]
    return mis_score


def teacher_min_max_lessons_particular(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
        .group_by(lambda lesson: lesson.teacher,
                  ConstraintCollectors.to_list()) \
        .penalize("Too many or too few particular lessons for teacher",
                  HardSoftScore.ONE_SOFT,
                  lambda teacher, lesson_list: count_subject_discrepancy(teacher, lesson_list))


def teacher_min_max_lessons_total(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
        .group_by(lambda lesson: lesson.teacher,
                  ConstraintCollectors.sum(lambda lesson: lesson.duration)) \
        .penalize("Too many or too few lessons for teacher",
                  HardSoftScore.ONE_SOFT,
                  lambda teacher, count: positive_score(-min(teacher.max_lessons - count,
                                                             count - teacher.min_lessons)))

def one_lesson_per_day(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
        .group_by(lambda lesson: lesson.student_group,
                  lambda lesson: lesson.timeslot.week_day,
                  ConstraintCollectors.count()) \
        .penalize("More than one student's group lesson per day",
                  HardSoftScore.ONE_SOFT,
                  lambda student_group, week_day, count: positive_score(count - 1))


def teacher_at_least_one_lesson(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Teacher) \
        .if_not_exists(Lesson,
                       Joiners.equal(lambda teacher: teacher.id,
                                     lambda lesson: lesson.teacher.id)) \
        .penalize("Unused teacher",
                  HardSoftScore.ONE_HARD)


# def teacher_max_lessons_total(constraint_factory: ConstraintFactory):
#     return constraint_factory.for_each(Lesson) \
#             .group_by(lambda lesson: lesson.teacher,
#                       ConstraintCollectors.sum(lambda lesson: lesson.duration)) \
#             .filter(lambda teacher, count: count - teacher.max_lessons > 0) \
#             .penalize("Too many lessons for teacher",
#                       HardSoftScore.ONE_HARD,
#                       lambda teacher, count: count)


# def teacher_min_lessons_total(constraint_factory: ConstraintFactory):
#     return constraint_factory.for_each(Lesson) \
#             .group_by(lambda lesson: lesson.teacher,
#                       ConstraintCollectors.sum(lambda lesson: lesson.duration)) \
#             .filter(lambda teacher, count: teacher.min_lessons - count > 0) \
#             .penalize("Too few lessons for teacher",
#                       HardSoftScore.ONE_HARD,
#                       lambda teacher, count: count)


def teacher_max_days(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Lesson) \
        .group_by(lambda lesson: lesson.teacher,
                  lambda lesson: lesson.timeslot.week_day,
                  ConstraintCollectors.count()) \
        .group_by(lambda teacher, days, count: teacher,
                  ConstraintCollectors.countTri()) \
        .penalize("",
                  HardSoftScore.ONE_SOFT,
                  lambda teacher, count: positive_score(count - teacher.max_days))


def teacher_timing(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Teacher) \
        .join(Lesson,
              Joiners.equal(lambda teacher: teacher.id,
                            lambda lesson: lesson.teacher.id)) \
        .filter(lambda teacher, lesson: not lesson.timeslot.start_end_set.issubset(teacher.slots_set)) \
        .penalize("Teacher is busy", HardSoftScore.ONE_HARD)


def student_group_timing(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(StudentGroup) \
        .join(Lesson,
              Joiners.equal(lambda student_group: student_group.id,
                            lambda lesson: lesson.student_group.id)) \
        .filter(lambda student_group, lesson: not lesson.timeslot.start_end_set.issubset(student_group.slots_set)) \
        .penalize("Student Group is busy", HardSoftScore.ONE_HARD)


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
                  ConstraintCollectors.to_list()) \
        .penalize("Student group conflict",
                  HardSoftScore.ONE_HARD,
                  lambda student_group, lesson_list: timeslots_intersection(lesson_list))
