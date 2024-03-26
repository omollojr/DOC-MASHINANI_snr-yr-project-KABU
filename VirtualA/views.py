from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from .models import Patient, ActivityLog, Services



# Create your views here.
def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken! Please try again.')
                return redirect('/')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken! Please try again.')
                return redirect('/')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
                send_user_id_email(user)  # Sending email after successful registration
                return redirect('login/')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('/')
    else:  
        return render(request, 'signup.html')
    
def send_user_id_email(user):
    subject = 'Your User ID'
    html_message = render_to_string('email_template.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email

    email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
    email.attach_alternative(html_message, "text/html")
    email.send()


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user with provided email exists
        user = User.objects.filter(email=email).first()

        if user is not None:
            # Verify password
            if user.check_password(password):
                # Authentication successful, log in the user
                auth.login(request, user)
                return redirect('/home')
            else:
                # Incorrect password
                messages.error(request, 'Incorrect password. Please try again.')
                return redirect('/login')
        else:
            # User not found
            messages.error(request, 'User with this email does not exist.')
            return redirect('/login')
    else:
        return render(request, 'login.html')
    
    
def home(request):
    return render(request, 'index.html')

@csrf_protect
def logout_view(request):
    logout(request)
    messages.success(request, 'You logged out')
    return redirect('login.html')
    

def about(request):
    return render(request, 'about.html')

def service(request):
    if request.method == 'POST':
        # Retrieve form data
        access_id = request.POST.get('Access_id')
        service_name = request.POST.get('service_name')
        email = request.POST.get('email')
        date_time = request.POST.get('date_time')
        next_visit_date = request.POST.get('next_visit_date')
        notes = request.POST.get('notes')
        refer_to_hospital = request.POST.get('refer_to_hospital')

        # Match email to patient
        try:
            patient = Patient.objects.get(email=email)
        except Patient.DoesNotExist:
            # Handle if patient doesn't exist
            messages.error(request, 'Patient with this email does not exist.')
            return redirect('/service')

        # Validate access_id
        try:
            user = User.objects.get(id=access_id)
        except (User.DoesNotExist, ValueError):
            # Handle if user doesn't exist or access_id is not a valid integer
            messages.error(request, 'Invalid User ID.')
            return redirect('/service')

        # Create and save the service
        service = Services(
            user=user,
            patient=patient,
            Access_id=access_id,
            service_name=service_name,
            email=email,
            date_time=date_time,
            next_visit_date=next_visit_date,
            notes=notes,
            refer_to_hospital=refer_to_hospital
        )
        service.save()

        
        messages.success(request, 'Upload successful.')

        # Redirect to a success page or another URL
        return redirect('/home')  
    else: 
        
        return render(request, 'service.html')

def patient_search(request):
    if request.method == "GET":
        query = request.GET.get('search_query')
        if query:
            # Search in Patient table
            patients = Patient.objects.filter(email__icontains=query)
            
            # Search in Services table
            services = Services.objects.filter(patient__email__icontains=query)
            
            return render(request, 'results.html', {'patients': patients, 'services': services, 'query': query})
    
    return render(request, 'patient_search.html')


@login_required
def form(request):
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        marital_status = request.POST.get('marital_status')
        id_number = request.POST.get('id_number')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        county = request.POST.get('county')
        subcounty = request.POST.get('subcounty')
        emergency_name = request.POST.get('emergency_name')
        emergency_relationship = request.POST.get('emergency_relationship')
        emergency_phone_number = request.POST.get('emergency_phone_number')
        
        # Create a patient object
        patient = Patient(
            user=request.user,
            photo=photo,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            gender=gender,
            marital_status=marital_status,
            id_number=id_number,
            address=address,
            phone_number=phone_number,
            email=email,
            county=county,
            subcounty=subcounty,
            emergency_name=emergency_name,
            emergency_relationship=emergency_relationship,
            emergency_phone_number=emergency_phone_number,
        )
        patient.save()  # Save the patient object to the database
        
        # Log activity
        action = f"Added patient: {patient.first_name} {patient.last_name}"
        ActivityLog.objects.create(user=request.user, action=action, timestamp=timezone.now())
        
        return redirect('/patient_search')
    
    else:
        return render(request, 'form.html')


def results(request):
    return render(request, 'results.html')

def reset_link(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate password reset token
            token = default_token_generator.make_token(user)
            # Construct password reset link
            reset_link = f"http://127.0.0.1:8000/new_pass/?email={email}&token={token}"
            # Send password reset email with the link
            send_mail(
                'Password Reset',  # Email subject
                f'Please follow this link to reset your password: {reset_link}',  # Email body
                settings.EMAIL_HOST_USER,  # Sender email address
                [email],  # List of recipient email addresses
                fail_silently=False,  # Whether to raise an exception on failure
            )
            messages.success(request, 'Password reset email sent successfully.')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
    return render(request, 'reset.html')

def new_pass(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # Check if the passwords match
            if password != confirm_password:
                messages.error(request, 'Passwords do not match. Try Again!')
                return redirect('new_password/')  # Redirect back to the new password form

            # Update the user's password
            user.set_password(password)
            user.save()

            messages.success(request, 'Password updated successfully.')
            return redirect('login/')  # Redirect to the dashboard or any other appropriate page
        else:
            return render(request, 'new_password.html')
    else:
        messages.error(request, 'Invalid or expired link.')
        return redirect('login/')
 