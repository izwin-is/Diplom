PAIR_DAILY = 5
NUM_DAYS = 3
WEEK = ['MON', 'TUE', 'WED']


def calculate_week_day(slot_id):
    return WEEK[(slot_id - 1) // PAIR_DAILY]


def calculate_lesson_num(slot_id):
    return (slot_id - 1) % PAIR_DAILY + 1