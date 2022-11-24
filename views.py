from datetime import timedelta
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Appointment, Category, Service
from .forms import AppointmentForm
from django.urls import reverse
from ParlourApp.forms import UserRegistrationForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email,
                                                password=password)
                user.save();
                messages.info(request, "Account Created Successfully")
                return redirect('login')
                print("user Created")

        else:
            print("password not match")
            messages.info(request, "Password incorrect")
            return redirect('register')
        return redirect('login')
    return render(request, "register.html")


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("user")
        else:
            messages.error(request, "Invalid credentials!!!")
            return redirect('login')
    return render(request, "login.html")


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')


def user(request):
    if request.user.is_authenticated:
        apptmnt_info = Appointment.objects.filter(user=request.user)
        return render(request, "user.html",{
            'info': apptmnt_info,
        })
    return redirect('login')


########Sevices##########

def demo(request):
    obj = Category.objects.all()
    return render(request, "index.html", {'category': obj})


def bridal(request):
    bridal = Service.objects.filter(category_id=1)
    return render(request, "services/bridal.html", {'list': bridal})


def hair(request):
    hair = Service.objects.filter(category_id=2)
    return render(request, "services/hair.html", {'list2': hair})


def makeover(request):
    mkup = Service.objects.filter(category_id=6)
    return render(request, "services/makeover.html", {'list5': mkup})


def wax(request):
    wax = Service.objects.filter(category_id=5)
    return render(request, "services/wax.html", {'list6': wax})


def skin(request):
    skin = Service.objects.filter(category_id=3)
    return render(request, "services/skin.html", {'list3': skin})


def nails(request):
    nails = Service.objects.filter(category_id=4)
    return render(request, "services/nails.html", {'list4': nails})


########Appointment##########

def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            if date < timezone.now().date():
                messages.info(request, "Date cannot be in the past")
                return redirect('appointment')
            startdate = date
            enddate = startdate + timedelta(days=0)
            todays_service = Appointment.objects.filter(date__range=[startdate, enddate]).values_list('service').filter(service=service).count()
            todays_slot = Appointment.objects.filter(date__range=[startdate, enddate]).values_list('time').filter(service=service).filter(time=time).count()
            count_per_day = Appointment.objects.filter(date__range=[startdate, enddate]).count()
            if count_per_day > 4:
                messages.info(request, "Appointment is full for this date!! Try another date!")
                return redirect('appointment')
            elif todays_service > 2:
                messages.info(request, "Appointment is full for this service!! Try another day!")
                return redirect('appointment')
            elif todays_slot > 1:
                messages.info(request, "Appointment is full for this time slot!! Try another time slot!")
                return redirect('appointment')
                # print(result)
                print(count_per_day)
                print(todays_aptmnt)
                print(todays_slot)
            apptmnt = Appointment(user=request.user, service=service, date=date, time=time)
            apptmnt.save()
            messages.info(request, "New Appointment Added Successfully!!!")
            apptmnt_info = Appointment.objects.filter(user=request.user)
            return render(request, "appointment_info.html", {
                'info': apptmnt_info,
                'service': service,
                'date': date,
                'time': time,
            })

    else:
        form = AppointmentForm
    return render(request, 'appointment.html', {'form': form})


def appointment_info(request):
    if request.user.is_authenticated:
        apptmnt_info = Appointment.objects.filter(user=request.user)
        return render(request, "appointment_info.html", {
            'info': apptmnt_info,
        })

    return redirect('appointment')


# CRUD OPERATIONS
def Delete(request, id):
    apptmnt_info = Appointment.objects.filter(id=id)
    apptmnt_info.delete()
    messages.info(request, "Appointment Deleted!!!")
    return redirect("appointment_info")


def Update(request, id):
    if request.method == 'POST':
        result = Appointment.objects.get(id=id)
        form = AppointmentForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
    else:
        result = Appointment.objects.get(id=id)
        form = AppointmentForm(instance=result)
        messages.info(request, "Updated!!!")
    return render(request, 'update_appointment.html', {'form': form})


# Send Email
# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.template.loader import render_to_string
#
# def success(request,uid):
#     template = render_to_string('email_message.html')
#     email=EmailMessage(
#         'subject',
#         'body',
#         settings.EMAIL_HOST_USER,
#         ['beautyparlour801@gmail.com'],
#     )
#     email.fail_silently=False
#     email.send()
#     result = Appointment.objects.get(id=uid)
#     context = {'result':result}
#     return render(request,'success.html',context)
#


# def register(request):
#     form = UserRegistrationForm()
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user.is_active = False
#             print("Successfully Registered")
#             messages.info(request, 'Registered Successfully !!Now you can login!')
#             return redirect('register')
#             return redirect(reverse('register'))
#     return render(request, 'register.html', {'form': form})

# def activateEmail(request, user, to_email):
#     messages.success(request,'Dear <b> {user}</b>,please go to your email <b> {to_email}</b> inbox and click on received activation link to confirm and complete the registration.<b>Note:</b> Check ypur spam folder.')

def new(request):
    return render(request, "new.html")
