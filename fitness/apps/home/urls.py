from django.urls import path,re_path,include
from .views import FitnessListApiView, BookClassApiView, BookingListApiView, TimezoneSwitchView


urlpatterns = [

    re_path(r'^home/', include([
        path('list-classes/', FitnessListApiView.as_view()),
        path('booking-process/', BookClassApiView.as_view()),
        path('bookings-listing/', BookingListApiView.as_view()),
        path('switch-timezone/', TimezoneSwitchView.as_view()) 
    ])),

]

