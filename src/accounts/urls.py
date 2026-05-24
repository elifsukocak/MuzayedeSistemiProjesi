from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    profile_view,
    hesap_silme_kodu_gonder,
    hesap_silme_onay,
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),

    path("hesap-sil/kod-gonder/", hesap_silme_kodu_gonder, name="hesap_silme_kodu_gonder"),
    path("hesap-sil/onay/", hesap_silme_onay, name="hesap_silme_onay"),
]