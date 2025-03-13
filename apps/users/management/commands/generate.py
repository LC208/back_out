import csv
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
    help = "Создает пользователей для компаний и экспортирует данные в CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            "--company_id", type=int, help="ID компании для создания пользователя"
        )

    def handle(self, *args, **options):
        company_id = options.get("company_id")
        companies = (
            Companies.objects.filter(id=company_id)
            if company_id
            else Companies.objects.all()
        )
        file_path = "companies_users.csv"

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(
                file,
                quoting=csv.QUOTE_MINIMAL,
                quotechar='"',
                escapechar="\\",
            )
            writer.writerow(["Название компании", "Username", "Password"])

            for company in companies:
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

                writer.writerow([cleaned_company_name, username, f"{password}"])

        self.stdout.write(self.style.SUCCESS(f"CSV-файл сохранен как {file_path}"))
