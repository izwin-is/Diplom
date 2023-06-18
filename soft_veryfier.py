import sqlite3 as sq

with sq.connect("lessons.db") as con:
    cur = con.cursor()

    print('Проверка количества пар у преподавателя')
    count1 = 0
    cur.execute("""SELECT lesson.teacher_id, teacher.name, teacher.min_lessons, teacher.max_lessons, count(lesson.teacher_id) FROM lesson
                   JOIN teacher ON  lesson.teacher_id = teacher.teacher_id
                   GROUP BY lesson.teacher_id""")
    result = cur.fetchall()
    for teacher in result:
        if teacher[4] < teacher[2]:
            print(f'Слишком мало пар у {teacher[1]}(id={teacher[0]}). '
                  f'Всего пар:{teacher[4]}, min={teacher[2]}, max={teacher[3]}')
            count1 += teacher[2] - teacher[4]
        elif teacher[4] > teacher[3]:
            print(f'Слишком много пар у {teacher[1]}(id={teacher[0]}). '
                  f'Всего пар:{teacher[4]}, min={teacher[2]}, max={teacher[3]}')
            count1 += teacher[4] - teacher[3]
    if count1 == 0:
        print('Каждый преподаватель получил желаемое количество пар')
    else:
        print(count1)

    print('=====================')
    print('Проверка максимального количества дней на кампусе')
    count2 = 0
    cur.execute("""SELECT *, count(*) FROM (SELECT teacher.teacher_id, teacher.name, teacher.max_days
                   FROM teacher
                   JOIN lesson ON teacher.teacher_id == lesson.teacher_id
                   GROUP BY teacher.teacher_id, lesson.week_day)
				   GROUP BY teacher_id""")
    result = cur.fetchall()
    for teacher in result:
        if teacher[2] < teacher[3]:
            print(f'Слишком много дней на кампусе у {teacher[1]}(id={teacher[0]}) '
                  f'max_days={teacher[2]}, на самом деле {teacher[3]}')
            count2 += teacher[3] - teacher[2]
    if count2 == 0:
        print('Каждый преподаватель работает не более максимального количества дней')
    else:
        print(count2)

    print('=====================')
    print('Проверка пожеланий преподавателей по группам')
    count3 = 0
    cur.execute("""SELECT teacher_id, name, wishes_sem, wishes_lab FROM teacher
				   WHERE wishes_sem != '' OR wishes_lab != ''""")
    teacher_param_list = cur.fetchall()

    for teacher_param in teacher_param_list:
        if teacher_param[2]:
            wishes_sem = teacher_param[2].split(',')
            for wish_group in wishes_sem:
                cur.execute(f"""SELECT lesson_id FROM lesson
                               WHERE teacher_id = {teacher_param[0]} 
                               AND student_group = '{wish_group}' 
                               AND subject = 'sem'""")
                if len(cur.fetchall()) == 0:
                    count3 += 1
                    print(f"{teacher_param[1]}(id={teacher_param[0]}) не ведёт sem у {wish_group}, а хотел")

        if teacher_param[3]:
            wishes_lab = teacher_param[3].split(',')
            for wish_group in wishes_lab:
                cur.execute(f"""SELECT lesson_id FROM lesson
                               WHERE teacher_id = {teacher_param[0]} 
                               AND student_group = '{wish_group}' 
                               AND subject = 'lab'""")
                if len(cur.fetchall()) == 0:
                    count3 += 1
                    print(f"{teacher_param[1]}(id={teacher_param[0]}) не ведёт lab у {wish_group}, а хотел")

    if count3 == 0:
        print('Каждый преподаватель работает с желаемой группой')
    else:
        print(count3)


print(f'Всего ошибок {count1 + count2 + count3}')
