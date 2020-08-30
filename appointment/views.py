from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth import login
from .tokens import account_activation_token
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from datetime import datetime
from .models import appointment,neagtive,posative,donor


# Create your views here.
def home(request):
    #allnegative=neagtive.objects.all()
    #allposative=posative.objects.all()
    AllAppiontment = appointment.objects.all()
    #alnegative=neagtive.objects.filter()
    numOfNegative = appointment.objects.filter(result = 'Negative').count()
    numOfNegativee = appointment.objects.filter(result = 'Negativee').count()
    numOfPositive = appointment.objects.filter(result = 'Positive').count()
    numOfNegatives = numOfNegative+numOfNegativee
    # allresult = alnegative|allposative
    context = {
        'AllAppiontment': AllAppiontment,
        'numOfNegatives':numOfNegatives,
        "numOfPositive":numOfPositive,
        #'allposative':allposative,
        #'allnegative':allnegative,
        # 'allresult':allresult,
    }
    return render(request,'index.html',context)

def appiontment(request):
    if request.method == 'POST':
        name = request.POST['name']
        first_name = request.POST['hname']
        age = request.POST['age']
        blood = request.POST['blood_group']
        email = request.POST['email']
        address = request.POST['address']
        date = request.POST['date']
        time = request.POST['time']
        if appointment.objects.filter(date=datetime.today()).count()>199:
            messages.info(request,'appiontments are full')
            return redirect('appiontment')
        else:
            add = appointment(
                first_name= first_name,
                name=name,
                age=age,
                blood_group=blood,
                email=email,
                address=address,
                date=date,
                time=time,
                result='Pendding',
            )
            add.save()
            current_site = get_current_site(request)
            mail_subject = 'Appointment Confirmation'
            message = "Hi "+name+", \nPlease check below your appointment confrim and time.Your Appointment ID:" + str(add.appointid)+" and Date: "+date+" and time:"+time
            try:
                email_msg = EmailMessage(
                mail_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                )
                email_msg.send()
                messages.info(request,'Registration Confrim Check your mail ')
            except:
                messages.info(request,' Your email is not correte! Try with valid email. ')
    hospitals =  User.objects.values('first_name')
    return render(request,'appointment.htm',{'hospitals':hospitals})

def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['hname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Taken')
                return redirect('registration')
            else:
                user = User.objects.create_user(
                    username= username,
                    first_name=first_name,
                    email=email,
                    password=password1
                 )
                user.is_active=False
                user.save()
                
                
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                })
                try:
                    email_msg = EmailMessage(
                    mail_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    )
                    email_msg.send()
                    messages.info(request,' Activation Email sent info your mail ')
                except:
                    messages.info(request,' Your email is not correte! Try with valid email. ')
                    print("account create!")
        else:
            messages.error(request,"passowrd are not same!")            



            

    return render(request,'register.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Account Activation Complate!')
    else:
        return HttpResponse('Activation link is invalid!')

def singin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        if username and password:
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                messages.success(request,'you are login')
                return redirect('profile') 
            else:
                messages.error(request,' incorret Username Password!')
                return redirect('singin')   
        else:
            messages.error(request,'  Username & Password are invalid!')
            return redirect('singin')         
    return render(request,'singin.html')
def profile(request):
    #allnegative=neagtive.objects.filter(first_name=request.user.first_name)
    #allposative=posative.objects.filter(first_name=request.user.first_name)
    AllAppiontment = appointment.objects.filter(first_name=request.user.first_name)
    numOfNegative1 = appointment.objects.filter(first_name=request.user.first_name ,result = 'Negative').count()
    numOfNegative2 = appointment.objects.filter(first_name=request.user.first_name ,result = 'Negativee').count()
    numOfPositive = appointment.objects.filter(first_name=request.user.first_name ,result = 'Positive').count()
    numOfPendding= appointment.objects.filter(first_name=request.user.first_name ,result = 'Pendding').count()
    AllNegative = appointment.objects.filter(first_name=request.user.first_name ,result='Negative')
    AllNegative = appointment.objects.filter(first_name=request.user.first_name ,result='Negativee')
    numOfNegative=numOfNegative1+numOfNegative2

    context = {
        'AllAppiontment': AllAppiontment,
        'numOfNegative':numOfNegative,
        "numOfPositive":numOfPositive,
        'numOfPendding':numOfPendding,
        #'allposative':allposative,
        'AllNegative':AllNegative
    }
    return render(request,'profile.html', context)  
def edit(request,appointid):
    appoint = appointment.objects.get(appointid=appointid)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        first_name = request.POST.get('hname')
        age = request.POST.get('age')
        blood = request.POST.get('blood_group')
        email = request.POST.get('email')
        address = request.POST.get('address')
        date = request.POST.get('date')
        time = request.POST.get('time')
        result =request.POST.get('result')

        appoint.name=name
        appoint.first_name= first_name
        appoint.age=age
        appoint.blood_group=blood
        appoint.email=email
        appoint.address=address
        appoint.date=date
        appoint.time=time
        appoint.result=result
        appoint.save()

        if result =='Negativee':
            add=donor(
                name=name,
                first_name=first_name,
                age=age,
                blood_group=blood,
                email=email,
                address=address,
                date=date,
                time=time,
                result=result

            )
            add.save()
        return redirect('profile')  

    return render(request,'edit.html',{'appoint':appoint})

def donorpage(request):
    AllDonor = donor.objects.filter(result = 'Negativee')
    numOfDonor = donor.objects.filter(result = 'Negativee').count()

    context = {
        'AllDonor': AllDonor,
        'numOfDonor':numOfDonor,
    }

    return render(request,'plasma_donor.html',context)