# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название института")
    picture = models.CharField(max_length=1000, verbose_name="Адрес на картинку")

    def __str__(self):
        return self.name or f"Институт {self.id}"

    class Meta:
        managed = False
        db_table = 'faculty'
        verbose_name = "Институт"
        verbose_name_plural = "Институты"

class Speciality(models.Model):
    url = models.SlugField(max_length=200, null=True)
    code = models.CharField(max_length=255, blank=True, null=True, verbose_name="Код специальности")
    full_name = models.CharField(max_length=512, blank=False, null=True, verbose_name="Название специальности")
    # education_level = models.CharField(max_length=64, choices=EducationLevel.choices, null=True)
    education_level = models.SmallIntegerField(blank=False, null=True, verbose_name="Уровень образования")
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name="specialities"
    )

    def __str__(self):
        return self.full_name or self.code or self

    class Meta:
        managed = False
        db_table = 'base_speciality'
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"


class Companies(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название компании")
    themes = models.CharField(max_length=255, blank=True, null=True, verbose_name="Темы")
    dbegin = models.CharField(max_length=255, blank=True, null=True, verbose_name="Дата начала")
    dend = models.CharField(max_length=255, blank=True, null=True, verbose_name="Дата окончания")
    agreements = models.CharField(max_length=255, blank=True, null=True, verbose_name="Соглашения")
    image = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Ссылка на изображение")
    user = models.OneToOneField(User, models.DO_NOTHING, blank=True, null=True, verbose_name="Представитель")
    area_of_activity = models.TextField(max_length=2000, blank=True, null=True, verbose_name="Область деятельности")
    head_full_name = models.CharField(max_length=128, blank=True, null=True, verbose_name="ФИО руководителя")
    head_job_title = models.CharField(max_length=512, blank=True, null=True, verbose_name="Должность руководителя")

    def __str__(self):
        return self.name or f"Компания {self.id}"

    class Meta:
        managed = False
        db_table = 'companies'
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

class CompanyRepresentativeProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    job_title = models.CharField(max_length=512, blank=True, null=True, verbose_name="Должность")
    messenger = models.CharField(max_length=128, blank=True, null=True, verbose_name="Уникальное имя в мессенджере") # TODO написать флаг unique
    email = models.CharField(max_length=254, verbose_name="Почта")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, null=False, verbose_name="Аккаунт")

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return f"Представитель {self.user}"

    class Meta:
        verbose_name = "Представитель компании"
        verbose_name_plural = "Представители компаний"

class Practice(models.Model): 
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название практики")
    company = models.ForeignKey(
        Companies, on_delete=models.DO_NOTHING, related_name="company"
    )
    faculty = models.ForeignKey(
        Faculty, on_delete=models.DO_NOTHING, related_name="faculty"
    )   


    # здесь и других моделях есть колхозная проверка на None,
    #  так как в параметрах атрибутов Null=True
    def __str__(self):
        return self.name or f"Практика {self.id}"

    class Meta:
        managed = False
        db_table = 'base_practice'
        verbose_name = "Практика"
        verbose_name_plural = "Практики"

