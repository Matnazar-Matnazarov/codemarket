from django.dispatch import receiver
from django.db.models.signals import post_save
import time
from ..models.model_project import Project
from accounts.models.accounts import CustomUser, Role
from .custom_send_emails import send_emails_in_thread


@receiver(post_save, sender=Project)
def new_project_users_send_mail(sender, instance, request, **kwargs):
    if instance.is_check_admin:
        html_path = ""
        context = {"user": request.user.username, "project": instance}
        subject = "Yangi project yuklandi "
        start_time = time.time()
        send_emails_in_thread(html_path=html_path, context=context, subject=subject)
        end_time = time.time()
        print(f"Time: {end_time - start_time}")
    else:
        html_path = ""
        context = {"user": request.user.username, "project": instance}
        subject = "Yangi project yuklandi "
        start_time = time.time()
        send_emails_in_thread(
            html_path=html_path,
            context=context,
            subject=subject,
            recipient_list=CustomUser.objects.filter(role=Role.SUPER_ADMIN),
        )
        end_time = time.time()
        print(f"Time: {end_time - start_time}")


"""
0.0023322105407714844
17.33945655822754
0.0004973411560058594
"""
