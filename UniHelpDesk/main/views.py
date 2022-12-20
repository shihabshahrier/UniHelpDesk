from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Student, Faculty, Staff, Course, Course_Content, Announcement, Complain, Payment
from django.contrib.auth.decorators import login_required
from datetime import datetime



# Create your views here.


# @login_required(login_url='studentLogin')
# def index(request):
#     return render(request, 'index.html')

def studentLogin(request):
    if request.method == 'POST':
        student_id = request.POST['studentid']
        password = request.POST['password']

        user = auth.authenticate(username=student_id, password=password)

        if user is not None and Student.objects.filter(student_id=student_id).exists():
            auth.login(request, user)
            return redirect('studentProfile')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('studentLogin')
    return render(request, 'student_login.html')


def facultyLogin(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=user_name, password=password)

        if user is not None and Faculty.objects.filter(user=user).exists():
            auth.login(request, user)
            return redirect('facultyProfile')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('facultyLogin')
    return render(request, 'faculty_login.html')

def staffLogin(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=user_name, password=password)

        if user is not None and Staff.objects.filter(user=user).exists():
            auth.login(request, user)
            return redirect('staffProfile')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('staffLogin')

    return render(request, 'staff_login.html')


def studentRegister(request):
    if request.method == 'POST':
        student_id = request.POST['studentid']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=student_id).exists():
                messages.info(request, 'Username Taken')
                return redirect('studentRegister')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('studentRegister')
            else:
                user = User.objects.create_user(username=student_id, email=email, password=password)
                user.save()

                student = Student.objects.create(user=user, student_id=student_id, email=email)
                student.save()
                return redirect('studentLogin')
        else:
            messages.info(request, 'Password not matching')
            return redirect('studentRegister')  
    return render(request, 'student_reg.html')


@login_required(login_url='studentLogin')
def studentProfile(request):
    if Student.objects.filter(user=request.user).exists():
        user = request.user
        obj = User.objects.get(username=user)

        if Student.objects.filter(user=obj).exists():
            obj = Student.objects.get(user=obj)
            return render(request, 'student_profile.html', {'user': obj, "student": "student"})
        
        return render(request, 'student_profile.html', {'user': obj})
    else:
        return redirect('studentLogin')



@login_required(login_url='studentLogin')
def studentProfileUpdate(request):
    if Student.objects.filter(user=request.user).exists():
        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            phone = request.POST['phone']
            dep = request.POST['dep']
            ens = request.POST["session"]

            user = request.user

            student = Student.objects.get(user=user)

            student.first_name = fname
            student.last_name = lname
            student.email = email
            student.phone = phone
            student.department = dep
            student.enrollment_session = ens

            student.save()
            return redirect('studentProfile')
        return render(request, 'update_student_profile.html', {'user': request.user})
    else:
        return redirect('studentLogin')

@login_required(login_url='facultyLogin')
def facultyProfile(request):
    if Faculty.objects.filter(user=request.user).exists():
        user = request.user
        obj = User.objects.get(username=user)
        if Faculty.objects.filter(user=obj).exists():
            obj = Faculty.objects.get(user=obj)
            return render(request, 'faculty_profile.html', {'user': obj, "faculty": "faculty"})
        return render(request, 'faculty_profile.html', {'user': obj})
    else:
        return redirect('facultyLogin')


@login_required(login_url='staffLogin')
def staffProfile(request):
    if Staff.objects.filter(user=request.user).exists():
        user = request.user
        obj = User.objects.get(username=user)
        if Staff.objects.filter(user=obj).exists():
            obj = Staff.objects.get(user=obj)
            return render(request, 'staff_profile.html', {'user': obj, "staff": "staff"})
        return render(request, 'staff_profile.html', {'user': obj})
    else:
        return redirect('staffLogin')


@login_required(login_url='facultyLogin')
def facultyCourseView(request):
    if Faculty.objects.filter(user=request.user).exists():
        courses = Course.objects.all().order_by('course_id')
        if request.method == 'POST':
            course_id = request.POST['course_id']
            course = Course.objects.get(course_id=course_id)
            course.delete()
        return render(request, 'faculty_course_view.html', {'courses': courses})
    else:
        return redirect('facultyLogin')

@login_required(login_url='studentLogin')
def courseView(request):
    if Student.objects.filter(user=request.user).exists():
        course = Course.objects.all().order_by('course_id')
        return render(request, 'course_view.html', {'course': course})
    else:
        return redirect('studentLogin')


@login_required(login_url='facultyLogin')
def addCourse(request):
    if Faculty.objects.filter(user=request.user).exists():
        if request.method == 'POST':
            course_id = request.POST['course_id']
            course_name = request.POST['cname']
            course_description = request.POST['description']
            course_credit = request.POST['credit']
            course_faculty = request.POST['faculty']
            department = request.POST['dep']

            if course_credit.isdigit() == False:
                messages.info(request, 'Credit must be a number')
                return redirect('addCourse')
            else:
                course = Course.objects.create(course_id=course_id, course_name=course_name, course_description=course_description, course_credit=course_credit, course_faculty=course_faculty, course_department=department)
                course.save()
                return redirect('facultyCourseView')
        return render(request, 'add_course.html')
    else:
        return redirect('facultyLogin')

