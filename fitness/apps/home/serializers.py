from rest_framework import serializers
from .models import FitnessClass, Booking
import pytz

class FitnessClassSerializer(serializers.ModelSerializer):
    id              = serializers.IntegerField(required=False, allow_null=True)
    fitness_name    = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    datetime     = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    instructor      = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    total_slots     = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    available_slots = serializers.CharField(required=False, allow_null=True, allow_blank=True)



    class Meta:
        model = FitnessClass
        fields = ['id', 'fitness_name', 'datetime', 'instructor',"total_slots", 'available_slots']


class BookingSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(write_only=True)
    client_name   = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    client_email    = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    
    class Meta:
        model = Booking
        fields = ['class_id', 'client_name', 'client_email']

    def validate(self, data):
        try:
            fitness_class = FitnessClass.objects.get(id=data['class_id'])
        except FitnessClass.DoesNotExist:
            raise serializers.ValidationError("Invalid class ID.")

        if fitness_class.available_slots <= 0:
            raise serializers.ValidationError("No available slots.")

        return data

    def create(self, validated_data):
        fitness_class = FitnessClass.objects.get(id=validated_data['class_id'])
        instance = Booking.objects.create(
            fitness_class=fitness_class,
            client_name=validated_data['client_name'],
            client_email=validated_data['client_email']
        )
        fitness_class.available_slots -= 1
        fitness_class.save()
        return instance
    
class TimezoneInputSerializer(serializers.Serializer):
    timezone = serializers.ChoiceField(
        choices=[(tz, tz) for tz in pytz.all_timezones],
        help_text="Valid timezone name (e.g., 'Asia/Kolkata', 'Pacific/Auckland')"
    )