from django.db import models
from django.utils.translation import gettext_lazy as _


class Subject(models.Model):

    class TypeOfSubject(models.TextChoices):
        BUILDING = 'BU', _('Багатоповерхівка')
        COMMERCE = 'CO', _('Будівля')
        GARAGE = 'GA', _('Гараж')
        HOUSE = 'HO', _('Особняк')
        APARTMENT = 'AP', _('Квартира')
        KEV = 'KE', _('КЕВ')
        QUARTERS = 'QU', _('Нежитлове приміщення')
        UNFINISHED = 'UF', _('Незавершене')
        SUMMERHOUSE = 'SH', _('Садовий будинок')

    class Priority(models.TextChoices):
        HIGH = 'AA', _('Високий')
        NORMAL = 'BB', _('Звичайний')
        LOW = 'CC', _('Низький')

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=2, choices=TypeOfSubject.choices, default=TypeOfSubject.HOUSE)
    priority = models.CharField(max_length=3, choices=Priority.choices, default=Priority.NORMAL)
    address = models.CharField(max_length=200, blank=True)
    invent_number = models.CharField(max_length=10, blank=True)
    measured = models.BooleanField(default=False)
    drawn = models.BooleanField(default=False)
    calculated = models.BooleanField(default=False)
    numbered = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    def get_measured(self):
        if self.measured:
            return 'btn btn-success'
        else:
            return 'btn btn-danger'

    def get_drawn(self):
        if self.drawn:
            return 'btn btn-success'
        else:
            return 'btn btn-danger'

    def get_calculated(self):
        if self.calculated:
            return 'btn btn-success'
        else:
            return 'btn btn-danger'

    def get_numbered(self):
        if self.numbered:
            return 'btn btn-success'
        else:
            return 'btn btn-danger'

    def get_done(self):
        if self.done:
            return 'btn btn-success'
        else:
            return 'btn btn-danger'

    def get_priority(self):
        if self.priority == 'AA':
            return '#ffb3b3'
        if self.priority == 'BB':
            return '#fffa75'
        if self.priority == 'CC':
            return '#9bff99'


class Comment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.text) < 100:
            return self.text
        else:
            return f"{self.text[:100]}..."
