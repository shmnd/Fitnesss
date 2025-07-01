from rest_framework import serializers
from apps.home.models import FitnessClass,Booking
class FitnessDropdownSchema(serializers.ModelSerializer):

    class Meta:
        model = FitnessClass
        fields = ['fitness_name', 'datetime', 'instructor','total_slots','available_slots']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key in data.keys():
            try:
                if data[key] is None:
                    data[key] = ""
            except KeyError:
                pass            
        return data
    

class BookingDropdownSchema(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['fitness_class', 'client_email', 'client_name']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key in data.keys():
            try:
                if data[key] is None:
                    data[key] = ""
            except KeyError:
                pass            
        return data

