import csv
import json
from django.core.management.base import BaseCommand
from apps.users.models import AuthsExtendedUser
from apps.companies.models import Companies
from django.utils import timezone


def generate_random_password(length=10):
    """Генерирует случайный пароль (буквы и цифры)."""
    import random
    import string

    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


class Command(BaseCommand):
    help = "Создает пользователей и компаний по JSON и экспортирует данные в CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            "--json_file", type=str, help="Путь к JSON-файлу со списком компаний"
        )

    def handle(self, *args, **options):
        json_file_path = options.get("json_file")
        if not json_file_path:
            self.stdout.write(
                self.style.ERROR("Укажите путь к JSON-файлу через --json_file")
            )
            return

        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка чтения JSON: {e}"))
            return

        companies_data = data.get("RecordSet", [])
        file_path = "companies_users.csv"

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(
                file,
                quoting=csv.QUOTE_MINIMAL,
                quotechar='"',
                escapechar="\\",
            )
            writer.writerow(
                ["ID компании", "Название компании", "Username", "Password"]
            )

            for item in companies_data:
                company_id = item.get("id")

                if company_id is None:
                    self.stdout.write(self.style.WARNING("Пропущена запись без ID"))
                    continue

                company = Companies.objects.filter(id=company_id).first()

                if not company:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Компания с ID {company_id} не найдена. Создаю..."
                        )
                    )

                    # Данные по умолчанию (можно добавить другие обязательные поля)
                    company_data = next(
                        item for item in companies_data if item["id"] == company_id
                    )
                    company_name = company_data.get(
                        "name", f"Неизвестная компания {company_id}"
                    )
                    company_dog = company_data.get("num", "")

                    company = Companies.objects.create(
                        id=company_id,
                        name=company_name,
                        agreement=company_dog,
                        argeement_date_begin="2025-03-08",
                        agreement_date_end="2025-03-08",
                    )

                    self.stdout.write(
                        self.style.SUCCESS(f"Создана новая компания: {company_name}")
                    )

                if not company.user:
                    username = f"P-I-{company.id:04d}"
                    password = generate_random_password()

                    user = AuthsExtendedUser.objects.create_user(
                        username=username,
                        password=password,
                        is_active=True,
                        date_joined=timezone.now(),
                    )

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

                cleaned_company_name = (
                    company.name.replace("\n", " ").replace("\r", " ").strip()
                )
                writer.writerow([company.id, cleaned_company_name, username, password])

        self.stdout.write(self.style.SUCCESS(f"CSV-файл сохранен как {file_path}"))
