import json
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage
from django.forms import modelform_factory
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _

from .models import Subject, Comment, Subtask, User, Task, Contact
from .forms import SubjectForm, CommentForm, SubtaskForm, TaskForm, ContactForm, SubjectFilterForm


def get_status_class(subject, status):
    if getattr(subject, status):
        return "btn btn-success"
    else:
        return "btn btn-secondary"


def get_new_class(subject, status):
    if getattr(subject, status):
        return "btn btn-secondary"
    else:
        return "btn btn-success"


def index(request):
    filter_form = SubjectFilterForm(request.GET)
    subjects = Subject.objects.all()

    if filter_form.is_valid():
        data = filter_form.cleaned_data
        if data.get('type'):
            subjects = subjects.filter(type=data['type'])
        if data.get('priority'):
            subjects = subjects.filter(priority=data['priority'])

        task_fields = ['measured', 'drawn', 'calculated', 'typed', 'numbered', 'done']
        for field in task_fields:
            if field in data and data[field] != '':
                subjects = subjects.filter(**{field: data[field]})

    subjects = subjects.order_by('priority', '-date_added')

    # Пагінація
    paginator = Paginator(subjects, 15)  # 15 об'єктів на сторінку
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        return HttpResponse('')

    for subject in page_obj:
        subject.unfinished_subtasks_count = subject.subtask_set.filter(done=False).count()
        subject.status_classes = {status: get_status_class(subject, status) for status in task_fields}
        subject.new_classes = {status: get_new_class(subject, status) for status in task_fields}

        # Обробка HTMX-запиту
    if request.headers.get('HX-Request'):
        return render(request, 'bord/partials/subject_list.html', {'subjects': page_obj})

    subjects_count = paginator.count
    context = {'subjects': page_obj, 'subjects_count': subjects_count, 'filter_form': filter_form}

    return render(request, 'bord/index.html', context)

@login_required()
def search_view(request):
    query = request.GET.get('query', '')
    if query:
        results = Subject.objects.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(client_name__icontains=query) |
            Q(client_number__icontains=query) |
            Q(invent_number__icontains=query)
        )
    else:
        results = []
    print(f'query: {query}')

    return render(request, 'bord/search_results.html', {'results': results, 'query': query})


@login_required()
def archive(request):
    subjects = Subject.objects.order_by('-date_added')
    subjects_count = Subject.objects.filter(archived=True).count()
    context = {'subjects': subjects, 'subjects_count': subjects_count}
    return render(request, 'bord/archive.html', context)


@login_required()
def my_subjects(request):
    filter_form = SubjectFilterForm(request.GET)
    subjects = Subject.objects.filter(user=request.user)

    if filter_form.is_valid():
        data = filter_form.cleaned_data
        if data.get('type'):
            subjects = subjects.filter(type=data['type'])
        if data.get('priority'):
            subjects = subjects.filter(priority=data['priority'])

        task_fields = ['measured', 'drawn', 'calculated', 'typed', 'numbered', 'done']
        for field in task_fields:
            if field in data and data[field] != '':
                subjects = subjects.filter(**{field: data[field]})

    subjects = subjects.order_by('priority', '-date_added')
    subjects_count = subjects.filter(archived=False).count()
    context = {'subjects': subjects, 'subjects_count': subjects_count, 'filter_form': filter_form}

    for subject in subjects:
        subject.unfinished_subtasks_count = subject.subtask_set.filter(done=False).count()

    return render(request, 'bord/my_subjects.html', context)


@login_required()
def take_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    user = request.user
    if user in subject.user.all():
        subject.user.remove(user)
    else:
        subject.user.add(user)
    return redirect('bord:subject', subject_id=subject.id)


@login_required()
def todo(request):
    user = request.user
    tasks = Task.objects.filter(user=user).order_by('done', '-date_added')
    subjects = Subject.objects.filter(subtask__isnull=False).distinct()
    subjects_with_incomplete_subtasks = []
    for subject in subjects:
        if subject.subtask_set.filter(done=False).exists():
            subject.subtasks_sorted = subject.subtask_set.all().order_by('done', 'id')
            subjects_with_incomplete_subtasks.append(subject)

    context = {'tasks': tasks, 'subjects': subjects_with_incomplete_subtasks}
    return render(request, 'bord/todo.html', context)


