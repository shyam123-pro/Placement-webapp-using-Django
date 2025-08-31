from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import StudentInfo, JobInfo, EventInfo, CompanyInfo

# Create your views here.
def index(request):
    return render(request, 'includes/index.html')

def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You are successfully registered.')
        return redirect("/")
    else:
        form = RegisterForm()
        
    return render(request, "registration/register.html", {"form":form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, "registration/login.html",{"form": form})



def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")

@login_required(login_url='/login/')
def register_student(request):
    return render(request,'TPO_app/register_student.html')

def register_student_submit(request):
    print("Hello form is submitted")
    print(request.POST['name'])
    print(request.POST['event'])
    name = request.POST['name']
    email = request.POST['email']
    phoneno = request.POST['phoneno']
    event = request.POST['event']
    Student_Info = StudentInfo(uname=name,email=email, phoneno=phoneno,event=event)
    Student_Info.save()
    messages.success(request, 'You have successfully registered.')
    return render(request,'TPO_app/register_student.html')



def companies(request):
    return render(request,'includes/company.html')

@login_required(login_url='/login/')
def register_job(request):
    return render(request,'includes/register_job.html')

def register_job_submit(request):
    print("Hello form is submitted")
    print(request.POST['name'])
    print(request.POST['college'])
    print(request.POST['company'])
    print(request.POST['profile'])
    print(request.POST['graduation'])
    print(request.POST['phoneno'])
    name = request.POST['name']
    email = request.POST['email']
    phoneno = request.POST['phoneno']
    college = request.POST['college']
    graduation = request.POST['graduation']
    company = request.POST['company']
    profile = request.POST['profile']

    Job_Info = JobInfo(uname=name, email=email, phoneno=phoneno, college=college, graduation=graduation, company=company, profile=profile)
    Job_Info.save()
    messages.success(request, 'Your Application is successfully sent.')
    return render(request,'includes/register_job.html')

def upcoming_events(request):
    return render(request,'includes/upcoming_events.html')


def upcoming_events_submit(request):
    print(request.POST['eventname'])
    eventname = request.POST['eventname']
    description = request.POST['description']
    eventdate = request.POST['eventdate']
    Event_Info = EventInfo(eventname=eventname,description=description, eventdate=eventdate)
    Event_Info.save()
    messages.success(request, 'Your Event is successfully saved.')
    return render(request,'includes/upcoming_events.html')


def add_company(request):
    return render(request,'includes/add_company.html')


def add_company_submit(request):
    print(request.POST['cname'])
    cname = request.POST['cname']
    role = request.POST['role']
    salary = request.POST['salary']
    Company_Info = CompanyInfo(cname=cname,role=role,salary=salary)
    Company_Info.save()
    messages.success(request, 'Your Company is successfully saved.')
    return render(request,'includes/add_company.html')


def Statistics(request):
    return render(request,'includes/Statistics.html')
# def home_supply_submit(request):
#     print("Hello form is submitted")
#     companyname = request.POST["companyname"]
#     medicine = request.POST["medicine"]
#     quantity = request.POST["quantity"]
#  # views.py
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import NOCRequest
from .serializers import NOCRequestSerializer
from django.shortcuts import render

# Function-based view (HTML Page)
@csrf_exempt
def noc(request):
    return render(request, 'includes/noc.html')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import NOCRequest
from .serializers import NOCRequestSerializer
import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.timezone import localtime
from django.core.serializers import serialize
from .models import NOCRequest

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["GET", "POST"])
def noc_api(request):
    if request.method == "GET":
        records = NOCRequest.objects.all().order_by('-timestamp')
        data = []
        for rec in records:
            data.append({
                "name": rec.name,
                "roll": rec.roll,
                "branch": rec.branch,
                "purpose": rec.purpose,
                "message": rec.message,
                "document": rec.document.url if rec.document else "",
                "timestamp": localtime(rec.timestamp).isoformat(),
                "status": rec.status
            })
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        name = request.POST.get("name")
        roll = request.POST.get("roll")
        branch = request.POST.get("branch")
        purpose = request.POST.get("purpose")
        message = request.POST.get("message", "")
        document = request.FILES.get("document")

        if not all([name, roll, branch, purpose, document]):
            return JsonResponse({"error": "Missing required fields."}, status=400)

        rec = NOCRequest.objects.create(
            name=name,
            roll=roll,
            branch=branch,
            purpose=purpose,
            message=message,
            document=document
        )

        return JsonResponse({
            "name": rec.name,
            "purpose": rec.purpose,
            "document": rec.document.url,
            "timestamp": localtime(rec.timestamp).isoformat(),
            "status": rec.status
        }, status=201)

    return HttpResponseNotAllowed(['GET', 'POST'])
