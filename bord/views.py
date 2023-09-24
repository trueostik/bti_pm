from django.shortcuts import render, redirect

from .models import Subject, Comment, Subtask
from .forms import SubjectForm, CommentForm, SubtaskForm


def index(request):
    subjects = Subject.objects.order_by('priority')
    context = {'subjects': subjects}
    for subject in subjects:
        subject.unfinished_subtasks_count = subject.subtask_set.filter(done=False).count()
    return render(request, 'bord/index.html', context)


def archive(request):
    subjects = Subject.objects.order_by('date_added')
    context = {'subjects': subjects}
    return render(request, 'bord/archive.html', context)


def subject_view(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    comments = subject.comment_set.order_by('-date_added')
    subtasks = subject.subtask_set.order_by('done')
    context = {'subject': subject, 'comments': comments, 'subtasks': subtasks}
    return render(request, 'bord/subject.html', context)


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


def delete_subject(*args, subject_id):
    subject = Subject.objects.get(id=subject_id)

    subject.delete()
    return redirect('bord:index')


def new_comment(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.subject = subject
            new_comment.save()
            return redirect('bord:subject', subject_id=subject_id)

    context = {'subject': subject, 'form': form}
    return render(request, 'bord/new_comment.html', context)


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


def delete_comment(*args, comment_id):
    comment = Comment.objects.get(id=comment_id)
    subject = comment.subject

    comment.delete()
    return redirect('bord:subject', subject_id=subject.id)


def change_status(request, subject_id, field):
    subject = Subject.objects.get(id=subject_id)
    field_value = getattr(subject, field)
    setattr(subject, field, not field_value)
    subject.save()
    return redirect('bord:index')


def change_priority(request, subject_id, priority):
    subject = Subject.objects.get(id=subject_id)
    subject.priority = priority
    subject.save()
    return redirect('bord:index')


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


def check_subtask(request, subtask_id):
    subtask = Subtask.objects.get(id=subtask_id)
    subject = subtask.subject
    if subtask.done:
        subtask.done = False
    else:
        subtask.done = True
    subtask.save()
    return redirect('bord:subject', subject_id=subject.id)


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


def delete_subtask(*args, subtask_id):
    subtask = Subtask.objects.get(id=subtask_id)
    subject = subtask.subject

    subtask.delete()
    return redirect('bord:subject', subject_id=subject.id)
