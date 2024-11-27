from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column, Div, ButtonHolder, HTML
from .models import Subject, Comment, Subtask, Task, Contact
from crispy_forms.bootstrap import InlineRadios, FormActions



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


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['text', ]
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['contact_name', 'contact_number']
        labels = {'contact_name': "Ім'я", 'contact_number': 'Номер телефону'}


'''class SubjectFilterForm(forms.Form):
    TYPE_CHOICES = [
        ('', 'Усі типи'),
        ('BU', 'Багатоповерхівка'),
        ('CO', 'Будівля'),
        ('GA', 'Гараж'),
        ('HO', 'Особняк'),
        ('AP', 'Квартира'),
        ('KE', 'КЕВ'),
        ('QU', 'Нежитлове приміщення'),
        ('UF', 'Незавершене'),
        ('SH', 'Садовий будинок'),
    ]

    PRIORITY_CHOICES = [
        ('', 'Усі пріоритети'),
        ('AA', 'Високий'),
        ('BB', 'Звичайний'),
        ('CC', 'Низький'),
    ]

    BOOLEAN_CHOICES = [
        ('', 'Будь-яке'),
        ('True', 'Так'),
        ('False', 'Ні'),
    ]

    type = forms.ChoiceField(label='Тип', choices=TYPE_CHOICES, required=False)
    priority = forms.ChoiceField(label='Пріоритет', choices=PRIORITY_CHOICES, required=False)

    measured = forms.ChoiceField(
        label='Поміряно',
        choices=[('', 'Будь-яке'), ('True', 'Так'), ('False', 'Ні')],
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'})
    )
    drawn = forms.ChoiceField(
        label='Намальовано',
        choices=[('', 'Будь-яке'), ('True', 'Так'), ('False', 'Ні')],
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'})
    )
    calculated = forms.ChoiceField(
        label='Пораховано',
        choices=[('', 'Будь-яке'), ('True', 'Так'), ('False', 'Ні')],
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'})
    )
    typed = forms.ChoiceField(
        label='Набрано',
        choices=[('', 'Будь-яке'), ('True', 'Так'), ('False', 'Ні')],
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'})
    )
    numbered = forms.ChoiceField(
        label='Пронумеровано',
        choices=[('', 'Будь-яке'), ('True', 'Так'), ('False', 'Ні')],
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'})
    )
    done = forms.ChoiceField(
        label='Виконано',
        choices=[('', 'Будь-яке'), ('True', 'Так'), ('False', 'Ні')],
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'})
    )

    def __init__(self, *args, **kwargs):
        super(SubjectFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('type', css_class='col-md-6'),
                Column('priority', css_class='col-md-6'),
            ),
            Div(
                Row(
                    Column('measured', css_class='col-md-4'),
                    Column('drawn', css_class='col-md-4'),
                    Column('calculated', css_class='col-md-4'),
                ),
                Row(
                    Column('typed', css_class='col-md-4'),
                    Column('numbered', css_class='col-md-4'),
                    Column('done', css_class='col-md-4'),
                ),
                css_class='btn-group-toggle',
            ),
            FormActions(
                Submit('submit', 'Фільтрувати', css_class='btn btn-primary'),
                css_class='mt-4',
            )
        )'''
