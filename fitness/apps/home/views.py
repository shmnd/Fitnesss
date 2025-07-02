import pytz,logging,os,sys
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer,TimezoneInputSerializer
from .schemas import BookingDropdownSchema,FitnessDropdownSchema
from django.utils.timezone import activate
from fitness_core.helpers.response import ResponseInfo
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from fitness_core.helpers.helper import get_object_or_none
from django.utils.timezone import is_aware

logger = logging.getLogger(__name__)

class BookClassApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(BookClassApiView, self).__init__(**kwargs)
        
    serializer_class = BookingSerializer
    
    @swagger_auto_schema(tags=["Booking"])
    def post(self, request):
        try:
            
            instance    = get_object_or_none(FitnessClass,pk=request.data.get('id', None))
            serializer  = self.serializer_class(instance, data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code']   = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]        = False
                self.response_format["errors"]        = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            
            self.response_format['status_code']   = status.HTTP_201_CREATED
            self.response_format["message"]       = "success"
            self.response_format["status"]        = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code']   = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']        = False
            self.response_format['message']       = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

class TimezoneSwitchView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(TimezoneSwitchView, self).__init__(**kwargs)
        
    serializer_class = TimezoneInputSerializer
    
    @swagger_auto_schema(tags=["Time zone"])
    def post(self, request):
            serializer = self.serializer_class(data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code']   = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]        = False
                self.response_format["errors"]        = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            tz = serializer.validated_data['timezone']
            target_tz = pytz.timezone(tz)
            try:
                # Loop through all classes
                for cls in FitnessClass.objects.all():
                    dt = cls.datetime

                    # Remove current timezone info completely
                    naive_dt = dt.replace(tzinfo=None)

                    # Re-apply the new timezone with same time
                    cls.datetime = target_tz.localize(naive_dt)
                    print(f"Updated datetime for {cls}: {cls.datetime}")
                    cls.save()

                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format["message"] = f"All class times updated to {tz}"
                return Response(self.response_format, status=status.HTTP_200_OK)
            
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                self.response_format['status_code']   = status.HTTP_500_INTERNAL_SERVER_ERROR
                self.response_format['status']        = False
                self.response_format['message']       = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
                return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            



class FitnessListApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(FitnessListApiView, self).__init__(**kwargs)
          
    serializer_class    = FitnessDropdownSchema

    search = openapi.Parameter('search_param', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="The search value", required=False)

    response_format = ResponseInfo().response

    @swagger_auto_schema(tags=["Fitness listing"], manual_parameters=[search])
    def get(self, request):
        try:
            search_value = request.GET.get('search_param', None)
            
            
            filter_set = Q()
            if search_value not in ['', None]:
                filter_set &= Q(fitness_name__icontains=search_value)

            
            queryset = FitnessClass.objects.filter(filter_set).order_by('-id')
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.serializer_class(page, many=True, context={'request': request})
                return self.get_paginated_response(serializer.data)

            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            self.response_format['status_code']   = status.HTTP_200_OK
            self.response_format["data"]          = serializer.data
            self.response_format["status"]        = True
            return Response(self.response_format, status=status.HTTP_200_OK)

        except Exception as e:
            
            self.response_format['status_code']   = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']        = False
            self.response_format['message']       = f"{e},Internal server error"
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class BookingListView(APIView):
    def get(self, request):
        email = request.GET.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        bookings = Booking.objects.filter(client_email=email)
        data = [
            {
                "class": str(booking.fitness_class),
                "name": booking.client_name,
                "email": booking.client_email,
            } for booking in bookings
        ]
        return Response(data)


class BookingListApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(BookingListApiView, self).__init__(**kwargs)
          
    serializer_class    = BookingDropdownSchema

    search = openapi.Parameter('search_param', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="The search value", required=False)

    response_format = ResponseInfo().response

    @swagger_auto_schema(tags=["Booking listing"], manual_parameters=[search])
    def get(self, request):
        try:
            search_value = request.GET.get('search_param', None)
            
            
            filter_set = Q()
            if search_value not in ['', None]:
                filter_set &= Q(client_name__icontains=search_value)

            
            queryset = Booking.objects.filter(filter_set).order_by('-id')
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.serializer_class(page, many=True, context={'request': request})
                return self.get_paginated_response(serializer.data)

            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            self.response_format['status_code']   = status.HTTP_200_OK
            self.response_format["data"]          = serializer.data
            self.response_format["status"]        = True
            return Response(self.response_format, status=status.HTTP_200_OK)

        except Exception as e:
            
            self.response_format['status_code']   = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']        = False
            self.response_format['message']       = f"{e},Internal server error"
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)