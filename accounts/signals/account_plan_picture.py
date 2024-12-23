from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from ..models.accounts import CustomUser, Role
from django.core.exceptions import ValidationError
import requests
from django.core.files.base import ContentFile
from allauth.account.signals import user_signed_up


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
    socialaccount = user.socialaccount_set.filter(provider="google").first()
    if socialaccount:
        # Emailni saqlash
        email = socialaccount.extra_data.get("email")
        check_user = CustomUser.objects.filter(email=email).first()
        if email and check_user is None:
            user.email = email

        # Profil rasmni saqlash
        picture_url = socialaccount.extra_data.get("picture")
        if picture_url:
            try:
                response = requests.get(picture_url)
                response.raise_for_status()

                user.picture.save(
                    f"{user.username}_profile.jpg",
                    ContentFile(response.content),
                    save=False,  # `save=True` emas, chunki oxirida bir marta `user.save()` qilamiz
                )
            except Exception as e:
                pass

        # Oxirgi ma'lumotlarni saqlash
        user.save()