class SubjectFilterForm(forms.Form):
    TYPE_CHOICES = [
        ('', 'Усі типи'),
        ('BU', 'Багатоповерхівка'),
        ('CO', 'Будівля'),
        ('GA', 'Гараж'),
        ('HO', 'Особняк'),
        ('AP', 'Квартира'),
        ('KE', 'КЕВ'),
        ('QU', 'Нежитлове приміщення'),
        ('UF', 'Незавершене'),
        ('SH', 'Садовий будинок'),
    ]

    PRIORITY_CHOICES = [
        ('', 'Усі пріоритети'),
        ('AA', 'Високий'),
        ('BB', 'Звичайний'),
        ('CC', 'Низький'),
    ]

    BOOLEAN_CHOICES = [
        ('', 'Будь-яке'),
        ('True', 'Так'),
        ('False', 'Ні'),
    ]

    type = forms.ChoiceField(label='Тип', choices=TYPE_CHOICES, required=False)
    priority = forms.ChoiceField(label='Пріоритет', choices=PRIORITY_CHOICES, required=False)

    measured = forms.ChoiceField(label='Поміряно', choices=BOOLEAN_CHOICES, required=False)
    drawn = forms.ChoiceField(label='Намальовано', choices=BOOLEAN_CHOICES, required=False)
    calculated = forms.ChoiceField(label='Пораховано', choices=BOOLEAN_CHOICES, required=False)
    typed = forms.ChoiceField(label='Набрано', choices=BOOLEAN_CHOICES, required=False)
    numbered = forms.ChoiceField(label='Пронумеровано', choices=BOOLEAN_CHOICES, required=False)
    done = forms.ChoiceField(label='Виконано', choices=BOOLEAN_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super(SubjectFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Div(
                Field('type', css_class='form-select'),
                Field('priority', css_class='form-select'),
                Div(
                    Div(
                        HTML('<p>Поміряно: </p>'),
                        css_class='col-sm-4'
                    ),
                    Div(
                        Div(
                            HTML(
                                '<input type="radio" class="btn-check"  name="measured" value="True" id="measured-true" autocomplete="off" onclick="toggleRadio(this);"><label class="btn btn-outline-success" for="measured-true">Так</label>'),
                            HTML(
                                '<input type="radio" class="btn-check" name="measured" value="False" id="measured-false" autocomplete="off" onclick="toggleRadio(this);"><label class="btn btn-outline-danger" for="measured-false">Ні</label>'),
                            css_class='btn-group'
                        ),
                        css_class='col-sm-6'
                    ),
                    css_class='row mb-3'
                ),
                Div(
                    Div(
                        HTML('<p>Накреслено: </p>'),
                        css_class='col-sm-4'
                    ),
                    Div(
                        Div(
                            HTML(
                                '<input type="radio" class="btn-check"  name="drawn" value="True" id="drawn-true" autocomplete="off" onclick="toggleRadio(this);"><label class="btn btn-outline-success" for="drawn-true">Так</label>'),
                            HTML(
                                '<input type="radio" class="btn-check" name="drawn" value="False" id="drawn-false" autocomplete="off" onclick="toggleRadio(this);"><label class="btn btn-outline-danger" for="drawn-false">Ні</label>'),
                            css_class='btn-group'
                        ),
                        css_class='col-sm-6'
                    ),
                    css_class='row mb-3'
                ),

                Div(
                    Div(
                        HTML('<p>Пораховано: </p>'),
                        css_class='col-sm-4'
                    ),
                    Div(
                        Div(
                            HTML(
                                '<input type="radio" class="btn-check"  name="calculated" value="True" id="calculated-true" autocomplete="off" onclick="toggleRadio(this);"><label class="btn btn-outline-success" for="calculated-true">Так</label>'),
                            HTML(
                                '<input type="radio" class="btn-check" name="calculated" value="False" id="calculated-false" autocomplete="off" onclick="toggleRadio(this);"><label class="btn btn-outline-danger" for="calculated-false">Ні</label>'),
                            css_class='btn-group'
                        ),
                        css_class='col-sm-6'
                    ),
                    css_class='row mb-3'
                ),

                Div(
                    Div(
                        HTML('<p>Розставлено: </p>'),
                        css_class='col-sm-4'
                    ),
                    Div(
                        Div(
                            HTML(
                                '<input type="radio" class="btn-check"  name="numbered" value="True" id="numbered-true" autocomplete="off" onclick="toggleRadio(this);"><label class="btn btn-outline-success" for="numbered-true">Так</label>'),
                            HTML(
                                '<input type="radio" class="btn-check" name="numbered" value="False" id="numbered-false" autocomplete="off" onclick="toggleRadio(this);"><label class="btn btn-outline-danger" for="numbered-false">Ні</label>'),
                            css_class='btn-group'
                        ),
                        css_class='col-sm-6'
                    ),
                    css_class='row mb-3'
                ),

                Div(
                    Div(
                        HTML('<p>Набрано: </p>'),
                        css_class='col-sm-4'
                    ),
                    Div(
                        Div(
                            HTML(
                                '<input type="radio" class="btn-check"  name="typed" value="True" id="typed-true" autocomplete="off" onclick="toggleRadio(this);"><label class="btn btn-outline-success" for="typed-true">Так</label>'),
                            HTML(
                                '<input type="radio" class="btn-check" name="typed" value="False" id="typed-false" autocomplete="off" onclick="toggleRadio(this);"><label class="btn btn-outline-danger" for="typed-false">Ні</label>'),
                            css_class='btn-group'
                        ),
                        css_class='col-sm-6'
                    ),
                    css_class='row mb-3'
                ),

                Div(
                    Div(
                        HTML('<p>Готово: </p>'),
                        css_class='col-sm-4'
                    ),
                    Div(
                        Div(
                            HTML(
                                '<input type="radio" class="btn-check"  name="done" value="True" id="done-true" autocomplete="off" onclick="toggleRadio(this);"><label class="btn btn-outline-success" for="done-true">Так</label>'),
                            HTML(
                                '<input type="radio" class="btn-check" name="done" value="False" id="done-false" autocomplete="off" onclick="toggleRadio(this);"><label class="btn btn-outline-danger" for="done-false">Ні</label>'),
                            css_class='btn-group'
                        ),
                        css_class='col-sm-6'
                    ),
                    css_class='row mb-3'
                ),


                FormActions(
                    HTML('<button type="submit" class="btn btn-primary me-1">Фільтрувати</button>'),
                    HTML('<button type="button" class="btn btn-secondary" onclick="resetFilters()">Скинути фільтри</button>'),

                    css_class='mt-3'
                ),
                css_class='mb-3'
            ),
        )