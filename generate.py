import csv
import random
import string
from django.contrib.auth.models import User
from companies.models import Companies


def generate_random_password(length=8):
    """Генерирует случайный пароль (буквы, цифры, символы)."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))


def generate_username():
    """Генерирует username в формате P-I-****."""
    return f"P-I-{random.randint(1000, 9999)}"


def create_users_and_generate_csv(file_path="companies_users.csv"):
    companies = Companies.objects.all()

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Название компании", "Username", "Password"])  # Заголовки CSV

        for company in companies:
            if not company.user:
                username = generate_username()
                password = generate_random_password()

                # Создаем пользователя
                user = User.objects.create_user(username=username, password=password)
                company.user = user
                company.save()
            else:
                username = company.user.username
                password = (
                    "********"  # Если пользователь уже существует, скрываем пароль
                )

            writer.writerow([company.name, username, password])

    print(f"CSV-файл сохранен как {file_path}")


# Запуск функции
create_users_and_generate_csv()