class Theme(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название темы")
    practice = models.ForeignKey(Practice, models.DO_NOTHING, blank=True, null=True, verbose_name="Практика",related_name="themes")

    def __str__(self):
        return self.name or f"Тема {self.id}"

    class Meta:
        managed = False
        db_table = 'base_theme'
        verbose_name = "Тема"
        verbose_name_plural = "Темы"


class DocLink(models.Model):
    type = models.TextField(verbose_name="Тип")
    url = models.CharField(max_length=1000, verbose_name="URL")
    practice = models.ForeignKey(
        Practice, on_delete=models.CASCADE, related_name="doc_links"
    )

    def __str__(self):
        return f"{self.practice_id}|{self.type} ({self.url})"

    class Meta:
        managed = False
        db_table = 'base_doclink'
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

class DivisionsInst(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название подразделения")
    faculty = models.ForeignKey('Faculty', models.DO_NOTHING, blank=True, null=True, verbose_name="Факультет")

    def __str__(self):
        return self.name or f"Подразделение {self.id}"

    class Meta:
        managed = False
        db_table = 'divisions_inst'
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"




class Groups(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Номер группы")
    stream = models.ForeignKey('Streams', models.DO_NOTHING, blank=True, null=True, verbose_name="Поток")

    def __str__(self):
        if self.stream and self.group_number:
            return f"{str(self.stream)} - {self.group_number}"
        return f"Группа ({self.id})"

    class Meta:
        managed = False
        db_table = 'groups'
        verbose_name = "Группа"
        verbose_name_plural = "Группы"





class Profiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название специальности")
    faculty = models.ForeignKey(Faculty, models.DO_NOTHING, blank=True, null=True, verbose_name="Институт")

    def __str__(self):
        return self.name or f"Специальность ({self.id})"

    class Meta:
        managed = False
        db_table = 'profiles'
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"


class Streams(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название потока сокр.")
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Полное название потока")
    code = models.CharField(max_length=255, blank=True, null=True, verbose_name="Код потока")
    year = models.CharField(max_length=255, blank=True, null=True, verbose_name="Год поступления")
    profile = models.ForeignKey(Profiles, models.DO_NOTHING, blank=True, null=True, verbose_name="Специальность")

    def __str__(self):
        if self.name and self.code and self.year:
            return f"{self.name}-{self.year}-{self.code}"
        return f"Поток ({self.id})"

    class Meta:
        managed = False
        db_table = 'streams'
        verbose_name = "Поток"
        verbose_name_plural = "Потоки"


class StudentOtchet(models.Model):

    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey('Students', models.DO_NOTHING, blank=True, null=True, verbose_name="Студент")
    link_ya = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ссылка на Яндекс")
    status = models.BigIntegerField(blank=True, null=True, verbose_name="Статус")

    class Meta:
        managed = False
        db_table = 'student_otchet'
        verbose_name = "Отчетность выгрузки отчета"
        verbose_name_plural = "Отчетности выгрузки отчета"


class StudentPractic(models.Model):
    """
    Запись студентов на практику
    """

    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey('Students', models.DO_NOTHING, blank=True, null=True, verbose_name="Студент")
    company = models.ForeignKey(Companies, models.DO_NOTHING, blank=True, null=True, verbose_name="Компания")
    teacher = models.ForeignKey('TeacherScore', models.DO_NOTHING, blank=True, null=True, verbose_name="Преподаватель")
    theme = models.CharField(max_length=255, blank=True, null=True, verbose_name="Тема практики")
    status = models.BigIntegerField(blank=True, null=True, verbose_name="Статус согласования") # TODO сделать IntegerChoice
    company_path = models.CharField(max_length=255, blank=True, null=True, verbose_name="Путь к компании")

    class Meta:
        managed = False
        db_table = 'student_practic'
        verbose_name = "Запись студента"
        verbose_name_plural = "Записи студентов"



class Students(models.Model):
    id = models.BigAutoField(primary_key=True)
    fio = models.CharField(max_length=255, blank=True, null=True, verbose_name="ФИО")
    group = models.ForeignKey(Groups, models.DO_NOTHING, blank=True, null=True, verbose_name="Группа")
    category = models.CharField(max_length=255, blank=True, null=True, verbose_name="Категория")
    mira_id = models.BigIntegerField(blank=True, null=True, verbose_name="Mira ID")

    def __str__(self):
        return self.fio if self.fio else f"Студент ({self.id})"

    class Meta:
        managed = False
        db_table = 'students'
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"


class TeacherScore(models.Model):
    id = models.BigAutoField(primary_key=True)
    teacher = models.ForeignKey('Teachers', models.DO_NOTHING, blank=True, null=True, verbose_name="Преподаватель")
    score = models.FloatField(blank=True, null=True, verbose_name="Рейтинг")

    def __str__(self):
        if self.teacher.fio and self.score:
            return f"{self.teacher.fio}, {self.score}"
        return f"Нагрузка преподавателя ({self.id})"

    class Meta:
        managed = False
        db_table = 'teacher_score'
        verbose_name = "Нагрузка на преподавателей"
        verbose_name_plural = "Нагрузка на преподавателей"


class Teachers(models.Model):
    id = models.BigAutoField(primary_key=True)
    fio = models.CharField(max_length=255, blank=True, null=True, verbose_name="ФИО")
    post = models.CharField(max_length=255, blank=True, null=True, verbose_name="Должность")
    work_load = models.BigIntegerField(blank=True, null=True, verbose_name="Нагрузка")
    mira_id = models.BigIntegerField(blank=True, null=True, verbose_name="Mira ID")
    fac = models.ForeignKey(Faculty, models.DO_NOTHING, blank=True, null=True, verbose_name="Институт")

    def __str__(self):
        return self.fio or f"Преподаватель ({self.id})"

    class Meta:
        managed = False
        db_table = 'teachers'
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"


class Templates(models.Model):
    """
    Таблица отчетности зачисления студентческих групп на практику
    """

    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(Groups, models.DO_NOTHING, blank=True, null=True, verbose_name="Группа")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Путь до файла отчета")
    decanat_check = models.BigIntegerField(blank=True, null=True, verbose_name="Согласие деканата")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="Комментарий деканата")
    date = models.CharField(max_length=255, blank=True, null=True, verbose_name="Дата комментария")

    class Meta:
        managed = False
        db_table = 'templates'
        verbose_name = "Отчетность зачисления групп"
        verbose_name_plural = "Отчетность зачисления групп"

