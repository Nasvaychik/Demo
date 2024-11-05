import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime


# Функция для регистрации пациента
def submit_patient_data():
    # Собираем данные из полей
    patient_data = {
        "first_name": first_name.get(),
        "last_name": last_name.get(),
        "patronymic": patronymic.get(),
        "passport_number": passport_number.get(),
        "passport_series": passport_series.get(),
        "date_of_birth": date_of_birth.get(),
        "gender": gender_var.get(),
        "address": address.get(),
        "phone_number": phone_number.get(),
        "email": email.get(),
        "medical_card_number": medical_card_number.get(),
        "medical_card_issue_date": medical_card_issue_date.get(),
        "last_visit_date": last_visit_date.get(),
        "next_visit_date": next_visit_date.get(),
        "insurance_policy_number": insurance_policy_number.get(),
        "insurance_policy_expiry": insurance_policy_expiry.get(),
        "diagnosis": diagnosis.get(),
        "medical_history": medical_history.get("1.0", "end-1c"),
        "photo": photo_data  # Сохраняем фото как бинарные данные
    }

    # Выводим данные (в реальном случае можно отправить их в базу данных)
    print("Пациент зарегистрирован:", patient_data)

    # Покажем сообщение об успешной регистрации
    messagebox.showinfo("Успех", "Пациент успешно зарегистрирован!")


