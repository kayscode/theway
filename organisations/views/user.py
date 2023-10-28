from django.shortcuts import render, redirect, reverse
from organisations.forms import DeleteUserForm, UpdateUserForm, AdminCreateUserForm, AdminUpdateUserForm
from organisations.repositories.user import UserRepository

from organisations.models import User

from django.contrib.auth.decorators import login_required
from django.shortcuts import resolve_url

user_repository = UserRepository()


# @login_required(login_url=resolve_url("login"))
def user_list(request):
    if request.method == "GET":

        grouped_users = {}

        for user in UserRepository.find_all():
            if user.organisation is not None:
                if user.organisation.name in grouped_users.keys():
                    grouped_users[user.organisation.name].append(user)
                else:
                    grouped_users[user.organisation.name] = [user]
            else:
                print(user)

        # print(UserRepository.find_all())
        # print(grouped_users)
        context = {
            "users": grouped_users
        }

        return render(request, "organisations/users/list_users.html", context)


# @login_required(login_url=resolve_url("login"))
def show_user(request, user_id):
    if request.method == "GET":
        user = user_repository.find_one(user_id)

        context = {
            "user": user
        }

        return render(request, "organisations/users/user_detail.html", context)


# @login_required(login_url=resolve_url("login"))
def update_user(request, user_id):
    if request.user is not None and request.user.is_authenticated:
        if request.method == "GET":
            try:
                user = UserRepository.find_one(user_id)

                if request.user.is_super_admin is True:
                    user_form = AdminUpdateUserForm(user.to_json)
                else:
                    user_form = UpdateUserForm(user.to_json)

                context = {
                    "form": user_form,
                    "user_id": user.id
                }
                return render(request, "organisations/users/edit_user.html", context)
            except User.DoesNotExist:

                return render(request, "errors/404.html")
        if request.method == "POST":
            is_admin = False

            if request.user.is_super_admin is True:
                user_form = AdminUpdateUserForm(request.POST)
                is_admin = True
            else:
                user_form = UpdateUserForm(request.POST)

            if user_form.is_valid():

                try:
                    if is_admin:
                        UserRepository.update_as_admin(
                            user_form.cleaned_data.get("id"),
                            user_form.cleaned_data
                        )
                    else:
                        UserRepository.update_as_manager(
                            user_form.cleaned_data.get("id"),
                            user_form.cleaned_data
                        )

                except User.DoesNotExist:
                    return render(request, "errors/404.html")

                return redirect(reverse("user_list"))

                # return render(request, "")

            context = {
                "form": user_form
            }

            return render(request, "organisations/users/edit_user.html", context)
    else:
        return redirect(reverse("auth_login"))


# @login_required(login_url=resolve_url("login"))
# def create_user(request):
#     if request.user is not None and request.user.is_authenticated:
#         if request.user.is_super_admin is True:
#             user_form = AdminCreateUserForm()
#             context = {
#                 "form": user_form
#             }
#             return render(request, "organisations/users/create_user.html", context)
#     else:
#         return redirect(reverse("auth_login"))


# @login_required(login_url=resolve_url("login"))
def store_user(request):
    if request.user is not None and request.user.is_authenticated:
        if request.user.is_super_admin is True:
            if request.method == "GET":
                user_form = AdminCreateUserForm()
                context = {
                    "form": user_form
                }
                return render(request, "organisations/users/create_user.html", context)
            if request.method == "POST":

                user_form = AdminCreateUserForm(request.POST, request.FILES)

                print(user_form.is_valid())
                print(user_form.cleaned_data)

                if user_form.is_valid():
                    user = UserRepository.create(user_form.cleaned_data)

                    return redirect(reverse("show_user", kwargs={"user_id": user.id}))
                context = {
                    "form": user_form
                }
                print("formulaire invalid")
                return render(request, "organisations/users/create_user.html", context)
    else:
        return redirect(reverse("auth_login"))


# @login_required(login_url=resolve_url("login"))

def delete_user(request, user_id):
    if request.user.is_authenticated and request.user.is_super_admin:
        if request.method == "GET":
            UserRepository.delete(user_id)
            return redirect(reverse("user_list"))
    else:
        return redirect(reverse("user_list"))


def deactivate_user(request, user_id):
    if request.user.is_authenticated and request.user.is_super_admin:
        if request.method == "GET":
            user = UserRepository.find_one(user_id)
            user.is_active = False
            user.save()
            return redirect(reverse("user_list"))
    else:
        return redirect(reverse("user_list"))


def reactivate_user(request, user_id):
    if request.user.is_authenticated and request.user.is_super_admin:
        if request.method == "GET":
            user = UserRepository.find_one(user_id)
            user.is_active = True
            user.save()
            return redirect(reverse("user_list"))
    else:
        return redirect(reverse("user_list"))
