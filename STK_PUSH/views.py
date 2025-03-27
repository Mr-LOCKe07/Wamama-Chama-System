from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login

import requests
from requests.auth import HTTPBasicAuth
import json
import time

from .credentials import MpesaAccessToken, LipanaMpesaPpassword
from .utilis import get_pesapal_access_token
from django.conf import settings
import time
from .forms import Meet, SignUpForm, RegisterChamaForm,ArticleForm
from .models import Meetings, RegisterChama,Article,SignUp
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect 
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import render, redirect 

def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token": validated_mpesa_access_token})


# MPESA Payment Processing
def pay(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Chama Programme",
            "TransactionDesc": "Chama Contribution"
        }

        response = requests.post(api_url, json=request_data, headers=headers)
        return HttpResponse("success")


# Payment Methods
def MPESA(request):
    return render(request, 'MPESA.html', {'navbar': 'MPESA'})


def method(request):
    return render(request, 'Payment Methods.html')


def kcb(request):
    return render(request, 'kcb.html')


def equity(request):
    return render(request, 'equity.html')


def pesapal(request):
    return render(request, 'pesapal.html')


# Pesapal Payment Integration
def initiate_payment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')

        if not all([name, email, phone, amount]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        access_token = get_pesapal_access_token()
        if not access_token:
            return JsonResponse({"error": "Failed to get access token"}, status=400)

        url = f"{settings.PESAPAL_API_BASE_URL}/Transactions/SubmitOrderRequest"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        data = {
            "id": str(int(time.time())),
            "currency": "KES",
            "amount": amount,
            "description": "Payment for Services",
            "callback_url": settings.CALLBACK_URL,
            "notification_id": "your_notification_id",
            "billing_address": {
                "email_address": email,
                "phone_number": phone,
                "first_name": name.split(" ")[0],
                "last_name": " ".join(name.split(" ")[1:]) if len(name.split(" ")) > 1 else ""
            }
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({"error": "Payment request failed", "details": response.text}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


def check_payment_status(request, order_tracking_id):
    access_token = get_pesapal_access_token()
    if not access_token:
        return JsonResponse({"error": "Failed to get access token"}, status=400)

    url = f"{settings.PESAPAL_API_BASE_URL}/Transactions/GetTransactionStatus?orderTrackingId={order_tracking_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({"error": "Failed to check payment status", "details": response.text}, status=400)


# Other Payment Methods
def paypal(request):
    return render(request, 'paypal.html')


# General Views
def index(request):
    articles = Article.objects.all()
    return render(request, 'index.html', {'articles': articles})


def events(request):
    return render(request, 'events.html')


def calendar(request):
    return render(request, 'calendar.html')


# Admin and User Authentication
def admin_sign(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        phone_number = request.POST.get("phone_number")
        name_of_chama = request.POST.get("name_of_chama")
        password = request.POST.get("password")

        try:
            admin = RegisterChama.objects.get(
                first_name=first_name,
                phone_number=phone_number,
                name_of_chama=name_of_chama
            )
            if check_password(password, admin.password):
                request.session["admin_id"] = admin.id
                return redirect("admin_dashboard")
            else:
                messages.error(request, "NOT CHAIRLADY")
        except RegisterChama.DoesNotExist:
            messages.error(request, "NOT CHAIRLADY")

    return render(request, "admin sign.html")


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            name_of_chama = form.cleaned_data.get('name_of_chama')
            if not RegisterChama.objects.filter(name_of_chama=name_of_chama).exists():
                form.add_error('name_of_chama', "Chama does not exist. Please register the chama first.")
                return render(request, 'sign up.html', {'signup_form': form})

            form.save()
            messages.success(request, "Sign up successful!")
            return redirect("home")
        else:
            messages.error(request, "Error in form submission. Please check your inputs.")
    else:
        form = SignUpForm()

    return render(request, 'sign up.html', {'signup_form': form})


def register(request):
    if request.method == "POST":
        form = RegisterChamaForm(request.POST)
        if form.is_valid():
            chama = form.save()
            messages.success(request, "Chama registered successfully!")
            return redirect("home")
        else:
            messages.error(request, "Error in form submission. Please check your inputs.")
    else:
        form = RegisterChamaForm()

    return render(request, 'sign up.html', {'register_form': form})


# Meetings Management
def meetings(request):
    meetings = Meetings.objects.all()
    print(meetings)
    return render(request, 'meetings.html', {'meetings': meetings})


def dashboard(request):
    return render(request, 'admin_dashboard.html')


def add_meeting(request):
    if request.method == 'POST':
        form = Meet(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = Meet()
    return render(request, 'admin_dashboard.html', {'form': form})


def meeting_detail(request, meeting_id):
    meeting = get_object_or_404(Meetings, id=meeting_id)
    return render(request, 'meetings.html', {'meeting': meeting})


def admin_dashboard(request):
    if request.method == 'POST':
        form = Meet(request.POST, request.FILES)
        if form.is_valid():
            Meetings.objects.all().delete()
            form.save()
            return redirect('admin_dashboard')
    else:
        form = Meet()
    meetings = Meetings.objects.all()
    return render(request, 'admin_dashboard.html', {'form': form, 'meetings': meetings})


def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meetings, id=meeting_id)
    if request.method == 'POST':
        meeting.delete()
        return redirect('admin-dashboard')
    return render(request, 'admin_dashboard.html')


# User Login
def user_login(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        try:
            user = SignUp.objects.get(phone_number=phone_number)
            if check_password(password, user.password):
                messages.success(request, "Login successful!")
                request.session['user_id'] = user.id
                return redirect("home")
            else:
                messages.error(request, "Invalid phone number or password. Please try again.")
        except SignUp.DoesNotExist:
            messages.error(request, "User does not exist. Please sign up first.")

    return render(request, "index.html")

def user_logout(request):
    try:
        del request.session['user_id']
        messages.success(request, "Logout successful!")
    except KeyError:
        messages.error(request, "You are not logged in.")
    return redirect('/')


def admin_login(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        name_of_chama = request.POST.get('name_of_chama')

        try:
            admin = RegisterChama.objects.get(
                phone_number=phone_number,
                first_name=first_name,
                name_of_chama=name_of_chama
            )
            if check_password(password, admin.password):
                messages.success(request, "Login successful!")
                request.session['admin_id'] = admin.id
                return redirect("admin_dashboard")
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        except RegisterChama.DoesNotExist:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, "admin sign.html")

def logout(request):
    try:
        del request.session['user_id']
        messages.success(request, "Logout successful!")
    except KeyError:
        messages.error(request, "You are not logged in.")
    return redirect('admin_sign')

def admin(request):
    return render(request, 'admin sign.html')


# Articles Management
def articles(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect after saving
        else:
            print("Form Errors:", form.errors)  # Debugging line

    else:
        form = ArticleForm()

    articles = Article.objects.all()
    return render(request, 'admin_dashboard.html', {'form': form, 'articles': articles})

