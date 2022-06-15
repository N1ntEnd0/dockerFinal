from django.urls import re_path

from users import views

urlpatterns = [
    re_path(
        r"^o/(?P<provider>\S+)/$",
        views.CustomProviderAuth.as_view(),
        name="provider-auth",
    )
]