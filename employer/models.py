# employer/models.py
from django.db import models
from django.contrib.auth.models import User

STATE_AWARDS = [
    ('hero', 'Кыргыз Республикасынын Баатыры'),
    ('manas', 'Орден "Манас"'),
    ('kurmanjan', 'Орден "Курманжан Датка"'),
    ('baatyr_ene', 'Орден "Баатыр эне"'),
    ('danaker', 'Орден "Данакер"'),
    ('erdik', 'Орден "Эрдик"'),
    ('dank', 'Медаль "Данк"'),
    ('ene_danky', 'Медаль "Эне данкы"'),
    ('kujurmon', 'Медаль "Кужурмож кызмат отогондугу учун"'),
    ('charity', 'Медаль "Кайрымдуулук учун" ("За благотворительность")'),
    ('emgek', 'Медаль "Эмгек ардагери" ("Ветеран труда")'),
    ('honorary_gramota', 'Почетная грамота Кыргызской Республики'), 
]

FACULTIES = [
    ('atf', 'Аграрно-технический факультет'),
    ('pedfac', 'Педагогический факультет'),
    ('filfac', 'Филологический факультет'),
    ('econom_fac', 'Факультет экономики, менеджмента и физического воспитания'),
]

HONORARY_TITLES = [
    ('writer', 'Народный писатель Кыргызской Республики'),
    ('poet', 'Народный поэт Кыргызской Республики'),
    ('artist', 'Народный художник Кыргызской Республики'),
    ('actor', 'Народный артист Кыргызской Республики'),
    ('teacher', 'Народный учитель Кыргызской Республики'),
    ('z_teacher', 'Заслуженный учитель Кыргызской Республики'),

    ('z_edu_worker', 'Заслуженный работник образования Кыргызской Республики'),
    ('z_doctor', 'Заслуженный врач Кыргызской Республики'),
    ('z_health_worker', 'Заслуженный работник здравоохранения Кыргызской Республики'),
    ('z_actor', 'Заслуженный артист Кыргызской Республики'),
    ('z_culture', 'Заслуженный деятель культуры Кыргызской Республики'),
    ('z_science', 'Заслуженный деятель науки Кыргызской Республики'),
    ('z_industry', 'Заслуженный работник промышленности Кыргызской Республики'),
    ('z_agriculture', 'Заслуженный работник сельского хозяйства Кыргызской Республики'),
    ('z_builder', 'Заслуженный строитель Кыргызской Республики'),
    ('z_transport', 'Заслуженный работник транспорта Кыргызской Республики'),
    ('z_communication', 'Заслуженный работник связи Кыргызской Республики'),
    ('z_geology', 'Заслуженный работник геологической службы Кыргызской Республики'),
    ('z_services', 'Заслуженный работник сферы обслуживания населения Кыргызской Республики'),
    ('z_lawyer', 'Заслуженный юрист Кыргызской Республики'),
    ('z_economist', 'Заслуженный экономист Кыргызской Республики'),
    ('z_ecology', 'Заслуженный работник охраны природы Кыргызской Республики'),
    ('z_coach', 'Заслуженный тренер Кыргызской Республики'),
    ('z_master_sport', 'Заслуженный мастер спорта Кыргызской Республики'),
    ('z_inventor', 'Заслуженный изобретатель Кыргызской Республики'),
    ('z_sport_worker', 'Заслуженный работник физической культуры и спорта Кыргызской Республики'),
    ('z_state_worker', 'Заслуженный работник государственной службы Кыргызской Республики'),
    ('z_local_gov', 'Заслуженный работник местного самоуправления Кыргызской Республики'),
]


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employer_profile")
    
    last_name = models.CharField("Фамилия", max_length=50)
    first_name = models.CharField("Имя", max_length=50)
    middle_name = models.CharField("Отчество", max_length=50, blank=True, null=True)
    birth_date = models.DateField("Дата рождения", blank=True, null=True)
    position = models.CharField("Должность", max_length=100, blank=True, null=True)
    department = models.CharField("Отдел", max_length=100, blank=True, null=True)
    faculty = models.CharField("Факультет", choices=FACULTIES, max_length=100, blank=True, null=True)
    hire_date = models.DateField("Дата приема на работу", blank=True, null=True)

    def __str__(self):
        return f"{self.last_name or ''} {self.first_name or ''}".strip()


class Award(models.Model):
    TYPE_CHOICES = [
        ('state', 'Государственная'),
        ('honorary', 'Почётное звание (Ардак наам)'),
        ('department', 'Ведомственная'),
    ]

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name="awards")
    type = models.CharField("Категория награды", max_length=20, choices=TYPE_CHOICES)

    state_award = models.CharField("Гос. награда", max_length=100, choices=STATE_AWARDS, blank=True, null=True)
    honorary_title = models.CharField("Почётное звание", max_length=100, choices=HONORARY_TITLES, blank=True, null=True)
    title = models.CharField("Наименование награды", max_length=200, blank=True, null=True)

    award_date = models.DateField("Дата награждения")
    issued_by = models.CharField("Кем выдано", max_length=200)
    description = models.TextField("Описание", blank=True, null=True)
    document_number = models.CharField("Приказ №", max_length=100, blank=True, null=True)

    def __str__(self):
        if self.type == 'state' and self.state_award:
            return dict(STATE_AWARDS).get(self.state_award, self.state_award)
        elif self.type == 'honorary' and self.honorary_title:
            return dict(HONORARY_TITLES).get(self.honorary_title, self.honorary_title)
        return self.title or "Награда"


