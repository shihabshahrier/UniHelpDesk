from django.urls import path
from . import views


urlpatterns = [
    path('', views.studentLogin, name='studentLogin'),
    path('student-login/', views.studentLogin, name='studentLogin'),
    path('faculty-login/', views.facultyLogin, name='facultyLogin'),
    path('staff-login/', views.staffLogin, name='staffLogin'),
    path('student-register/', views.studentRegister, name='studentRegister'),
    path('student-profile/', views.studentProfile, name='studentProfile'),
    path('faculty-profile/', views.facultyProfile, name='facultyProfile'),
    path('staff-profile/', views.staffProfile, name='staffProfile'),
    path('student-profile-update/', views.studentProfileUpdate, name='studentProfileUpdate'),
    path('faculty-course-view/', views.facultyCourseView, name='facultyCourseView'),
    path('course-view/', views.courseView, name='courseView'),
    path('add-course/', views.addCourse, name='addCourse'),
    path('course-content/<str:course_id>/', views.courseContent, name='courseContent'),
    path('add-course-content/<str:course_id>/', views.addCourseContent, name='addCourseContent'),
    path('post-announcement/', views.postAnnouncement, name='postAnnouncement'),
    path('post-complain/', views.postComplain, name='postComplain'),
    path('student-announcement-view/', views.studentAnnouncementView, name='studentAnnouncementView'),
    path('faculty-announcement-view/', views.facultyAnnouncementView, name='facultyAnnouncementView'),
    path('staff-announcement-view/', views.staffAnnouncementView, name='staffAnnouncementView'),
    path('complain-student-view/', views.complainStudentView, name='complainStudentView'),
    path('complain-staff-view/', views.complainStaffView, name='complainStaffView'),
    path('payment/', views.payment, name='payment'),
    path('logout/', views.logoutUser, name='logoutUser'),

]

