from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import threading
import asyncio
from asgiref.sync import sync_to_async
from accounts.models.accounts import CustomUser
from config.settings import EMAIL_HOST_USER


async def send_bulk_emails_async(html_content, subject, recipient_list, batch_size=50):
    for i in range(0, len(recipient_list), batch_size):
        batch = recipient_list[i : i + batch_size]
        tasks = [send_email_async(html_content, subject, user) for user in batch]
        await asyncio.gather(*tasks)


async def send_email_async(html_content, subject, user):
    to_email = [user.email]

    # Emailni yaratish
    msg = EmailMultiAlternatives(
        subject,
        "",
        EMAIL_HOST_USER,
        to_email,  # Mavzu  # Oddiy matn  # Kimdan  # Qayerga
    )

    # HTML formatidagi emailni qo'shish
    msg.attach_alternative(html_content, "text/html")

    # Emailni yuborish
    try:
        await sync_to_async(msg.send)()
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")


async def send_emails_in_background_async(
    html_content, subject="Xush kelibsiz!", recipient_list=None
):
    if recipient_list is None:
        # Foydalanuvchilarni olish
        recipient_list = await sync_to_async(list)(
            CustomUser.objects.exclude(email=EMAIL_HOST_USER)
        )

    # Asinxron email yuborishni boshlash
    await send_bulk_emails_async(html_content, subject, recipient_list)


def send_emails_in_thread(
    context,
    subject="Xush kelibsiz!",
    html_path="",
    recipient_list=None,
):
    html_content = render_to_string(html_path, context)

    # Thread ichida asyncio.loop ni ishga tushirish
    thread = threading.Thread(
        target=lambda: asyncio.run(
            send_emails_in_background_async(html_content, subject, recipient_list)
        )
    )
    thread.start()
    return thread
