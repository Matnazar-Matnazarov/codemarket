# Dockerfile
FROM python:3.12

# Ishchi katalog
WORKDIR /codemarket

# Barcha fayllarni loyihaga nusxalash
COPY . .

# Talab qilinadigan kutubxonalarni o‘rnatish
RUN pip install --upgrade pip && pip install -r requirements.txt

# Django serverni ishga tushirish
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
