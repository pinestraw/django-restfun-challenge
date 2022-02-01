from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, AuthView, Logout

router = DefaultRouter(trailing_slash=False)
router.register('users', UserViewSet, basename='users')
urlpatterns = router.urls

urlpatterns += [
    path('login', AuthView.as_view(), name='login'),
    path('logout', Logout.as_view()),
]
