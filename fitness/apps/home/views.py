import pytz,logging,os,sys
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
from .schemas import BookingDropdownSchema,FitnessDropdownSchema
from django.utils.timezone import activate
from fitness_core.helpers.response import ResponseInfo
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q

logger = logging.getLogger(__name__)


class BookClassView(APIView):
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Booking successful: {serializer.data}")
            return Response({"message": "Booking successful"}, status=status.HTTP_201_CREATED)
        logger.warning(f"Booking failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class TimezoneSwitchView(APIView):
    def post(self, request):
        tz = request.data.get('timezone')
        try:
            activate(pytz.timezone(tz))
            for cls in FitnessClass.objects.all():
                cls.datetime = cls.datetime.astimezone(pytz.timezone(tz))
                cls.save()
            return Response({"message": f"Timezone updated to {tz}"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        


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