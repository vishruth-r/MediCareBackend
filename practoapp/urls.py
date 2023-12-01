
from .views import DoctorRegistration, DoctorList, GetDoctorDetails, UserAppointments, UserListView, CancelAppointmentView, DoctorRecommendationView
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import SignupView, LoginView
from .views import BookAppointmentView, RescheduleAppointmentView, MyAppointmentsView

urlpatterns = [
    path('get-doctors/', DoctorList.as_view(), name='get-doctors'),
    path('register-doctor/', DoctorRegistration.as_view(), name='register-doctor'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('book-appointment/', BookAppointmentView.as_view(), name='book-appointment'),
    path('reschedule-appointment/<int:pk>/', RescheduleAppointmentView.as_view(), name='reschedule-appointment'),
    path('my-appointments/', MyAppointmentsView.as_view(), name='my-appointments'),
    path('get-doctors/<int:id>/', GetDoctorDetails.as_view(), name='get_doctor_details'),
    path('user-appointments/<int:user_id>/', UserAppointments.as_view(), name='user-appointments'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('appointments/<int:pk>/cancel/', CancelAppointmentView.as_view(), name='cancel-appointment'),
    path('search/', DoctorRecommendationView.as_view(), name='search-view'),

]
