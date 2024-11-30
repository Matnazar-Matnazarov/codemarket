from ..models.accounts import CustomUser
from faker import Faker


# add a face to the user
def add_user_face():
    users = []
    fake = Faker()
    for i in range(10):
        users.append(CustomUser(is_active=True, email=fake.email()))
    faceusers = CustomUser.objects.bulk_create(users)
    return faceusers
