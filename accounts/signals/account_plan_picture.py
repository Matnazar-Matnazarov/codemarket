from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from ..models.accounts import CustomUser, Role
from django.core.exceptions import ValidationError
import requests
from django.core.files.base import ContentFile
from allauth.account.signals import user_signed_up, user_logged_in
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mass_mail
import time
import threading
import asyncio
from asgiref.sync import sync_to_async


# Foydalanuvchi rejasini yangilash, rekursiyani oldini olish uchun save chaqirishni cheklash
@receiver(post_save, sender=CustomUser)
def update_user_plan(sender, instance, created=False, **kwargs):
    """
    Foydalanuvchi rejasini BASIC dan PREMIUM ga avtomatik ravishda
    yangilash, agar ular 100 yoki undan ko'p codecoins to'plagan bo'lsa.
    """
    # Agar foydalanuvchi 100 yoki undan ko'p codecoins yig'gan bo'lsa va roli BASIC bo'lsa
    if instance.codecoins >= 100 and instance.role == Role.BASIC:
        instance.role = Role.PREMIUM
        instance.save(
            update_fields=["role"]
        )  # Faqat role o'zgargan bo'lsa, save chaqiriladi

@receiver(post_save, sender=CustomUser)
def sign_up_gift(sender, instance, created=False, **kwargs):
    if created:
        instance.codecoins = 50
        instance.save(update_fields=['codecoins'])

# Foydalanuvchi profil rasmini saqlashdan oldin uning hajmini tekshirish
@receiver(pre_save, sender=CustomUser)
def validate_user_picture(sender, instance, **kwargs):
    """
    Foydalanuvchi profil rasmiga oid signal, tasvir faylining 10MB dan katta bo'lmasligini tekshiradi.
    """
    if instance.picture:
        max_file_size = 10 * 1024 * 1024  # 10MB ni baytlarda
        if instance.picture.size > max_file_size:
            raise ValidationError("Profil rasmining hajmi 10MB dan oshmasligi kerak")


@receiver(post_save, sender=CustomUser)
def update_codecoins(sender, instance, created=False, **kwargs):
    if instance.role == Role.SUPER_ADMIN:
        if instance.codecoins < 1:
            instance.codecoins = 1000
            instance.save(update_fields=["codecoins"])
    elif instance.role == Role.ADMIN:
        if instance.codecoins < 100:
            instance.codecoins = 100
            instance.save(update_fields=["codecoins"])


@receiver(user_signed_up)
def save_user_data(request, user, **kwargs):
    # Google va GitHub uchun provayderlar
    socialaccount_google = user.socialaccount_set.filter(provider="google").first()
    socialaccount_github = user.socialaccount_set.filter(provider="github").first()
    # Emailni saqlash yoki yangilash
    email = None
    if socialaccount_google:
        email = socialaccount_google.extra_data.get("email")
    elif socialaccount_github:
        email = socialaccount_github.extra_data.get("email")

    if email:
        existing_user = CustomUser.objects.filter(email=email).first()
        if existing_user is None:
            user.delete()  # Yangi foydalanuvchini o'chirish
            user = existing_user


    # Profil rasmni saqlash yoki yangilash
    picture_url = None
    if socialaccount_google:
        picture_url = socialaccount_google.extra_data.get("picture")
    elif socialaccount_github:
        picture_url = socialaccount_github.extra_data.get("avatar_url")

    if picture_url and not user.picture:  # Faqat rasm mavjud bo'lmasa saqlanadi
        try:
            response = requests.get(picture_url)
            response.raise_for_status()

            # Foydalanuvchi rasmni saqlash
            user.picture.save(
                f"{user.username}_profile.jpg",
                ContentFile(response.content),
                save=False,  # Oxirida bir marta user.save() qilinadi
            )
        except Exception as e:
            pass  # Agar rasm yuklashda muammo bo‘lsa, xatolikni e’tiborsiz qoldiramiz

    # Oxirgi o‘zgarishlarni saqlash
    user.save()


# @receiver(user_logged_in)
# def send_welcome_email(sender, request, user, **kwargs):
#     """
#     Foydalanuvchi tizimga kirganda, unga xush kelibsiz xabarini yuboradi.
#     """
#     one_user_time_start = time.time()
#     if not user.email:
#         subject = "Xush kelibsiz!"
#         from_email = "codemarketcode@gmail.com"
#         to_email = [user.email]

