from db_filler import fill_db
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
    "Б09-909": {"sem":2, "lab": 2}
}

PAIR_DAILY = 4
NUM_DAYS = 3

mainset = {1, 2, 3}
subset = {1, 3, 5}
mainset = mainset.union(subset)
print(mainset)

