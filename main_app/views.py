from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Court, Booking
from .forms import BookingForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('')

def home(request):
    courts = Court.objects.all()
    return render(request, 'home.html', {'courts': courts})
    current_year = datetime.datetime.now().year
    return render(request, 'home.html', {'current_year': current_year})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to the home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('home')  # Redirect to the home page
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def court_detail(request, court_id):
    court = get_object_or_404(Court, id=court_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.court = court
            booking.save()
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'court_detail.html', {'court': court, 'form': form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
    return redirect('my_bookings')

def user_logout(request):
    logout(request)  # Log out the user
    return redirect('home')  # Redirect to the home page after logging out