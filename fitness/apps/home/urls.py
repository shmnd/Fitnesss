from django.urls import path,re_path,include
from .views import FitnessListApiView, BookClassView, BookingListApiView, TimezoneSwitchView


urlpatterns = [

    re_path(r'^home/', include([
        path('list-classes/', FitnessListApiView.as_view()),
        path('book/', BookClassView.as_view()),
        path('bookings/', BookingListApiView.as_view()),
        path('switch-timezone/', TimezoneSwitchView.as_view()) 
    ])),

]

