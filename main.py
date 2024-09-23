import tkinter as tk
from tkinter import messagebox
import datetime
import sys

# Zmienne
days = {
    '1': r"dni/pon.txt",
    '2': r"dni/wtor.txt",
    '3': r"dni/srod.txt",
    '4': r"dni/czwart.txt",
    '5': r"dni/piat.txt",
    '6': r"dni/sob.txt",
    '7': r"dni/niedz.txt"
}


# Funkcja do pobrania zadań z pliku na dany dzień
def what_to_do_in_this_day(day):
    what_to_do = []
    try:
        with open(days[day], "r") as file:
            for line in file:
                tasks = line.strip()
                what_to_do.append(tasks.split(" "))
    except FileNotFoundError:
        return what_to_do
    return what_to_do


# Funkcja do sortowania zadań
def sort_tasks(tasks):
    return sorted(tasks, key=lambda x: (x[0], x[1]))


# Funkcje GUI do obsługi zadań
def refresh_tasks():
    what_to_do = what_to_do_in_this_day(day_entry.get())
    sorted_tasks = sort_tasks(what_to_do)
    tasks_text = ""
    for task in sorted_tasks:
        tasks_text += " ".join(task) + "\n"

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, tasks_text)


def show_day():
    day = day_entry.get()
    if day not in days:
        messagebox.showerror("Błąd", "Podano nieprawidłowy dzień.")
        return

    refresh_tasks()
    show_task_buttons()  # Pokazuje przyciski po wybraniu dnia


def show_task_buttons():
    task_frame.pack(pady=10)  # Pokazuje sekcję z przyciskami do zadań
    add_task_button.pack(pady=5)
    remove_task_button.pack(pady=5)
    clear_day_button.pack(pady=5)


def validate_time_format(time_str):
    """Walidacja formatu godziny."""
    try:
        if ':' in time_str:
            hour, minute = map(int, time_str.split(':'))
            return 0 <= hour <= 23 and 0 <= minute <= 59
        else:
            hour = int(time_str)
            return 0 <= hour <= 23
    except ValueError:
        return False


def add_task():
    day = day_entry.get()
    if day not in days:
        messagebox.showerror("Błąd", "Podano nieprawidłowy dzień.")
        return

    task = task_entry.get()
    start_time = start_hour_entry.get()
    end_time = end_hour_entry.get()

    if not task or not validate_time_format(start_time) or not validate_time_format(end_time):
        messagebox.showerror("Błąd", "Podaj poprawne zadanie oraz godziny w formacie HH:mm lub HH.")
        return

    # Sprawdzenie, czy godzina zakończenia jest większa niż godzina rozpoczęcia
    start_hour = int(start_time.split(':')[0])
    end_hour = int(end_time.split(':')[0])

    if end_hour < start_hour or (
            end_hour == start_hour and int(end_time.split(':')[1]) <= int(start_time.split(':')[1])):
        messagebox.showerror("Błąd", "Godzina zakończenia musi być większa niż godzina rozpoczęcia.")
        return

    task = task.replace(" ", "_")
    tasks = [start_time, end_time, task]
    what_to_do = what_to_do_in_this_day(day)

    task_idx = 0
    while True:
        if not what_to_do:
            what_to_do.append(tasks)
            break
        elif int(what_to_do[task_idx][0].split(':')[0]) >= int(start_time.split(':')[0]):
            what_to_do.insert(task_idx, tasks)
            break
        task_idx += 1

    # Zapisanie nowych zadań do pliku
    with open(days[day], "w") as file:
        for line in sort_tasks(what_to_do):
            file.write(" ".join(line) + "\n")

    messagebox.showinfo("Sukces", "Pomyślnie dodano zadanie.")
    clear_entries()
    refresh_tasks()


def remove_task():
    day = day_entry.get()
    if day not in days:
        messagebox.showerror("Błąd", "Podano nieprawidłowy dzień.")
        return

    task = task_entry.get()
    if not task:
        messagebox.showerror("Błąd", "Proszę podać zadanie do usunięcia.")
        return

    what_to_do = what_to_do_in_this_day(day)
    new_tasks = [line for line in what_to_do if line[2] != task]

    # Zapisanie zadań po usunięciu do pliku
    with open(days[day], "w") as file:
        for line in sort_tasks(new_tasks):
            file.write(" ".join(line) + "\n")

    messagebox.showinfo("Sukces", "Pomyślnie usunięto zadanie.")
    clear_entries()
    refresh_tasks()


def clear_day():
    day = day_entry.get()
    if day not in days:
        messagebox.showerror("Błąd", "Podano nieprawidłowy dzień.")
        return
    with open(days[day], "w") as file:
        file.write("")
    messagebox.showinfo("Sukces", "Pomyślnie wyczyszczono zadania.")
    refresh_tasks()


def clear_entries():
    task_entry.delete(0, tk.END)
    start_hour_entry.delete(0, tk.END)
    end_hour_entry.delete(0, tk.END)


# Funkcja zamykająca aplikację
def close_app():
    window.destroy()


# Utworzenie GUI z użyciem tkinter
window = tk.Tk()
window.title("Zarządzanie zadaniami")

# Ustawienie trybu pełnoekranowego
window.attributes('-fullscreen', True)

# Przycisk zamykający na górze
close_button = tk.Button(window, text="Zamknij", command=close_app)
close_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

# Elementy GUI - początkowe
tk.Label(window, text="Podaj dzień (1-pon, 2-wt, ..., 7-niedz):").pack(pady=5)
day_entry = tk.Entry(window)
day_entry.pack(pady=5)

output_text = tk.Text(window, height=15, width=70)
output_text.pack(pady=10)

# Sekcja z przyciskami do zarządzania zadaniami
task_frame = tk.Frame(window)

task_entry_label = tk.Label(task_frame, text="Zadanie:")
task_entry_label.pack(side=tk.LEFT)
task_entry = tk.Entry(task_frame)
task_entry.pack(side=tk.LEFT, padx=5)

start_hour_entry_label = tk.Label(task_frame, text="Godzina rozpoczęcia:")
start_hour_entry_label.pack(side=tk.LEFT)
start_hour_entry = tk.Entry(task_frame)
start_hour_entry.pack(side=tk.LEFT, padx=5)

end_hour_entry_label = tk.Label(task_frame, text="Godzina zakończenia:")
end_hour_entry_label.pack(side=tk.LEFT)
end_hour_entry = tk.Entry(task_frame)
end_hour_entry.pack(side=tk.LEFT, padx=5)

# Przyciski
show_day_button = tk.Button(window, text="Pokaż zadania", command=show_day)
add_task_button = tk.Button(window, text="Dodaj zadanie", command=add_task)
remove_task_button = tk.Button(window, text="Usuń zadanie", command=remove_task)
clear_day_button = tk.Button(window, text="Wyczyść zadania", command=clear_day)

# Dodanie sekcji i przycisków do widoku
task_frame.pack(pady=10)
show_day_button.pack(pady=5)

# Nasłuchiwanie na zmianę w polu dnia
day_entry.bind("<Return>", lambda event: show_day())  # Uruchamia show_day po naciśnięciu Enter

# Uruchomienie pętli aplikacji
window.mainloop()