#         # HTML shablonini yuklash
#         html_content = render_to_string("email/login_in.html", {"user": user})

#         # Emailni yaratish
#         msg = EmailMultiAlternatives(
#             subject,  # Mavzu
#             "",  # Oddiy matn
#             from_email,  # Kimdan
#             to_email,  # Qayerga
#         )

#         # HTML formatidagi emailni qo'shish
#         msg.attach_alternative(html_content, "text/html")

#         # Emailni yuborish
#         try:
#             msg.send()
#         except Exception as e:
#             # Xatolikni loglash
#             print(f"Xatolik yuz berdi: {e}")
#     start_time = time.time()
#     send_emails_in_thread()
#     end_time = time.time()
#     print(f"Time: {end_time - start_time}")
# send_emails_in_background()
# one_user_time_end = time.time()
# print(f"User: {user.username}, Time: {one_user_time_end - one_user_time_start}")
# all_users_time_start = time.time()
# users = CustomUser.objects.exclude(id=1)
# email_list = [(subject, html_content, from_email, [user.email]) for user in users if user.email]
# send_mass_mail(email_list, fail_silently=False)


# def send_bulk_emails(subject,from_email, recipient_list, batch_size=50):
#     for i in range(0, len(recipient_list), batch_size):
#         batch = recipient_list[i:i + batch_size]
#         for user in batch:
#             to_email = [user.email]

#             # HTML shablonini yuklash
#             html_content = render_to_string('email/login_in.html', {'user': user})

#             # Emailni yaratish
#             msg = EmailMultiAlternatives(
#                 subject,  # Mavzu
#                 '',  # Oddiy matn
#                 from_email,  # Kimdan
#                 to_email  # Qayerga
#             )

#             # HTML formatidagi emailni qo'shish
#             msg.attach_alternative(html_content, 'text/html')

#             # Emailni yuborish
#             try:
#                 msg.send()
#             except Exception as e:
#                 # Xatolikni loglash
#                 print(f"Xatolik yuz berdi: {e}")

# def send_emails_in_background(subject: str='Xush kelibsiz!', from_email: str='codemarketcode@gmail.com'):
#     recipient_list = CustomUser.objects.exclude(pk=1)
#     print(recipient_list)
#     start_time = time.time()
#     threading.Thread(
#         target=send_bulk_emails,
#         args=(subject, from_email, recipient_list),
#     ).start()
#     end_time = time.time()
#     print(f"Time: {end_time - start_time}")


async def send_bulk_emails_async(
    html_content, subject, from_email, recipient_list, batch_size=50
):
    for i in range(0, len(recipient_list), batch_size):
        batch = recipient_list[i : i + batch_size]
        tasks = [
            send_email_async(html_content, subject, from_email, user) for user in batch
        ]
        await asyncio.gather(*tasks)


async def send_email_async(html_content, subject, from_email, user):
    to_email = [user.email]

    # Emailni yaratish
    msg = EmailMultiAlternatives(
        subject, "", from_email, to_email  # Mavzu  # Oddiy matn  # Kimdan  # Qayerga
    )

    # HTML formatidagi emailni qo'shish
    msg.attach_alternative(html_content, "text/html")

    # Emailni yuborish
    try:
        await sync_to_async(msg.send)()
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")


async def send_emails_in_background_async(
    html_content, subject="Xush kelibsiz!", from_email="codemarketcode@gmail.com"
):
    # Foydalanuvchilarni olish
    recipient_list = await sync_to_async(list)(CustomUser.objects.exclude(pk=1))

    # Asinxron email yuborishni boshlash
    await send_bulk_emails_async(html_content, subject, from_email, recipient_list)


def send_emails_in_thread(
    subject="Xush kelibsiz!", from_email="codemarketcode@gmail.com", html_content=""
):
    if len(html_content) < 1:
        html_content = render_to_string(
            "email/login_in.html", {"user": CustomUser.objects.first()}
        )
    # Thread ichida asyncio.loop ni ishga tushirish
    thread = threading.Thread(
        target=lambda: asyncio.run(
            send_emails_in_background_async(html_content, subject, from_email)
        )
    )
    thread.start()
    return thread


"""
0.0023322105407714844
17.33945655822754
0.0004973411560058594
"""
