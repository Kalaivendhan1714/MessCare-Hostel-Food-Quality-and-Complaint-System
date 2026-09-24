from django.urls import path
from . import views


urlpatterns = [
            path('',views.login,name='login'),
            path('register/', views.register, name='register'),
            path('admin-login/', views.adminlogin, name='adminlogin'),
            path('viewusers/', views.viewusers, name='viewusers'),
            path('adminpage/', views.adminpage, name='adminpage'),
            path('logout/', views.logout, name='logout'),
            path('studentpage/<int:user_id>/', views.studentpage, name='studentpage'),
            path('todaydish/<int:user_id>/', views.todaydish, name='todaydish'),
            path('feedback/<int:user_id>/', views.feedback, name='feedback'),
            path('complaintpage/<int:user_id>/', views.complaintpage, name='complaintpage'),
            path('adddish/',views.adddish,name='adddish'),
            path('viewfeedback/', views.viewfeedback, name='viewfeedback'),
            path('viewcomplaints/', views.viewcomplaints, name='viewcomplaints'),
            path('my-complaints/<int:user_id>/',views.my_complaints,name='my_complaints'),
            path('my-food-safety-reports/<int:user_id>/',views.my_food_safety_reports,name='my_food_safety_reports'),
            path('update-complaint-status/<int:cid>/',views.update_complaint_status,name='update_complaint_status'),
            path('foodsafety/<int:user_id>/', views.foodsafety, name='foodsafety'),
            path('viewfoodsafety/', views.viewfoodsafety, name='viewfoodsafety'),
            path('resolve-food-safety/<int:cid>/',views.resolve_food_safety,name='resolve_food_safety'),
            path('food-safety-list/<int:user_id>/', views.food_safety_list, name='food_safety_list'),
            path('vote-food-safety/<int:cid>/<int:user_id>/',views.vote_food_safety,name='vote_food_safety'),
            path('edituser/<int:user_id>/', views.edituser, name='edituser'),
            path('deleteuser/<int:user_id>/', views.deleteuser, name='deleteuser'),
] 