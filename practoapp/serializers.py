from rest_framework import serializers
from .models import Doctor, CustomUser, Appointment

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'city', 'password')

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'  # You can specify specific fields if needed

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class AppointmentDetailsSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name')
    doctor_specialization = serializers.CharField(source='doctor.specialization')
    doctor_image_url = serializers.URLField(source='doctor.image_url')

    class Meta:
        model = Appointment
        fields = ('id', 'doctor_name', 'doctor_specialization', 'doctor_image_url', 'appointment_datetime')

