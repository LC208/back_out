import csv
from django.core.management.base import BaseCommand
from users.models import AuthsExtendedUser
from companies.models import Companies
from django.utils import timezone


def generate_random_password(length=10):
    """Генерирует случайный пароль (буквы, цифры, символы)."""
    import random
    import string

    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))


class Command(BaseCommand):
    help = "Создает пользователей для компаний и экспортирует данные в CSV"

    def handle(self, *args, **kwargs):
        companies = Companies.objects.all()
        file_path = "companies_users.csv"

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(
                file,
                quoting=csv.QUOTE_MINIMAL,  # Убираем экранирование для строк без запятых
                quotechar='"',  # Используем двойные кавычки для заключения строк
                escapechar="\\",  # Устанавливаем escape-символ (если нужно)
            )
            writer.writerow(["Название компании", "Username", "Password"])

            for company in companies:
                if not company.user:
                    username = f"P-I-{company.id:04d}"
                    password = generate_random_password()

                    # Создание пользователя через кастомную модель пользователя
                    user = AuthsExtendedUser.objects.create_user(
                        username=username,
                        password=password,
                        is_active=True,
                        date_joined=timezone.now(),  # Указываем текущую дату и время
                    )

                    # Связываем пользователя с компанией
                    company.user = user
                    company.save()

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Создан пользователь {username} для {company.name}"
                        )
                    )
                else:
                    username = company.user.username
                    password = "********"

                # Пишем данные компании, избавляясь от экранирования
                cleaned_company_name = (
                    company.name.replace("\n", " ").replace("\r", " ").strip()
                )

                writer.writerow([cleaned_company_name, username, f"{password}"])

        self.stdout.write(self.style.SUCCESS(f"CSV-файл сохранен как {file_path}"))
