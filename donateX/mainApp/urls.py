from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mainApp.views import DonationViewSet,CustomUserViewSet,register,user_login,user_logout,donation_form,PaymentHistoryViewSet,thankyou

router = DefaultRouter()
router.register(r'donations', DonationViewSet)
router.register(r'users', CustomUserViewSet)
router.register(r'payment-history', PaymentHistoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('donate/', donation_form, name='donate'),
    path('thankyou/', thankyou, name='thankyou'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
