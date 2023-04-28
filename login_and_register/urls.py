from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout_view'),
    path('leaveform/', views.leaveform, name='leaveform'),
#     path('dashboard_redirect_after_leave_apply/', views.dashboard_redirect_after_leave_apply,
#          name='dashboard_redirect_after_leave_apply'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('admin_page', views.admin_page, name='admin_page'),
    path('leave_status_pending', views.leave_status_pending,
         name='leave_status_pending'),
    path('leave_status_approved', views.leave_status_approved,
         name='leave_status_approved'),
    path('leave_status_rejected', views.leave_status_rejected,
         name='leave_status_rejected'),
    path('pending_to_approved/<str:oid>/',
         views.pending_to_approved, name='pending_to_approved'),  # when data is to be fetched from template to view function then we use <str:oid> and when data is to be fetched from view function to template then we use {{oid}}
    path('pending_to_rejected/<str:oid>/',
         views.pending_to_rejected, name='pending_to_rejected'),
    path('approved_to_rejected/<str:oid>/',
         views.approved_to_rejected, name='approved_to_rejected'),
    path('rejected_to_approved/<str:oid>/',
         views.rejected_to_approved, name='rejected_to_approved'),
    path('approved_leave_data', views.approved_leave_data,
         name='approved_leave_data'),
     path('student_data', views.student_data,name='student_data'),
     path('ta_data', views.ta_data,name='ta_data'),
     path('faculty_data', views.faculty_data,name='faculty_data'),
     path('change_pass', views.change_pass,name='change_pass'),
]
