PAIR_DAILY = 7
NUM_DAYS = 6
WEEK = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SUN']
# Минимальное количество квантов 387, максимальное 447, а на 125 групп нужно 375
# Количество преподов 112
# Количество таймслотов 112 * 42 = 4704. Нужно 125 * 5 = 625

def calculate_week_day(slot_id):
    return WEEK[(slot_id - 1) // PAIR_DAILY]


def calculate_lesson_num(slot_id):
    return (slot_id - 1) % PAIR_DAILY + 1