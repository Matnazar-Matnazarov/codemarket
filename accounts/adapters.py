from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Foydalanuvchi Google yoki GitHub orqali kirganda email asosida ulash.
        Agar foydalanuvchi allaqachon mavjud bo'lsa, uni ulaydi.
        """
        user = sociallogin.user
        if not user.email:
            return  # Email mavjud bo'lmasa davom ettirmaydi

        User = get_user_model()
        try:
            existing_user = User.objects.get(email=user.email)
            socialaccount = SocialAccount.objects.filter(user=existing_user, provider=sociallogin.account.provider).first()

            if socialaccount:
                # Agar socialaccount allaqachon biriktirilgan bo'lsa, hech narsa qilmaydi
                return

            # SocialAccount'ni biriktirish
            sociallogin.connect(request, existing_user)
        except User.DoesNotExist:
            pass
