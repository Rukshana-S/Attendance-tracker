from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Student, Attendance, AttendanceUser
from django.utils import timezone
from datetime import date
from django.http import HttpResponse
import datetime
from datetime import datetime
from django.db.models import Q
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# Home Page
def home(request):
    return render(request, 'home.html')

# Sign Up Page
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validation
        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        if len(password1) < 8:
            return render(request, 'signup.html', {'error': 'Password must be at least 8 characters long'})

        # Check both Django User and AttendanceUser for duplicates
        if User.objects.filter(username=username).exists() or AttendanceUser.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists() or AttendanceUser.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already registered'})

        try:
            # Create user in Django User model (for authentication)
            django_user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )

            # Create user in AttendanceUser model (for Attendancetracker.users collection)
            attendance_user = AttendanceUser.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password_hash=make_password(password1),  # Hash the password
                is_active=True,
                date_joined=timezone.now()
            )

            print(f"✅ User created in both models:")
            print(f"   Django User ID: {django_user.id}")
            print(f"   AttendanceUser ID: {attendance_user.id}")

            # Auto login after successful registration
            login(request, django_user)
            return redirect('dashboard')

        except Exception as e:
            return render(request, 'signup.html', {'error': f'Error creating account: {str(e)}'})

    return render(request, 'signup.html')

# Login Page
def user_login(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(request, username=uname, password=pwd)
        if user is not None:
            # Login with Django User
            login(request, user)

            # Update last_login in AttendanceUser model
            try:
                attendance_user = AttendanceUser.objects.get(username=uname)
                attendance_user.last_login = timezone.now()
                attendance_user.save()
                print(f"✅ Updated last_login for AttendanceUser: {uname}")
            except AttendanceUser.DoesNotExist:
                print(f"⚠️  AttendanceUser not found for: {uname}")

            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# Dashboard Page (after login)
@login_required
def dashboard(request):
    students = Student.objects.all()
    return render(request, 'dashboard.html', {'students': students})

# Mark Attendance
@login_required
def mark_attendance(request):
    students = Student.objects.all()
    if request.method == 'POST':
        today = date.today()
        for student in students:
            status = request.POST.get(str(student.id))
            Attendance.objects.create(student=student, date=today, status=status)
        return redirect('dashboard')
    return render(request, 'mark_attendance.html', {'students': students})


# View Records
@login_required
def view_attendance(request):
    records = Attendance.objects.all().order_by('-date')

    # Get filters from GET request
    date_filter = request.GET.get('date')
    class_filter = request.GET.get('class_name')
    search_query = request.GET.get('search')

    # Apply date filter if present
    if date_filter:
        try:
            parsed_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
            records = records.filter(date=parsed_date)
        except ValueError:
            pass

    # Apply class filter if present
    if class_filter:
        records = records.filter(student__class_name__icontains=class_filter)

    # Apply search filter if present (search by student name)
    if search_query:
        records = records.filter(student__name__icontains=search_query)

    return render(request, 'view_attendance.html', {'records': records})



# Calculate Averages and Defaulters
@login_required
def attendance_summary(request):
    students = Student.objects.all()
    data = []
    for student in students:
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status='Present').count()
        percentage = (present / total * 100) if total > 0 else 0
        data.append({
            'student': student,
            'percentage': round(percentage, 2),
            'is_defaulter': percentage < 75,
        })

    # Separate defaulters from the rest
    defaulters = [entry for entry in data if entry['is_defaulter']]

    return render(request, 'summary.html', {'data': data, 'defaulters': defaulters})


@login_required
def export_pdf(request):
    records = Attendance.objects.all().order_by('-date')

    template_path = 'pdf_template.html'
    context = {'records': records}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error while generating PDF')
    return response

@login_required
def export_defaulter_pdf(request):
    students = Student.objects.all()
    data = []

    # Calculate attendance percentages for all students
    for student in students:
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status='Present').count()
        percentage = (present / total * 100) if total > 0 else 0
        data.append({
            'student': student,
            'percentage': round(percentage, 2),
            'is_defaulter': percentage < 75,
        })

    # Filter defaulters
    defaulters = [entry for entry in data if entry['is_defaulter']]

    # Generate HTML for the PDF
    html = render_to_string('defaulter_pdf.html', {'defaulters': defaulters})

    # Create the response object with PDF mimetype
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="defaulter_list.pdf"'

    # Use xhtml2pdf to generate the PDF from the HTML content
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Check if there were any errors in the PDF generation
    if pisa_status.err:
        return HttpResponse('We had some errors generating the PDF. Please try again later.')

    return response

@login_required
def export_attendance_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - 50

    p.setFont("Helvetica", 12)
    p.drawString(200, y, "Attendance Report")
    y -= 30

    records = Attendance.objects.all().order_by('-date')

    for record in records:
        line = f"{record.date} | {record.student.name} ({record.student.class_name}) - {record.status}"
        p.drawString(50, y, line)
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 12)

    p.save()
    return response