@login_required(login_url='studentLogin')
def courseContent(request, course_id):
    if Student.objects.filter(user=request.user).exists():
    # course = Course.objects.get(course_id=course_id)
        course_content = Course_Content.objects.all()[::-1]
        return render(request, 'course_content.html', {'content':course_content , 'course_id': course_id})
    else:
        return redirect('studentLogin')


@login_required(login_url='studentLogin')
def addCourseContent(request, course_id):
    if Student.objects.filter(user=request.user).exists():
        course_id = Course.objects.get(course_id=course_id)
        user = request.user
        if Student.objects.filter(user=user).exists():
            user = Student.objects.get(user=user)
        if request.method == 'POST':
            course_content_tag = request.POST['tag']
            course_content_description = request.POST['description']
            img = request.FILES.get('image')

            course_content = Course_Content.objects.create(course_id=course_id, course_content_tag=course_content_tag, course_content_description=course_content_description, content_img=img, datetime = datetime.now(), upload_by=user)
            course_content.save()
            return redirect(f'/course-content/{course_id}/')
        return render(request, 'add_course_content.html', {'course_id': course_id})
    else:
        return redirect('studentLogin')

@login_required(login_url='facultyLogin')
def facultyAnnouncementView(request):
    if Faculty.objects.filter(user=request.user).exists():
        obj = Announcement.objects.all()
        return render(request, 'faculty_announcement_view.html', {'obj': obj[::-1]})
    else:
        return redirect('facultyLogin')


@login_required(login_url='studentLogin')
def studentAnnouncementView(request):
    if Student.objects.filter(user=request.user).exists():
        obj = Announcement.objects.all()
        return render(request, 'student_announcement_view.html', {'obj': obj[::-1]})
    else:
        return redirect('studentLogin')


@login_required(login_url='staffLogin')
def staffAnnouncementView(request):
    if Staff.objects.filter(user=request.user).exists():
        obj = Announcement.objects.all()
        if request.method == 'POST':
            announcement_id = request.POST['aid']
            announcement = Announcement.objects.get(anumber = announcement_id)
            announcement.delete()

        return render(request, 'staff_announcement_view.html', {'obj': obj[::-1]})
    else:
        return redirect('staffLogin')


@login_required(login_url='studentLogin')
def complainStudentView(request):
    if Student.objects.filter(user=request.user).exists():
        user = request.user
        complain = Complain.objects.all()
        # n_complain = []
        # for c in complain:
        #     if c.posted_by == user:
        #         n_complain.append(c)
        # context = {
        #     'complain': n_complain[::-1]
        # }
        context = {
            'complain': complain[::-1]
        }
        return render(request, 'complain_student_view.html', context)
    else:
        return redirect('studentLogin')

@login_required(login_url='staffLogin')
def complainStaffView(request):
    if Staff.objects.filter(user=request.user).exists():
        cuser = Staff.objects.get(user=request.user)
        complain = Complain.objects.all()
        context = {
            'complain': complain[::-1]
        }
        if request.method == 'POST' and request.POST['status'] == 'resolved':
            cnum = request.POST['cnum']
            status = "resolved"
            resolved_by = cuser

            complain = Complain.objects.get(cnumber=cnum)
            complain.status = status
            complain.resolved_by = resolved_by
            complain.save()
            return redirect('complainStaffView')
        elif request.method == 'POST' and request.POST['status'] == 'rejected':
            cnum = request.POST['cnum']
            status = "rejected"
            resolved_by = cuser

            complain = Complain.objects.get(cnumber=cnum)
            complain.status = status
            complain.resolved_by = resolved_by
            complain.save()
            return redirect('complainStaffView')
        return render(request, 'complain_staff_view.html', context)
    else:
        return redirect('staffLogin')


@login_required(login_url='studentLogin')
def postComplain(request):
    if Student.objects.filter(user=request.user).exists():
        cuser = Student.objects.get(user=request.user)
        if request.method == 'POST':
            tag = request.POST['tag']
            statement = request.POST['statement']

            complain = Complain.objects.create(tag=tag, statement=statement, datetime = datetime.now(), posted_by=cuser)
            complain.save()
            return redirect('complainStudentView')
        return render(request, 'post_complain.html')
    else:
        return redirect('studentLogin')


@login_required(login_url='staffLogin')
def postAnnouncement(request):
    if Staff.objects.filter(user=request.user).exists():
        cuser = Staff.objects.get(user=request.user)
        if request.method == 'POST':
            subject = request.POST['subject']
            source = request.POST['source']
            statement = request.POST['statement']
            announcement = Announcement.objects.create(subject=subject, source=source, statement=statement, datetime = datetime.now(), posted_by=cuser)
            announcement.save()
            return redirect('staffAnnouncementView')
        return render(request, 'post_announcement.html')
    else:
        return redirect('staffLogin')

@login_required(login_url='staffLogin')
def payment(request):
    if Staff.objects.filter(user = request.user).exists():
        staff = Staff.objects.get(user = request.user)
        
        payment = Payment.objects.get(staff_username = staff)
        return render(request, 'payment.html', {'payment': payment})
    else:
        return redirect('staffLogin')


@login_required(login_url='studentLogin')
def logoutUser(request):
    if Student.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('studentLogin')
    elif Faculty.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('facultyLogin')
    elif Staff.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('staffLogin')
    else:
        logout(request)
        return redirect('studentLogin')



    









