from django import forms

from .models import Subject, Comment, Subtask


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'type', 'address', 'invent_number']
        labels = {'name': 'Назва', 'type': 'Тип', 'address': 'Адреса', 'invent_number': 'Інвентаризаційний номер'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


class SubtaskForm(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}