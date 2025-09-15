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

with open("utility/dates.txt", 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        if line == '\n' or line[0]=='#':
            continue
        if line[0] == '-':
            break
        line = line.strip().split(' ', 1)

        if len(line[0])==10:
            date = datetime.strptime(line[0], '%d.%m.%Y')
        else:
            date = datetime.strptime(line[0], '%d.%m')

        my_dict[date] = line[1]
    f.close()

my_dict = dict(sorted(my_dict.items(), key=lambda x: (x[0].month, x[0].day)))

with open("dates_sorted.txt", 'w', encoding='utf-8') as f:
    for item in my_dict.items():
        temp_str = str(item[0].day) + ' ' + months[item[0].month-1] + ' '
        if item[0].year != 1900:
            temp_str += str(item[0].year) + ' '
        temp_str += '-- ' + item[1] + '\n\n'
        f.write(temp_str)
    f.close()