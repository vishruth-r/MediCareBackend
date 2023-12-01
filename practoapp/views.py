from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from .models import CustomUser, Appointment
from .serializers import (
     AppointmentDetailsSerializer, UserSerializer,
    AppointmentSerializer
)
import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor
from .serializers import DoctorSerializer
from openai import OpenAI
from openai import OpenAI


class DoctorRecommendationView(APIView):
    def post(self, request):
        symptoms_description = request.data.get('symptoms_description', '')

        client = OpenAI(api_key="")

        doctors = Doctor.objects.all()
        doctor_specializations = [doctor.specialization.lower() for doctor in doctors]

        messages = [
            {"role": "system", "content": "You are a helpful assistant that recommends doctors based on their specialization and the symptoms of the user"},
            {"role": "user", "content": symptoms_description}
        ]

        # Make the OpenAI API request
        openai_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100,
            n=1,
            stop=None
        )

        action = openai_response.choices[0].message.content.strip().lower()

        if action == 'search_doctor':
            matched_doctors = []
            for idx, spec in enumerate(doctor_specializations):
                if spec in symptoms_description.lower():
                    matched_doctors.append(doctors[idx])

            serializer = DoctorSerializer(matched_doctors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid action', 'action_received': action}, status=status.HTTP_400_BAD_REQUEST)

class DoctorList(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorRegistration(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

from django.contrib.auth import authenticate
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email)
        print(password)

        if email and password:
            user = authenticate(request, email=email, password=password)
            print(user)

            if user:
                return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'detail': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)

class BookAppointmentView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.AllowAny]

class RescheduleAppointmentView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.AllowAny]

class MyAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user)

class GetDoctorDetails(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    lookup_field = 'id'

class UserAppointments(generics.ListAPIView):
    serializer_class = AppointmentDetailsSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')  # Assuming the URL parameter is named 'user_id'
        return Appointment.objects.filter(patient__id=user_id)

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Adjust the permissions as needed

class CancelAppointmentView(generics.DestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        appointment = self.get_object()
        appointment.delete()
        return Response({'detail': 'Appointment canceled successfully'}, status=200)