@login_required()
def subject_view(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    users = subject.user.all()
    comments = subject.comment_set.order_by('-date_added')
    subtasks = subject.subtask_set.order_by('done', 'id')
    contacts = subject.contact_set.all().order_by('id')
    context = {'subject': subject, 'comments': comments, 'subtasks': subtasks, 'contacts': contacts, 'users': users}
    return render(request, 'bord/subject.html', context)


@login_required()
def new_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        contacts_data = json.loads(request.POST.get('contacts', '[]'))  # Отримуємо контакти у вигляді JSON

        if form.is_valid():
            new_subject = form.save(commit=False)
            new_subject.save()
            new_subject.user.add(request.user)

            # Створюємо контакти та зв’язуємо їх із новим суб'єктом
            for contact in contacts_data:
                Contact.objects.create(
                    subject=new_subject,
                    contact_name=contact['contact_name'],
                    contact_number=contact['contact_number']
                )

            return HttpResponse(status=200, headers={'HX-Redirect': reverse('bord:index')})

        return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'bord/new_subject.html', {'form': SubjectForm()})


def contacts_view(request):
    contacts = Contact.objects.all().order_by('contact_name')
    return render(request, 'bord/contacts_list.html', {'contacts' : contacts})


def contact_form_partial(request):
    form = ContactForm()
    return render(request, 'bord/partials/contact_form_partial.html', {'form': form})


