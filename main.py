import datetime,sys
#zmienne
current_datetime = str(datetime.datetime.now())
day_name = datetime.datetime.now().strftime("%A")
print(current_datetime.split(".")[0],day_name)
#sprawdzanie dnia

days = {
    '1': r"dni/pon.txt",
    '2': r"dni/wtor.txt",
    '3': r"dni/środ.txt",
    '4': r"dni/czwart.txt",
    '5': r"dni/piąt.txt",
    '6': r"dni/sob.txt",
    '7': r"dni/niedz.txt"
}
def what_to_do_in_this_day(day,what_to_do):
    with open(days[day], "r") as file:
        for line in file:
            tasks = line.strip()
            what_to_do.append(tasks.split(" "))

#co do zrobienia

def show_day():
    what_to_do = []
    day = str(input("Podaj dzień:\n"))
    what_to_do_in_this_day(day,what_to_do)
    print(what_to_do)

def add_task():
    what_to_do = []
    day = str(input("Podaj dzień:\n"))
    what_to_do_in_this_day(day, what_to_do)
    task = str(input("Podaj zadanie:\n"))
    hour1 = int(input("Podaj godzine rozpoczęcia:\n"))
    hour2 = int(input("Podaj godzine zakończenia:\n"))
    task = task.replace(" ","_")
    tasks = [str(hour1),str(hour2),task]
    task = 0
    while True:
        if what_to_do == []:
            what_to_do.append(tasks)
            break
        elif int(what_to_do[task][0]) >= hour1:
            what_to_do.insert(task,tasks)
            break
        task += 1
    to_write = ""
    for line in what_to_do:
        for text in line:
            to_write += text
            to_write += " "
        to_write+="\n"
    with open(days[day], "w") as file:
        file.write(to_write)
    print("Pomyślnie dodano zadanie")

def remove_task():
    what_to_do = []
    day = str(input("Podaj dzień:\n"))
    what_to_do_in_this_day(day, what_to_do)
    print(what_to_do)
    task = str(input("Podaj zadanie do usunięcia:\n"))
    new_tasks = []
    for line in what_to_do:
        if str(line[2]) != task:
            new_tasks.append(line)
    to_write = ""
    for line in new_tasks:
        for text in line:
            to_write += text
            to_write += " "
        to_write+="\n"
    with open(days[day], "w") as file:
        file.write(to_write)
    print("Pomyślnie usunięto zadanie")

def clear_day():
    day = str(input("Podaj dzień:\n"))
    a = open(days[day], "w")
    a.close()
    print("Pomyślnie wyczyszczono zadania")

def stop():
    sys.exit()

answer = {
    '1': show_day,
    '2': add_task,
    '3': remove_task,
    '4': clear_day,
    '5': stop
}
def main():
    while True:
        print("Podaj co chcesz zrobić: 1-pokazuje zadania na dany dzień, 2-dodaje zadanie do konkretnego dnia,3-usuwa konkretne zadanie z dnia,4-usówa wszystkie zadania z danego dnia, 5-kończy program:")
        a = str(input())
        answer[a]()
main()
