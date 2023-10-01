from django import forms

from .models import Subject, Comment, Subtask


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'client_name', 'client_number', 'type', 'address', 'invent_number']
        labels = {
            'name': 'Назва',
            'client_name': "Ім'я замовника",
            'client_number': 'Номер телефону',
            'type': 'Тип',
            'address': 'Адреса',
            'invent_number': 'Інвентаризаційний номер'
        }


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