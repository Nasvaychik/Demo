import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import qrcode
import os
import requests
import random
import threading
from PIL import Image, ImageTk
from datetime import datetime
from docx import Document


# Установка базы данных
def setup_db():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            passport TEXT UNIQUE,
            work_place TEXT,
            insurance_number TEXT,
            insurance_validity TEXT,
            insurance_company TEXT,
            medical_card_number TEXT UNIQUE,
            photo_filename TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hospitalizations (
            id INTEGER PRIMARY KEY,
            patient_id INTEGER,
            hospitalization_code TEXT,
            admission_date TEXT,
            department TEXT,
            payment_type TEXT,
            additional_info TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY,
            patient_id INTEGER,
            doctor_id INTEGER,
            details TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
    ''')
    conn.commit()
    conn.close()


class PatientRegistrationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Регистрация пациента")
        self.geometry("600x600")
        self.setup_ui()

    def setup_ui(self):
        # Поля ввода для регистрации пациента
        tk.Label(self, text="Имя пациента:").grid(row=0, column=0, sticky="w")
        self.first_name_entry = tk.Entry(self)
        self.first_name_entry.grid(row=0, column=1)

        tk.Label(self, text="Фамилия:").grid(row=1, column=0, sticky="w")
        self.last_name_entry = tk.Entry(self)
        self.last_name_entry.grid(row=1, column=1)

        tk.Label(self, text="Паспортные данные:").grid(row=2, column=0, sticky="w")
        self.passport_entry = tk.Entry(self)
        self.passport_entry.grid(row=2, column=1)

        tk.Label(self, text="Место работы:").grid(row=3, column=0, sticky="w")
        self.work_place_entry = tk.Entry(self)
        self.work_place_entry.grid(row=3, column=1)

        tk.Label(self, text="Страховой номер:").grid(row=4, column=0, sticky="w")
        self.insurance_number_entry = tk.Entry(self)
        self.insurance_number_entry.grid(row=4, column=1)

        tk.Label(self, text="Срок действия страхового полиса:").grid(row=5, column=0, sticky="w")
        self.insurance_validity_entry = tk.Entry(self)
        self.insurance_validity_entry.grid(row=5, column=1)

        tk.Label(self, text="Страховая компания:").grid(row=6, column=0, sticky="w")
        self.insurance_company_entry = tk.Entry(self)
        self.insurance_company_entry.grid(row=6, column=1)

        tk.Label(self, text="Номер медкарты:").grid(row=7, column=0, sticky="w")
        self.medical_card_number_entry = tk.Entry(self)
        self.medical_card_number_entry.grid(row=7, column=1)

        tk.Label(self, text="Фотография пациента:").grid(row=8, column=0, sticky="w")
        self.photo_label = tk.Label(self, text="Нет файла")
        self.photo_label.grid(row=8, column=1)
        tk.Button(self, text="Загрузить", command=self.upload_photo).grid(row=8, column=2)

        # Кнопки
        tk.Button(self, text="Сохранить", command=self.save_patient).grid(row=9, column=0, columnspan=3)
        tk.Button(self, text="Госпитализация", command=self.open_hospitalization_window).grid(row=10, column=0,
                                                                                              columnspan=3)
        tk.Button(self, text="Вход для врачей", command=self.doctor_login).grid(row=11, column=0, columnspan=3)

    def upload_photo(self):
        file_path = filedialog.askopenfilename(title="Выберите файл", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.photo_filename = file_path
            self.photo_label.config(text=os.path.basename(file_path))

    def save_patient(self):
        # Получение данных из полей
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        passport = self.passport_entry.get()
        work_place = self.work_place_entry.get()
        insurance_number = self.insurance_number_entry.get()
        insurance_validity = self.insurance_validity_entry.get()
        insurance_company = self.insurance_company_entry.get()
        medical_card_number = self.medical_card_number_entry.get()

        if not all([first_name, last_name, passport, medical_card_number]):
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все обязательные поля.")
            return

        # Проверка на наличие пациента в БД
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE passport = ? OR medical_card_number = ?",
                       (passport, medical_card_number))
        if cursor.fetchone():
            messagebox.showerror("Ошибка", "Пациент с такими паспортными данными или номером медкарты уже существует.")
            conn.close()
            return

        # Сохранение пациента в БД
        cursor.execute('''
            INSERT INTO patients (first_name, last_name, passport, work_place, insurance_number, insurance_validity,
                                  insurance_company, medical_card_number, photo_filename)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, passport, work_place, insurance_number, insurance_validity, insurance_company,
              medical_card_number, self.photo_filename))

        conn.commit()

        # Генерация QR-кода
        qr_code_filename = self.generate_qr_code(medical_card_number)
        messagebox.showinfo("Успех", f"Пациент успешно зарегистрирован!\nQR-код сохранен: {qr_code_filename}")

        # Очистка полей ввода
        self.clear_fields()
        conn.close()

    def generate_qr_code(self, medical_card_number):
        qr = qrcode.make(medical_card_number)
        qr_filename = f'uploads/qr_{medical_card_number}.png'
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        qr.save(qr_filename)
        return qr_filename

    def clear_fields(self):
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.passport_entry.delete(0, tk.END)
        self.work_place_entry.delete(0, tk.END)
        self.insurance_number_entry.delete(0, tk.END)
        self.insurance_validity_entry.delete(0, tk.END)
        self.insurance_company_entry.delete(0, tk.END)
        self.medical_card_number_entry.delete(0, tk.END)
        self.photo_label.config(text="Нет файла")

    def open_hospitalization_window(self):
        self.hospitalization_window = tk.Toplevel(self)
        self.hospitalization_window.title("Госпитализация пациента")
        self.hospitalization_window.geometry("600x400")

        tk.Label(self.hospitalization_window, text="Код госпитализации:").grid(row=0, column=0, sticky="w")
        self.hospitalization_code_entry = tk.Entry(self.hospitalization_window)
        self.hospitalization_code_entry.grid(row=0, column=1)

        tk.Button(self.hospitalization_window, text="Проверить пациента", command=self.check_patient).grid(row=1,
                                                                                                           column=0,
                                                                                                           columnspan=2)
        tk.Button(self.hospitalization_window, text="Записать на госпитализацию",
                  command=self.record_hospitalization).grid(row=2, column=0, columnspan=2)
        tk.Button(self.hospitalization_window, text="Отказ от госпитализации",
                  command=self.cancel_hospitalization).grid(row=3, column=0, columnspan=2)

        self.info_label = tk.Label(self.hospitalization_window, text="", wraplength=500)
        self.info_label.grid(row=4, column=0, columnspan=2)

    def check_patient(self):
        hospitalization_code = self.hospitalization_code_entry.get()
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT p.first_name, p.last_name, p.passport, h.department, h.admission_date
                          FROM hospitalizations h
                          JOIN patients p ON h.patient_id = p.id
                          WHERE h.hospitalization_code = ?''', (hospitalization_code,))
        patient_info = cursor.fetchone()

        if patient_info:
            self.info_label.config(
                text=f"Пациент: {patient_info[0]} {patient_info[1]}\nПаспорт: {patient_info[2]}\nОтделение: {patient_info[3]}\nДата госпитализации: {patient_info[4]}")
        else:
            messagebox.showerror("Ошибка", "Пациент не найден.")
        conn.close()

    def record_hospitalization(self):
        hospitalization_code = self.hospitalization_code_entry.get()
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()

        # Check if the hospitalization code is valid
        cursor.execute('''SELECT id FROM patients WHERE medical_card_number = ?''', (hospitalization_code,))
        patient = cursor.fetchone()

        if not patient:
            messagebox.showerror("Ошибка", "Пациент не найден.")
            conn.close()
            return

        patient_id = patient[0]

        # Display hospitalization details and get user input
        admission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        department = "Терапия"  # Default department, can be changed
        payment_type = "Платно"  # Default payment type, can be changed
        additional_info = "Без дополнительных условий"  # Default additional info, can be changed

        # Insert hospitalization record
        cursor.execute('''
            INSERT INTO hospitalizations (patient_id, hospitalization_code, admission_date, department, payment_type, additional_info)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (patient_id, hospitalization_code, admission_date, department, payment_type, additional_info))

        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", f"Пациент успешно записан на госпитализацию с кодом {hospitalization_code}.")

    def cancel_hospitalization(self):
        hospitalization_code = self.hospitalization_code_entry.get()

        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()

        # Check if the hospitalization exists
        cursor.execute('''SELECT * FROM hospitalizations WHERE hospitalization_code = ?''', (hospitalization_code,))
        if cursor.fetchone() is None:
            messagebox.showerror("Ошибка", "Госпитализация с таким кодом не найдена.")
            conn.close()
            return

        reason = "Отмена по просьбе пациента"  # Reason for cancellation, can be improved
        cursor.execute('''
            DELETE FROM hospitalizations WHERE hospitalization_code = ?
        ''', (hospitalization_code,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", f"Госпитализация с кодом {hospitalization_code} отменена. Причина: {reason}.")

    def doctor_login(self):
        self.login_window = tk.Toplevel(self)
        self.login_window.title("Вход для врачей")
        self.login_window.geometry("300x200")

        tk.Label(self.login_window, text="Логин:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.login_window, text="Пароль:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.login_window, text="Войти", command=self.check_doctor_login).grid(row=2, columnspan=2)

    def check_doctor_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM doctors WHERE username = ? AND password = ?''', (username, password))
        doctor = cursor.fetchone()

        if doctor:
            messagebox.showinfo("Успех", "Вход успешен!")
            self.open_patient_info_window(doctor[0])  # Pass doctor ID
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль.")
        conn.close()

    def open_patient_info_window(self, doctor_id):
        self.patient_info_window = tk.Toplevel(self)
        self.patient_info_window.title("Информация о пациенте")
        self.patient_info_window.geometry("600x400")

        tk.Label(self.patient_info_window, text="Номер медицинской карты:").grid(row=0, column=0, sticky="w")
        self.medical_card_entry = tk.Entry(self.patient_info_window)
        self.medical_card_entry.grid(row=0, column=1)

        tk.Button(self.patient_info_window, text="Просмотреть информацию",
                  command=lambda: self.view_patient_info(doctor_id)).grid(row=1, columnspan=2)
        tk.Button(self.patient_info_window, text="Создать направление",
                  command=lambda: self.create_referral(doctor_id)).grid(row=2, columnspan=2)
        tk.Button(self.patient_info_window, text="Отслеживание перемещения",
                  command=lambda: self.track_movement(doctor_id)).grid(row=3, columnspan=2)

        self.patient_info_label = tk.Label(self.patient_info_window, text="", wraplength=500)
        self.patient_info_label.grid(row=4, column=0, columnspan=2)

    def view_patient_info(self, doctor_id):
        medical_card_number = self.medical_card_entry.get()

        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT first_name, last_name, passport, work_place FROM patients WHERE medical_card_number = ?''',
            (medical_card_number,))
        patient_info = cursor.fetchone()

        if patient_info:
            self.patient_info_label.config(
                text=f"Пациент: {patient_info[0]} {patient_info[1]}\nПаспорт: {patient_info[2]}\nМесто работы: {patient_info[3]}")
        else:
            messagebox.showerror("Ошибка", "Пациент не найден.")
        conn.close()

    def create_referral(self, doctor_id):
        medical_card_number = self.medical_card_entry.get()
        details = tk.simpledialog.askstring("Направление", "Введите детали направления:")

        if details:
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT id FROM patients WHERE medical_card_number = ?''', (medical_card_number,))
            patient = cursor.fetchone()

            if patient:
                cursor.execute('''INSERT INTO referrals (patient_id, doctor_id, details) VALUES (?, ?, ?)''',
                               (patient[0], doctor_id, details))
                conn.commit()
                messagebox.showinfo("Успех", "Направление успешно создано.")
            else:
                messagebox.showerror("Ошибка", "Пациент не найден.")
            conn.close()

    def track_movement(self, doctor_id):
        self.movement_window = tk.Toplevel(self)
        self.movement_window.title("Отслеживание перемещения")
        self.movement_window.geometry("800x600")

        self.canvas = tk.Canvas(self.movement_window, width=800, height=600, bg="white")
        self.canvas.pack()

        self.map_image = Image.open("hospital_map.png")  # Укажите путь к изображению карты больницы
        self.map_photo = ImageTk.PhotoImage(self.map_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.map_photo)

        self.persons = {}  # Хранит местоположение клиентов и сотрудников
        self.update_movement(doctor_id)

    def update_movement(self, doctor_id):
        try:
            response = requests.get("http://10.30.76.66:8082/PersonLocations")
            if response.status_code == 200:
                self.canvas.delete("person")  # Удалить предыдущие кружочки
                data = response.json()

                for person in data:
                    person_code = person['PersonCode']
                    role = person['PersonRole']
                    last_security_point_time = person['LastSecurityPointTime']
                    if role == "Клиент":
                        color = "green"
                    elif role == "Сотрудник":
                        color = "blue"
                    else:
                        continue

                    # Генерация случайных координат внутри помещения
                    x = random.randint(50, 750)
                    y = random.randint(50, 550)

                    # Добавление кружочка на карту
                    self.canvas.create_oval(x, y, x + 10, y + 10, fill=color, tags="person")
                    self.persons[person_code] = (x, y)

            # Повторное обновление через 3 секунды
            self.movement_window.after(3000, lambda: self.update_movement(doctor_id))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", "Не удалось получить данные о перемещении. Проверьте соединение.")


if __name__ == "__main__":
    setup_db()
    app = PatientRegistrationApp()
    app.mainloop()
