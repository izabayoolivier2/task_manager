from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm
from django.http import Http404
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})


# Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}!")
                return redirect('task_list')
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

# Logout View
def user_logout(request):
    logout(request)
    messages.info(request, "You have logged out successfully.")
    return redirect('login')



# Task List View
@login_required  # Ensure that only logged-in users can access this view
def task_list(request):
    tasks = Task.objects.filter(user=request.user)  # Only fetch tasks for the current user
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')


    # Get the task to mark as completed (if any)
    task_to_complete = request.GET.get('mark_completed', None)
    if task_to_complete:
        task = get_object_or_404(Task, pk=task_to_complete)
        task.status = 'completed'
        task.save()


    # Filter tasks based on search query and status filter
    tasks = Task.objects.all()

    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    if status_filter:
        tasks = tasks.filter(status=status_filter)

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'search_query': search_query, 'status_filter': status_filter})


# Task Detail View
@login_required  # Ensure the user is logged in
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

# Task Create View
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Link task to the logged-in user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

# Task Edit View
@login_required  # Ensure the user is logged in
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

# Task Delete View
@login_required  # Ensure the user is logged in
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
