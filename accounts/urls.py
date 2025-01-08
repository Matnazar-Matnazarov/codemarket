from django.urls import path
from .views.login import LoginView, EditProfileView, LogoutView, EditPasswordView, your_cancelled_view
from .views.profile import ProfileView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", your_cancelled_view, name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("edit_profile/", EditProfileView.as_view(), name="edit_profile"),
    path("edit_password/", EditPasswordView.as_view(), name="edit_password"),
    path('3rdparty/login/cancelled/', your_cancelled_view, name='socialaccount_cancelled'),
]
