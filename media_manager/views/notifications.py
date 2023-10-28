from django.shortcuts import render, redirect, reverse

from media_manager.repositories import NotificationsRepository, SourceMediaNotificationsRepository
from media_manager.forms import RejectAndApprovalNotificationForm


def notifications_main(request):
    return render(request, "")


def list_notifications(request, notification_type):
    if request.user is not None and request.user.is_authenticated:
        if request.method == "GET":

            notifications_and_form = []

            if notification_type == "source":
                notifications = SourceMediaNotificationsRepository.find_all()
                for notification in notifications:
                    notifications_and_form.append(
                        {
                            "notification": notification,
                            "form": RejectAndApprovalNotificationForm({
                                "id": notification.id,
                                "media_id": notification.source.id})
                        }
                    )

            elif notification_type == "media":
                notifications = NotificationsRepository.find_all()
                for notification in notifications:
                    notifications_and_form.append(
                        {
                            "notification": notification,
                            "form": RejectAndApprovalNotificationForm({
                                "id": notification.id,
                                "media_id": notification.media.id})
                        }
                    )
            context = {
                "notifications": notifications_and_form,
                "notification_type": notification_type
            }

            return render(request, "media_manager/notifications/notifications_list.html", context)
    else:
        return redirect(reverse("auth_login"))


def show_notification(request, notification_type, notification_id):
    if request.user is not None and request.user.is_authenticated:
        context = None
        if notification_type == "source":
            notification = SourceMediaNotificationsRepository.find_one(notification_id)
            context = {
                "notification_type": notification_type,
                "notification": notification,
                "source": notification.source,
                "media": None,
                "form": RejectAndApprovalNotificationForm({
                    "id": notification.id,
                    "media_id": notification.source.id
                })
            }
        elif notification_type == "media":
            notification = NotificationsRepository.find_one(notification_id)

            context = {
                "notification_type": notification_type,
                "notification": notification,
                "source": None,
                "media": notification.media,
                "form": RejectAndApprovalNotificationForm({
                    "id": notification.id,
                    "media_id": notification.media.id
                })
            }

        return render(request, "media_manager/notifications/notifications_details.html", context)
    else:
        return redirect(reverse("auth_login"))


def reject_notification(request, notification_type, notification_id):
    if request.user is not None and request.user.is_authenticated:
        if request.method == "POST":

            notification_form = RejectAndApprovalNotificationForm(request.POST)
            context = None

            if notification_form.is_valid():

                redirect_url = ""
                if notification_type == "source":
                    SourceMediaNotificationsRepository.reject_notification(
                        notification_id=notification_form.cleaned_data.get("id"),
                    )
                    redirect_url = reverse("list_notification", kwargs={"notification_type": "source"})

                elif notification_type == "media":
                    NotificationsRepository.reject_notification(
                        notification_id=notification_form.cleaned_data.get("id")
                    )
                    redirect_url = reverse("list_notification", kwargs={"notification_type": "media"})

                return redirect(redirect_url)

            return redirect(reverse(
                "show_notification",
                kwargs={"notification_type": notification_type, "notification_id": notification_id}
            ))
        else:
            return redirect(reverse("list_notification"))
    else:
        return redirect(reverse("auth_login"))


def accept_notification(request, notification_type, notification_id):
    if request.user is not None and request.user.is_authenticated:
        if request.method == "POST":

            notification_form = RejectAndApprovalNotificationForm(request.POST)
            context = None

            if notification_form.is_valid():
                print(notification_form.cleaned_data.get("id"))
                redirect_url = ""
                if notification_type == "source":
                    SourceMediaNotificationsRepository.approve_notification(
                        notification_id=notification_form.cleaned_data.get("id")
                    )
                    redirect_url = reverse("list_notification", kwargs={"notification_type": "source"})

                elif notification_type == "media":
                    NotificationsRepository.approve_notification(
                        notification_id=notification_form.cleaned_data.get("id")
                    )
                    redirect_url = reverse("list_notification", kwargs={"notification_type": "media"})

                return redirect(redirect_url)

            return redirect(reverse(
                "show_notification",
                kwargs={"notification_type": notification_type, "notification_id": notification_id}
            ))
        else:
            return redirect(reverse("list_notification"))
    else:
        return redirect(reverse("auth_login"))


def delete_notification(request, notification_type, notification_id):
    pass
