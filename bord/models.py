from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


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
    user = models.ManyToManyField(User, blank=True)
    type = models.CharField(max_length=2, choices=TypeOfSubject.choices, default=TypeOfSubject.HOUSE)
    priority = models.CharField(max_length=3, choices=Priority.choices, default=Priority.HIGH)
    archived = models.BooleanField(default=False)
    address = models.CharField(max_length=200, blank=True)
    client_name = models.CharField(max_length=200, blank=True)
    client_number = models.CharField(max_length=200, blank=True)
    invent_number = models.CharField(max_length=10, blank=True)
    measured = models.BooleanField(default=False)
    drawn = models.BooleanField(default=False)
    calculated = models.BooleanField(default=False)
    typed = models.BooleanField(default=False)
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

    def get_typed(self):
        if self.typed:
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

    def get_comments_quantity1():
        return "1"


class Comment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if len(self.text) < 500:
            return self.text
        else:
            return f"{self.text[:500]}..."


class Subtask (models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    text = models.TextField()
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Task (models.Model):
    user = models.ManyToManyField(User, related_name='task')
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        users = ', '.join([user.username for user in self.user.all()])
        return f'{self.text}, ({users})'

    def users(self):
        users = '<br>'.join([user.username for user in self.user.all()])
        return users


class Contact (models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.subject}, {self.contact_name}"
