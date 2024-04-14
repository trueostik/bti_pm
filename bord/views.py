from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import Subject, Comment, Subtask, User, Task
from .forms import SubjectForm, CommentForm, SubtaskForm, TaskForm


@login_required()
def index(request):
    subjects = Subject.objects.order_by('priority', '-date_added')
    subjects_count = Subject.objects.filter(archived=False).count()
    context = {'subjects': subjects, 'subjects_count': subjects_count}
    for subject in subjects:
        subject.unfinished_subtasks_count = subject.subtask_set.filter(done=False).count()
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
def todo(request):
    user = request.user
    tasks = Task.objects.filter(user=user).order_by('done', '-date_added')
    context = {'tasks': tasks}
    return render(request, 'bord/todo.html', context)


@login_required()
def subject_view(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    comments = subject.comment_set.order_by('-date_added')
    subtasks = subject.subtask_set.order_by('done')
    contacts = subject.contact_set.all()
    context = {'subject': subject, 'comments': comments, 'subtasks': subtasks, "contacts": contacts}
    return render(request, 'bord/subject.html', context)


@login_required()
def new_subject(request):
    if request.method != 'POST':
        form = SubjectForm()
    else:
        form = SubjectForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bord:index')

    context = {'form': form}
    return render(request, 'bord/new_subject.html', context)


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

    context = {'subject': subject, 'form': form}
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
    if subject.archived:
        subject.archived = False
        subject.done = False
        subject.save()
    else:
        subject.archived = True
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
    subtasks = Subtask.objects.filter(subject=subject)

    return render(request, 'bord/partials/subtask_list.html', {'subtasks': subtasks})


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


@require_http_methods(['DELETE'])
def delete_subtask(request, subtask_id):
    subtask = Subtask.objects.get(id=subtask_id)
    subject = subtask.subject

    subtask.delete()

    subtasks = Subtask.objects.filter(subject=subject)

    return render(request, 'bord/partials/subtask_list.html', {'subtasks': subtasks})

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
            users_selected = request.POST.getlist('users')  # Отримати список обраних користувачів
            users = User.objects.filter(pk__in=users_selected)  # Отримати об'єкти користувачів за їх ID
            new_task.user.set(users)  # Додати обраних користувачів до поля user завдання
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
            if users_selected:
                users = User.objects.filter(pk__in=users_selected)
                task.user.set(users)
                task.user.add(request.user)
            else:
                task.user.clear()
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

