from rest_framework import viewsets, permissions, status
from .models import Donation,PaymentHistory
from .serializers import DonationSerializer,UserSerializer,PaymentHistorySerializer
from django.shortcuts import render
from .models import CustomUser
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    
class PaymentHistoryViewSet(viewsets.ModelViewSet):
    queryset = PaymentHistory.objects.all()
    serializer_class = PaymentHistorySerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'})

# UI templates views 

@login_required
def donation_form(request):
    if request.method == 'POST':
        # Create a new donation entry
        transaction_id = request.POST.get('transaction_id')
        donor_name = request.POST.get('donor_name')
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')

        # if response.status_code == 201:  # Check if donation creation was successful
        #     donation = Donation.objects.get(pk=response.data['id'])
            # Create a corresponding payment history entry
            
        donation = Donation.objects.create(
            donor_name=donor_name,
            phone_number=phone_number,
            amount=amount,
            # You can add other fields as needed
        )
        PaymentHistory.objects.create(
            # user=request.user,
            donation=donation,  # Assuming the donation ID is returned in the response
            transaction_id=transaction_id,  # Replace with actual transaction ID
            status="Successful",  # You can update this based on the payment status
            user=request.user,
        )

        return redirect('thankyou')

    # For GET requests, render the donate.html template
    return render(request, 'donate.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create a user object but don't save it yet
            user.set_password(form.cleaned_data['password1'])  # Set the password
            user.save()  # Save the user object with the dynamically added fields
            login(request, user)
            
             # Generate and save an authentication token for the user
            token, created = Token.objects.get_or_create(user=user)
            
            return redirect('login')  # Redirect to the donation page after successful registration
    else:
        form = RegistrationForm()
    
    return render(request, 'registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('donate')  # Redirect to the donation page after successful login
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def thankyou(request):
    return render(request,'thankyou.html')