@login_required()
def edit_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)

    if request.method != 'POST':
        form = SubjectForm(instance=subject)
    else:
        form = SubjectForm(instance=subject, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bord:subject', subject_id=subject.id)

    contacts = subject.contact_set.all().order_by('id')
    context = {'subject': subject, 'form': form, 'contacts': contacts}
    return render(request, 'bord/edit_subject.html', context)


@login_required()
def delete_subject(*args, subject_id):
    subject = Subject.objects.get(id=subject_id)

    subject.delete()
    return redirect('bord:index')


@login_required()
def new_comment(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            try:
                new_comment = form.save(commit=False)
                new_comment.author = request.user
                new_comment.subject = subject
                new_comment.save()
                return redirect('bord:subject', subject_id=subject_id)
            except:
                return redirect('users:login')

    context = {'subject': subject, 'form': form}
    return render(request, 'bord/new_comment.html', context)


@login_required()
def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    subject = comment.subject

    if request.method != 'POST':
        form = CommentForm(instance=comment)
    else:
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bord:subject', subject_id=subject.id)

    context = {'comment': comment, 'subject': subject, 'form': form}
    return render(request, 'bord/edit_comment.html', context)


@login_required()
def delete_comment(*args, comment_id):
    comment = Comment.objects.get(id=comment_id)
    subject = comment.subject

    comment.delete()
    return redirect('bord:subject', subject_id=subject.id)


@login_required()
def change_status(request, subject_id, field):
    subject = Subject.objects.get(id=subject_id)
    field_value = getattr(subject, field)
    setattr(subject, field, not field_value)
    subject.save()
    return redirect('bord:index')


@login_required()
def change_priority(request, subject_id, priority):
    subject = Subject.objects.get(id=subject_id)
    subject.priority = priority
    subject.save()
    return redirect('bord:index')


@login_required()
def add_to_archive(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    user = request.user

    if subject.archived:
        subject.archived = False
        subject.done = False
        subject.user.clear()
        subject.user.add(user)
        subject.save()
    else:
        subject.archived = True
        subject.user.clear()
        subject.save()

    return redirect('bord:index')


@login_required()
def new_subtask(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    if request.method != 'POST':
        form = SubtaskForm()
    else:
        form = SubtaskForm(data=request.POST)
        if form.is_valid():
            new_subtask = form.save(commit=False)
            new_subtask.subject = subject
            new_subtask.save()
            return redirect('bord:subject', subject_id=subject_id)

    context = {'subject': subject, 'form': form}
    return render(request, 'bord/new_subtask.html', context)


@login_required()
def check_subtask(request, subtask_id):
    subtask = get_object_or_404(Subtask, id=subtask_id)
    subject = subtask.subject
    subtask.done = not subtask.done
    subtask.save()
    subtasks = Subtask.objects.filter(subject=subject).order_by('done', 'id')

    return render(request, 'bord/partials/subtask_list.html', {'subtasks': subtasks})


@login_required()
def todo_check_subtask(request, subtask_id):
    subtask = get_object_or_404(Subtask, id=subtask_id)
    subtask.done = not subtask.done
    subtask.save()
    return render(request, 'bord/partials/subtask_partial.html', {'subtask': subtask})


@login_required()
def edit_subtask(request, subtask_id):
    subtask = Subtask.objects.get(id=subtask_id)
    subject = subtask.subject

    if request.method != 'POST':
        form = SubtaskForm(instance=subtask)
    else:
        form = SubtaskForm(instance=subtask, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bord:subject', subject_id=subject.id)

    context = {'subtask': subtask, 'subject': subject, 'form': form}
    return render(request, 'bord/edit_subtask.html', context)


@login_required()
@require_http_methods(['DELETE'])
def delete_subtask(request, subtask_id):
    subtask = Subtask.objects.get(id=subtask_id)
    subject = subtask.subject

    subtask.delete()

    subtasks = Subtask.objects.filter(subject=subject).order_by('done', 'id')

    return render(request, 'bord/partials/subtask_list.html', {'subtasks': subtasks})


@login_required()
def delete_subtask_modal(request, subtask_id):
    subtask = Subtask.objects.get(id=subtask_id)
    return render(request, 'bord/partials/delete_subtask_modal.html', {'subtask': subtask})

@login_required()
def new_task(request):
    current_user = request.user
    users = User.objects.exclude(pk=current_user.pk).exclude(username='admin')
    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(data=request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.save()
            users_selected = request.POST.getlist('users')
            users = User.objects.filter(pk__in=users_selected)
            new_task.user.set(users)
            new_task.user.add(current_user)
            return redirect('bord:todo')

    context = {'form': form, 'users': users}
    return render(request, 'bord/new_task.html', context)


@login_required()
def check_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.done:
        task.done = False
    else:
        task.done = True
    task.save()
    return redirect('bord:todo')


@login_required()
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    selected_users = task.user.all()

    users = User.objects.exclude(pk=request.user.pk).exclude(username='admin')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            users_selected = request.POST.getlist('users')
            users = User.objects.filter(pk__in=users_selected)
            task.user.set(users)
            task.user.add(request.user)
            return redirect('bord:todo')
    else:
        form = TaskForm(instance=task)

    context = {'task': task, 'form': form, 'users': users, 'selected_users': selected_users}
    return render(request, 'bord/edit_task.html', context)


@login_required()
def delete_task(*args, task_id):
    task = Task.objects.get(id=task_id)

    task.delete()
    return redirect('bord:todo')


@login_required()
def contacts(request, subject_id):
    contacts = Contact.objects.filter(subject_id=subject_id).order_by('id')
    context = {'contacts': contacts}
    return render(request, 'bord/partials/contact.html', context)


@login_required()
def contact(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    context = {'contact': contact}
    return render(request, 'bord/partials/contact.html', context)


@csrf_exempt
@login_required()
def edit_contact(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    subject = contact.subject
    if request.method != 'POST':
        form = ContactForm(instance=contact)
    else:
        form = ContactForm(instance=contact, data=request.POST)
        if form.is_valid():
            form.save()
            contacts = subject.contact_set.all().order_by('id')
            return render(request, 'bord/partials/contact.html', {'contacts': contacts})

    context = {'subject': subject, 'form': form, 'contact': contact}
    return render(request, 'bord/partials/edit_contact.html', context)


@login_required()
def new_contact(request, subject_id):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            new_contact = form.save(commit=False)
            new_contact.subject = Subject.objects.get(id=subject_id)
            new_contact.save()
            contacts = Contact.objects.filter(subject_id=subject_id).order_by('id')
            return render(request, 'bord/partials/contact.html', {'contacts': contacts})
    else:
        form = ContactForm()
    return render(request, 'bord/partials/new_contact.html', {'form': form, 'subject_id': subject_id})


@login_required()
@require_http_methods(['DELETE'])
def delete_contact(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    subject = contact.subject
    contact.delete()
    contacts = Contact.objects.filter(subject=subject)
    return render(request, 'bord/partials/contact.html', {'contacts': contacts})


@login_required()
def delete_contact_modal(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    return render(request, 'bord/partials/delete_contact_modal.html', {'contact': contact})
