from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from .forms import RegisterForm, TodoForm
from .models import Todo

# ===============================
# MAIN TODO LIST VIEW
# ===============================
@login_required
def index(request):
    filter_type = request.GET.get("filter", "all")
    priority_filter = request.GET.get("priority", None)  # 👈 New priority GET param

    # Start with all tasks for the user
    todos = Todo.objects.filter(user=request.user)

    # Filter by type
    if filter_type == "today":
        todos = todos.filter(due_date__date=now().date(), is_completed=False)
    elif filter_type == "completed":
        todos = todos.filter(is_completed=True)
    else:
        todos = todos.filter(is_completed=False)

    # Filter by priority
    if priority_filter in ["low", "medium", "high"]:
        todos = todos.filter(priority=priority_filter)

    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, "Task added successfully! 🎉")
            return redirect("index")
    else:
        form = TodoForm()

    return render(request, "todo/index.html", {
        "list": todos,
        "forms": form,
        "filter": filter_type,
        "priority_filter": priority_filter,  # 👈 Pass to template to highlight dropdown
        "now": now(),
        "overdue_messages": [
            "💪 Feeling lazy? One small step and you're unstoppable!",
            "⏳ Hey bestie, future you will thank you for finishing this now!",
            "🌸 Procrastination check! Take a breath and power through 💥",
            "🫶 You got this! Let’s turn “later” into “done”",
        ],
    })


# ===============================
# TOGGLE COMPLETION
# ===============================
@login_required
def toggle_complete(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect('index')


@login_required
def edit_task(request, id):
    # Get the task that belongs to the logged-in user
    task = get_object_or_404(Todo, id=id, user=request.user)

    if request.method == "POST":
        form = TodoForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully ✨")
            return redirect('index')
    else:
        # Pre-fill form with existing task data
        form = TodoForm(instance=task)

    return render(request, "todo/edit_task.html", {
        "form": form,
        "task": task
    })


# ===============================
# REGISTER VIEW
# ===============================
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully 🎉")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, "todo/register.html", {'form': form})

# ===============================
# LOGIN VIEW
# ===============================
def Login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # fixed redirect
        else:
            messages.error(request, "Invalid username or password 😥")

    return render(request, "todo/login.html")

# ===============================
# LOGOUT VIEW
# ===============================
@login_required
def Logout_view(request):
    logout(request)
    return redirect('login')

# ===============================
# REMOVE TODO
# ===============================
@login_required
def remove(request, item_id):
    item = get_object_or_404(Todo, id=item_id, user=request.user)
    item.delete()
    messages.info(request, "Item removed! 🗑️")
    return redirect('index')

