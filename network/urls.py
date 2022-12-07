from distutils.debug import DEBUG
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post/<str:pk>", views.create_post, name="create_post"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("following/<int:id>", views.following, name="following"),
    # api routes
    path("edit/<int:id>", views.edit, name="edit"),
    path("like/<int:id>", views.likes, name="likes"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if DEBUG == True:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
