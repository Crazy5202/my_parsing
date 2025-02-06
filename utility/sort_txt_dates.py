from datetime import datetime

months = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь"
]

my_dict = {}

with open("dates.txt", 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip().split(' ', 1)

        date = datetime.strptime(line[0], '%d.%m.%Y')

        my_dict[date] = line[1]
    f.close()

my_dict = dict(sorted(my_dict.items(), key=lambda x: (x[0].month, x[0].day)))

with open("dates_sorted.txt", 'w', encoding='utf-8') as f:
    for item in my_dict.items():
        f.write(str(item[0].day) + ' ' + months[item[0].month-1] + ' ' + str(item[0].year) + ' -- ' + item[1] + '\n')
    f.close()