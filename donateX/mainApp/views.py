from rest_framework import viewsets, permissions, status
from .models import Donation,PaymentHistory,CustomUser
from .serializers import DonationSerializer,UserSerializer,PaymentHistorySerializer
from django.shortcuts import render
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.views import View


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    
class PaymentHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter payment history records for the authenticated user
        user = self.request.user
        return PaymentHistory.objects.filter(user=user)

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
    
class DashboardView(View):
    def get(self, request):
        # Get the payment history for the logged-in user
        payments = PaymentHistory.objects.filter(user=request.user)
        context = {
            'user': request.user,
            'payments': payments,
        }
        return render(request, 'dashboard.html', context)

# UI templates views 

@login_required
def donation_form(request): 
    user = request.user
    
    if request.method == 'POST':
        # Create a new donation entry
        transaction_id = request.POST.get('transaction_id')
        amount = request.POST.get('amount')

        donation = Donation.objects.create(
            donor_name=user.username,
            phone_number=user.phone,
            amount=amount,
            # You can add other fields as needed
        )
        PaymentHistory.objects.create(
            donation=donation,  # Assuming the donation ID is returned in the response
            transaction_id=transaction_id,  # Replace with actual transaction ID
            status="Successful",  # You can update this based on the payment status
            user=user,
        )

        return redirect('thankyou')

    # For GET requests, render the donate.html template
    return render(request, 'donate.html', {'user': user})

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