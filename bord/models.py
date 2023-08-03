from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=200)
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


class Comment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.text) < 100:
            return self.text
        else:
            return f"{self.text[:100]}..."
