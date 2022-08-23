from django.urls import include, path
from .views import SignUpView


urlpatterns = [
    path('register/', SignUpView.as_view(), name='register_user'),

]
