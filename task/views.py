from django.shortcuts import get_object_or_404, render, redirect
from .models import Task, User
from django.contrib import messages

def home(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    current_user = User.objects.get(id=user_id)
    tasks = Task.objects.all()
    users = User.objects.all()

    return render(request, "home.html", {
        "tasks": tasks,
        "users": users,
        "current_user": current_user
    })

def create_task(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        status = request.POST.get("status")
        owner_id = request.POST.get("owner")

        owner = User.objects.filter(id=owner_id).first() if owner_id else None
        created_by = User.objects.get(id=user_id)

        task = Task(
            name=name,
            description=description,
            status=status,
            owner=owner,
            created_by=created_by,
            updated_by=created_by
        )
        task.save()
        messages.success(request, "Task criada com sucesso!")

    return redirect("home")

def update_task(request, task_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    task = get_object_or_404(Task, id=task_id)
    current_user = User.objects.get(id=user_id)

    if task.owner != current_user:
        messages.error(request, "Você só pode editar suas próprias tasks!")
        return redirect("home")

    if request.method == "POST":
        task.name = request.POST.get("name")
        task.description = request.POST.get("description")
        task.status = request.POST.get("status")

        owner_id = request.POST.get("owner")
        task.owner = User.objects.filter(id=owner_id).first() if owner_id else None

        task.updated_by = current_user
        task.save()

        messages.success(request, "Task atualizada com sucesso!")

    return redirect("home")

def delete_task(request, task_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    task = get_object_or_404(Task, id=task_id)

    current_user = User.objects.get(id=user_id)

    if task.created_by != current_user:
        messages.error(request, "Você só pode deletar suas próprias tasks!")
        return redirect("home")

    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deletada com sucesso!")
        return redirect("home")