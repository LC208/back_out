import pandas as pd
from django.core.management.base import BaseCommand
from themes.models import Theme
from practices.models import Practice


class Command(BaseCommand):
    help = "Загружает темы из Excel в базу данных Django"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Путь к файлу Excel")
        parser.add_argument("practice_id", type=int, help="ID практики")
        parser.add_argument("--save", action="store_true", help="Сохраняет данные в БД")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        practice_id = kwargs["practice_id"]
        dry_run = not kwargs["save"]

        self.load_themes_from_excel(file_path, practice_id, dry_run)

    def load_themes_from_excel(self, file_path, practice_id, dry_run=True):
        """
        Читает Excel-файл и загружает темы в базу данных.
        :param file_path: путь к файлу Excel
        :param practice_id: ID практики
        :param dry_run: если True - только выводит темы, если False - записывает в БД
        """
        try:
            df = pd.read_excel(file_path, usecols=[0], names=["name"], dtype=str)
            df.dropna(inplace=True)
            themes = df["name"].tolist()

            if dry_run:
                self.stdout.write("Темы для добавления:")
                for theme in themes:
                    self.stdout.write(f"- {theme}")
            else:
                practice = Practice.objects.get(id=practice_id)
                for theme in themes:
                    Theme.objects.create(name=theme, practice=practice)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Добавлено {len(themes)} тем в практику {practice}"
                    )
                )

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ошибка: {e}"))
