from django.core.exceptions import ValidationError


def file_size_validator(file, max_size_mb=10):
    max_size = max_size_mb * 1024 * 1024  # Baytlarga o‘girish
    if file.size > max_size:
        raise ValidationError(f"Fayl hajmi {max_size_mb} MB dan oshmasligi kerak.")
