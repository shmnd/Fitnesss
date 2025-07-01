from rest_framework import serializers
from .models import FitnessClass, Booking

class FitnessClassSerializer(serializers.ModelSerializer):
    id              = serializers.IntegerField(required=False, allow_null=True)
    fitness_name    = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    description     = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    instructor      = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    total_slots     = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    available_slots = serializers.CharField(required=False, allow_null=True, allow_blank=True)



    class Meta:
        model = FitnessClass
        fields  = ['id', 'fitness_name', 'description', 'instructor','total_slots','available_slots']


class BookingSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(write_only=True)
    
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
        booking = Booking.objects.create(
            fitness_class=fitness_class,
            client_name=validated_data['client_name'],
            client_email=validated_data['client_email']
        )
        fitness_class.available_slots -= 1
        fitness_class.save()
        return booking