# Обработчик выбора файла (фото пациента)
def on_file_pick():
    global photo_data
    file_path = filedialog.askopenfilename(title="Выберите фото",
                                           filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*")))
    if file_path:
        with open(file_path, "rb") as file:
            photo_data = file.read()  # Сохраняем фото как бинарные данные
        photo_label.config(text="Фото выбрано: " + file_path.split('/')[-1])  # Отображаем название файла


# Функция для записи на госпитализацию
def hospitalization():
    hospitalization_code = hospitalization_code_entry.get()

    # Если код госпитализации введен
    if hospitalization_code:
        # Вводим данные о госпитализации
        hospitalization_data = {
            "code": hospitalization_code,
            "first_name": first_name.get(),
            "last_name": last_name.get(),
            "diagnosis": diagnosis.get(),
            "department": department.get(),
            "hospitalization_goal": hospitalization_goal.get(),
            "payment_type": payment_type_var.get(),
            "hospitalization_dates": hospitalization_dates.get(),
            "additional_info": additional_info.get("1.0", "end-1c"),
        }

        print("Данные госпитализации:", hospitalization_data)

        # Показать информацию о госпитализации
        hospitalization_info = f"Код госпитализации: {hospitalization_data['code']}\n"
        hospitalization_info += f"Пациент: {hospitalization_data['first_name']} {hospitalization_data['last_name']}\n"
        hospitalization_info += f"Диагноз: {hospitalization_data['diagnosis']}\n"
        hospitalization_info += f"Цель госпитализации: {hospitalization_data['hospitalization_goal']}\n"
        hospitalization_info += f"Отделение: {hospitalization_data['department']}\n"
        hospitalization_info += f"Тип оплаты: {hospitalization_data['payment_type']}\n"
        hospitalization_info += f"Сроки госпитализации: {hospitalization_data['hospitalization_dates']}\n"
        hospitalization_info += f"Доп. информация: {hospitalization_data['additional_info']}"

        hospitalization_display_label.config(text=hospitalization_info)
    else:
        messagebox.showwarning("Ошибка", "Введите код госпитализации.")


# Функция для отмены госпитализации
def cancel_hospitalization():
    reason = cancel_reason_entry.get("1.0", "end-1c")

    if reason:
        messagebox.showinfo("Отмена госпитализации", f"Госпитализация отменена по причине: {reason}")
    else:
        messagebox.showwarning("Ошибка", "Введите причину отмены госпитализации.")


# Создание главного окна
root = tk.Tk()
root.title("Госпитализация пациента")
root.geometry("1000x1000")

# Переменная для хранения данных фото
photo_data = None

# Создаем виджеты для данных пациента
first_name_label = tk.Label(root, text="Имя пациента:")
first_name = tk.Entry(root)

last_name_label = tk.Label(root, text="Фамилия пациента:")
last_name = tk.Entry(root)

patronymic_label = tk.Label(root, text="Отчество пациента:")
patronymic = tk.Entry(root)

passport_number_label = tk.Label(root, text="Номер паспорта:")
passport_number = tk.Entry(root)

passport_series_label = tk.Label(root, text="Серия паспорта:")
passport_series = tk.Entry(root)

date_of_birth_label = tk.Label(root, text="Дата рождения пациента:")
date_of_birth = tk.Entry(root)

gender_label = tk.Label(root, text="Пол пациента:")
gender_var = tk.StringVar(value="Мужской")
gender_male = tk.Radiobutton(root, text="Мужской", variable=gender_var, value="Мужской")
gender_female = tk.Radiobutton(root, text="Женский", variable=gender_var, value="Женский")

address_label = tk.Label(root, text="Адрес пациента:")
address = tk.Entry(root)

phone_number_label = tk.Label(root, text="Телефонный номер пациента:")
phone_number = tk.Entry(root)

email_label = tk.Label(root, text="Электронный адрес пациента:")
email = tk.Entry(root)

medical_card_number_label = tk.Label(root, text="Номер медицинской карты:")
medical_card_number = tk.Entry(root)

medical_card_issue_date_label = tk.Label(root, text="Дата выдачи медицинской карты:")
medical_card_issue_date = tk.Entry(root)

last_visit_date_label = tk.Label(root, text="Дата последнего обращения:")
last_visit_date = tk.Entry(root)

next_visit_date_label = tk.Label(root, text="Дата следующего визита:")
next_visit_date = tk.Entry(root)

insurance_policy_number_label = tk.Label(root, text="Номер страхового полиса:")
insurance_policy_number = tk.Entry(root)

insurance_policy_expiry_label = tk.Label(root, text="Дата окончания полиса:")
insurance_policy_expiry = tk.Entry(root)

diagnosis_label = tk.Label(root, text="Диагноз пациента:")
diagnosis = tk.Entry(root)

medical_history_label = tk.Label(root, text="История болезни пациента:")
medical_history = tk.Text(root, height=5, width=50)

# Ввод кода госпитализации
hospitalization_code_label = tk.Label(root, text="Введите код госпитализации:")
hospitalization_code_entry = tk.Entry(root)

# Поля для записи госпитализации
department_label = tk.Label(root, text="Отделение госпитализации:")
department = tk.Entry(root)

hospitalization_goal_label = tk.Label(root, text="Цель госпитализации:")
hospitalization_goal = tk.Entry(root)

payment_type_label = tk.Label(root, text="Тип оплаты:")
payment_type_var = tk.StringVar(value="Бюджет")
payment_type_budget = tk.Radiobutton(root, text="Бюджет", variable=payment_type_var, value="Бюджет")
payment_type_paid = tk.Radiobutton(root, text="Платно", variable=payment_type_var, value="Платно")

hospitalization_dates_label = tk.Label(root, text="Сроки госпитализации:")
hospitalization_dates = tk.Entry(root)

additional_info_label = tk.Label(root, text="Доп. информация:")
additional_info = tk.Text(root, height=4, width=50)

# Поле для вывода информации о госпитализации
hospitalization_display_label = tk.Label(root, text="Информация о госпитализации будет отображаться здесь.",
                                         justify="left", anchor="w")

# Кнопки для работы с госпитализацией
submit_hospitalization_button = tk.Button(root, text="Записать на госпитализацию", command=hospitalization)

# Поле для отмены госпитализации
cancel_reason_label = tk.Label(root, text="Причина отмены госпитализации:")
cancel_reason_entry = tk.Text(root, height=4, width=50)

cancel_hospitalization_button = tk.Button(root, text="Отменить госпитализацию", command=cancel_hospitalization)

# Кнопка для регистрации пациента
submit_button = tk.Button(root, text="Зарегистрировать пациента", command=submit_patient_data)

# Кнопка для загрузки фото
photo_label = tk.Label(root, text="Фото пациента:")
photo_button = tk.Button(root, text="Загрузить фото", command=on_file_pick)

# Размещение виджетов на экране
first_name_label.grid(row=0, column=0, sticky="w")
first_name.grid(row=0, column=1)

last_name_label.grid(row=1, column=0, sticky="w")
last_name.grid(row=1, column=1)

patronymic_label.grid(row=2, column=0, sticky="w")
patronymic.grid(row=2, column=1)

passport_number_label.grid(row=3, column=0, sticky="w")
passport_number.grid(row=3, column=1)

passport_series_label.grid(row=4, column=0, sticky="w")
passport_series.grid(row=4, column=1)

date_of_birth_label.grid(row=5, column=0, sticky="w")
date_of_birth.grid(row=5, column=1)

gender_label.grid(row=6, column=0, sticky="w")
gender_male.grid(row=6, column=1)
gender_female.grid(row=6, column=2)

address_label.grid(row=7, column=0, sticky="w")
address.grid(row=7, column=1)

phone_number_label.grid(row=8, column=0, sticky="w")
phone_number.grid(row=8, column=1)

email_label.grid(row=9, column=0, sticky="w")
email.grid(row=9, column=1)

medical_card_number_label.grid(row=10, column=0, sticky="w")
medical_card_number.grid(row=10, column=1)

medical_card_issue_date_label.grid(row=11, column=0, sticky="w")
medical_card_issue_date.grid(row=11, column=1)

last_visit_date_label.grid(row=12, column=0, sticky="w")
last_visit_date.grid(row=12, column=1)

next_visit_date_label.grid(row=13, column=0, sticky="w")
next_visit_date.grid(row=13, column=1)

insurance_policy_number_label.grid(row=14, column=0, sticky="w")
insurance_policy_number.grid(row=14, column=1)

insurance_policy_expiry_label.grid(row=15, column=0, sticky="w")
insurance_policy_expiry.grid(row=15, column=1)

diagnosis_label.grid(row=16, column=0, sticky="w")
diagnosis.grid(row=16, column=1)

medical_history_label.grid(row=17, column=0, sticky="w")
medical_history.grid(row=17, column=1)

# Размещение новых полей для госпитализации
hospitalization_code_label.grid(row=18, column=0, sticky="w")
hospitalization_code_entry.grid(row=18, column=1)

department_label.grid(row=19, column=0, sticky="w")
department.grid(row=19, column=1)

hospitalization_goal_label.grid(row=20, column=0, sticky="w")
hospitalization_goal.grid(row=20, column=1)

payment_type_label.grid(row=21, column=0, sticky="w")
payment_type_budget.grid(row=21, column=1)
payment_type_paid.grid(row=21, column=2)

hospitalization_dates_label.grid(row=22, column=0, sticky="w")
hospitalization_dates.grid(row=22, column=1)

additional_info_label.grid(row=23, column=0, sticky="w")
additional_info.grid(row=23, column=1)

hospitalization_display_label.grid(row=24, column=0, columnspan=2, sticky="w")

# Кнопки для действий
submit_hospitalization_button.grid(row=25, column=0, columnspan=2)

cancel_reason_label.grid(row=26, column=0, sticky="w")
cancel_reason_entry.grid(row=26, column=1)

cancel_hospitalization_button.grid(row=27, column=0, columnspan=2)

photo_label.grid(row=28, column=0, sticky="w")
photo_button.grid(row=28, column=1)

submit_button.grid(row=29, column=0, columnspan=2)

# Запуск приложения
root.mainloop()
