from django.shortcuts import render, redirect
from django.contrib import messages

from .models import (
    UserDetails,
    Complaint,
    Feedback,
    TodayDish,
    FoodSafetyComplaint,
    FoodSafetyVote
)


# ===================== REGISTRATION SIDE =====================

def register(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        hostel_name = request.POST.get('hostel_name')
        branch_name = request.POST.get('branch_name')
        room_no = request.POST.get('room_no')
        password = request.POST.get('password')

        user = UserDetails(
            name=name,
            email=email,
            phone_no=phone_no,
            hostel_name=hostel_name,
            branch_name=branch_name,
            room_no=room_no,
            password=password
        )

        user.save()

        messages.success(
            request,
            'Registration successful! You can now login.'
        )

        return redirect('login')

    return render(
        request,
        'register.html'
    )


# ===================== STUDENT LOGIN =====================

def login(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        password = request.POST.get('password')

        # Admin Login

        if name == 'admin' and password == 'admin123':

            request.session['admin_logged_in'] = True

            return redirect('adminpage')

        # Student Login

        users = UserDetails.objects.filter(
            name=name,
            password=password
        )

        if users.exists():

            user = users.first()

            request.session['user_id'] = user.id

            return redirect(
                'studentpage',
                user_id=user.id
            )

        else:

            return render(
                request,
                'login.html',
                {
                    'error': 'Invalid name or password!'
                }
            )

    return render(
        request,
        'login.html'
    )


# ===================== ADMIN LOGIN =====================

def adminlogin(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin' and password == 'admin123':

            request.session['admin_logged_in'] = True

            messages.success(
                request,
                'Welcome Admin! Login successful.'
            )

            return redirect('adminpage')

        else:

            return render(
                request,
                'adminlogin.html',
                {
                    'error': 'Invalid admin username or password'
                }
            )

    return render(
        request,
        'adminlogin.html'
    )


# ===================== LOGOUT =====================

def logout(request):

    request.session.flush()

    messages.success(
        request,
        'Logged out successfully!'
    )

    return redirect('login')


# ===================== STUDENT PAGE =====================

def studentpage(request, user_id):

    user = UserDetails.objects.get(
        id=user_id
    )

    return render(
        request,
        'studentpage.html',
        {
            'user': user
        }
    )


# ===================== TODAY'S DISH =====================

def todaydish(request, user_id):

    dish = TodayDish.objects.last()

    user = UserDetails.objects.get(
        id=user_id
    )

    return render(
        request,
        'todaydish.html',
        {
            'dish': dish,
            'user': user
        }
    )


# ===================== FEEDBACK =====================

def feedback(request, user_id):

    user = UserDetails.objects.get(
        id=user_id
    )

    if request.method == 'POST':

        rating = request.POST.get('rating')
        feedback_text = request.POST.get('feedback')

        Feedback.objects.create(
            student_name=user.name,
            hostel_name=user.hostel_name,
            branch_name=user.branch_name,
            rating=rating,
            feedback=feedback_text
        )

        messages.success(
            request,
            'Feedback submitted successfully!'
        )

        return redirect(
            'feedback',
            user_id=user.id
        )

    return render(
        request,
        'feedback.html',
        {
            'user': user
        }
    )

# ===================== COMPLAINT =====================

def complaintpage(request, user_id):

    user = UserDetails.objects.get(
        id=user_id
    )

    if request.method == 'POST':

        complaint_type = request.POST.get(
            'complaint_type'
        )

        description = request.POST.get(
            'description'
        )

        Complaint.objects.create(
            student_name=user.name,
            hostel_name=user.hostel_name,
            branch_name=user.branch_name,
            room_number=user.room_no,
            complaint_type=complaint_type,
            description=description
        )

        messages.success(
            request,
            'Complaint submitted successfully!'
        )

        return redirect(
            'complaintpage',
            user_id=user.id
        )

    return render(
        request,
        'complaintpage.html',
        {
            'user': user
        }
    )


# ===================== ADMIN DASHBOARD =====================

def adminpage(request):

    if not request.session.get('admin_logged_in'):

        return redirect('adminlogin')


    # Dashboard statistics

    total_users = UserDetails.objects.count()

    total_feedback = Feedback.objects.count()

    total_complaints = Complaint.objects.count()

    total_food_safety = FoodSafetyComplaint.objects.count()


    pending_complaints = Complaint.objects.filter(
        status='Pending'
    ).count()


    resolved_complaints = Complaint.objects.filter(
        status='Resolved'
    ).count()


    escalated_reports = FoodSafetyComplaint.objects.filter(
        status='Escalated'
    ).count()


    pending_food_safety = FoodSafetyComplaint.objects.filter(
        status='Pending'
    ).count()


    escalated_food_safety = FoodSafetyComplaint.objects.filter(
        status='Escalated'
    ).count()



    # ===================== BRANCH SUMMARY =====================

    branch_summary = []

    branches = UserDetails.objects.values(
        'hostel_name',
        'branch_name'
    ).distinct()


    for branch in branches:

        hostel = (
            branch['hostel_name'] or ''
        ).strip()

        branch_name = (
            branch['branch_name'] or ''
        ).strip()


        # Skip empty hostel / branch

        if not hostel or not branch_name:

            continue


        # Check duplicate hostel + branch

        already_exists = False


        for item in branch_summary:

            if (
                item['hostel_name'].lower()
                == hostel.lower()

                and

                item['branch_name'].lower()
                == branch_name.lower()
            ):

                already_exists = True

                break


        if already_exists:

            continue


        # Students count

        students = UserDetails.objects.filter(
            hostel_name__iexact=hostel,
            branch_name__iexact=branch_name
        ).count()


        # Complaint count

        complaints = Complaint.objects.filter(
            hostel_name__iexact=hostel,
            branch_name__iexact=branch_name
        ).count()


        # Food safety count

        safety_reports = FoodSafetyComplaint.objects.filter(
            hostel_name__iexact=hostel,
            branch_name__iexact=branch_name
        ).count()


        branch_summary.append(
            {
                'hostel_name': hostel,
                'branch_name': branch_name,
                'students': students,
                'complaints': complaints,
                'safety_reports': safety_reports,
            }
        )



    # ===================== CHART DATA =====================

    branch_chart_data = {
        'labels': [],
        'students': [],
        'complaints': [],
        'safety_reports': []
    }


    for branch in branch_summary:

        branch_chart_data['labels'].append(
            f"{branch['hostel_name']} - {branch['branch_name']}"
        )


        branch_chart_data['students'].append(
            branch['students']
        )


        branch_chart_data['complaints'].append(
            branch['complaints']
        )


        branch_chart_data['safety_reports'].append(
            branch['safety_reports']
        )


    chart_data = {

        'pending_complaints':
            pending_complaints,

        'resolved_complaints':
            resolved_complaints,

        'escalated_reports':
            escalated_reports,

        'branch_chart':
            branch_chart_data
    }



    # ===================== ADMIN DASHBOARD =====================

    return render(
        request,
        'adminpage.html',
        {
            'total_users': total_users,

            'total_feedback': total_feedback,

            'total_complaints': total_complaints,

            'total_food_safety':
                total_food_safety,

            'pending_complaints':
                pending_complaints,

            'resolved_complaints':
                resolved_complaints,

            'escalated_reports':
                escalated_reports,

            'branch_summary':
                branch_summary,

            'pending_food_safety':
                pending_food_safety,

            'escalated_food_safety':
                escalated_food_safety,

            'chart_data':
                chart_data,
        }
    )

# ===================== ADD TODAY'S DISH =====================

def adddish(request):

    if not request.session.get('admin_logged_in'):

        return redirect('adminlogin')


    if request.method == 'POST':

        breakfast = request.POST.get(
            'breakfast'
        )

        breakfast_time = request.POST.get(
            'breakfast_time'
        )

        lunch = request.POST.get(
            'lunch'
        )

        lunch_time = request.POST.get(
            'lunch_time'
        )

        dinner = request.POST.get(
            'dinner'
        )

        dinner_time = request.POST.get(
            'dinner_time'
        )


        dish = TodayDish(
            breakfast=breakfast,
            breakfast_time=breakfast_time,
            lunch=lunch,
            lunch_time=lunch_time,
            dinner=dinner,
            dinner_time=dinner_time
        )

        dish.save()


        messages.success(
            request,
            "Today's dish added successfully!"
        )

        return redirect('adddish')


    return render(
        request,
        'adddish.html'
    )


# ===================== VIEW FEEDBACK =====================

def viewfeedback(request):

    if not request.session.get('admin_logged_in'):

        return redirect('adminlogin')


    feedbacks = Feedback.objects.all()


    return render(
        request,
        'viewfeedback.html',
        {
            'feedbacks': feedbacks
        }
    )


# ===================== VIEW COMPLAINTS =====================

def viewcomplaints(request):

    if not request.session.get('admin_logged_in'):

        return redirect('adminlogin')


    complaints = Complaint.objects.all()


    return render(
        request,
        'viewcomplaints.html',
        {
            'complaints': complaints
        }
    )

# ===================== MY COMPLAINTS =====================

def my_complaints(request, user_id):

    user = UserDetails.objects.get(
        id=user_id
    )

    complaints = Complaint.objects.filter(
        student_name=user.name
    ).order_by(
        '-date'
    )

    return render(
        request,
        'my_complaints.html',
        {
            'user': user,
            'complaints': complaints
        }
    )

# ===================== MY FOOD SAFETY REPORTS =====================

def my_food_safety_reports(request, user_id):

    user = UserDetails.objects.get(
        id=user_id
    )

    reports = FoodSafetyComplaint.objects.filter(
        student_name=user.name
    ).order_by(
        '-date'
    )

    return render(
        request,
        'my_food_safety_reports.html',
        {
            'user': user,
            'reports': reports
        }
    )
# ===================== RESOLVE COMPLAINT =====================

def update_complaint_status(request, cid):

    if not request.session.get('admin_logged_in'):
        return redirect('adminlogin')

    complaint = Complaint.objects.get(
        id=cid
    )

    if request.method == 'POST':

        new_status = request.POST.get('status')

        if new_status in [
            'Pending',
            'In Progress',
            'Resolved'
        ]:

            complaint.status = new_status
            complaint.save()

            messages.success(
                request,
                f'Complaint status changed to {new_status}.'
            )

    return redirect('viewcomplaints')

# ===================== FOOD SAFETY COMPLAINT =====================

def foodsafety(request, user_id):

    user = UserDetails.objects.get(
        id=user_id
    )


    if request.method == 'POST':

        food_type = request.POST.get(
            'food_type'
        )

        issue_type = request.POST.get(
            'issue_type'
        )

        description = request.POST.get(
            'description'
        )

        photo = request.FILES.get(
            'photo'
        )


        FoodSafetyComplaint.objects.create(
            student_name=user.name,
            hostel_name=user.hostel_name,
            branch_name=user.branch_name,
            room_number=user.room_no,
            food_type=food_type,
            issue_type=issue_type,
            description=description,
            photo=photo
        )


        messages.success(
            request,
            'Food safety complaint submitted successfully!'
        )


        return redirect(
            'foodsafety',
            user_id=user.id
        )


    return render(
        request,
        'foodsafety.html',
        {
            'user': user
        }
    )


# ===================== VIEW FOOD SAFETY =====================

def viewfoodsafety(request):

    if not request.session.get('admin_logged_in'):

        return redirect('adminlogin')


    complaints = FoodSafetyComplaint.objects.all().order_by(
        '-date'
    )


    for complaint in complaints:

        complaint.voter_list = FoodSafetyVote.objects.filter(
            complaint=complaint
        )


    return render(
        request,
        'viewfoodsafety.html',
        {
            'complaints': complaints
        }
    )

def resolve_food_safety(request, cid):

    if not request.session.get('admin_logged_in'):
        return redirect('adminlogin')

    complaint = FoodSafetyComplaint.objects.get(
        id=cid
    )

    complaint.status = 'Resolved'
    complaint.save()

    return redirect('viewfoodsafety')


# ===================== STUDENT FOOD SAFETY LIST =====================

def food_safety_list(request, user_id):

    user = UserDetails.objects.get(
        id=user_id
    )

    complaints = FoodSafetyComplaint.objects.all().order_by(
        '-date'
    )

    return render(
        request,
        'food_safety_list.html',
        {
            'user': user,
            'complaints': complaints
        }
    )


# ===================== FOOD SAFETY VOTE =====================

def vote_food_safety(request, cid, user_id):

    complaint = FoodSafetyComplaint.objects.get(
        id=cid
    )

    user = UserDetails.objects.get(
        id=user_id
    )


    # Make sure student belongs to same hostel + branch

    if (
        complaint.hostel_name.strip().lower()
        != user.hostel_name.strip().lower()
        or
        complaint.branch_name.strip().lower()
        != user.branch_name.strip().lower()
    ):

        return redirect(
            'food_safety_list',
            user_id=user_id
        )


    # Check whether already voted

    already_voted = FoodSafetyVote.objects.filter(
        complaint=complaint,
        student=user
    ).exists()


    if not already_voted:

        FoodSafetyVote.objects.create(
            complaint=complaint,
            student=user,
            student_name=user.name,
            hostel_name=user.hostel_name,
            branch_name=user.branch_name
        )


        complaint.votes += 1


        if complaint.votes >= 10:

            complaint.status = 'Escalated'


        complaint.save()


    return redirect(
        'food_safety_list',
        user_id=user_id
    )


# ===================== VIEW USERS =====================

def viewusers(request):

    if not request.session.get('admin_logged_in'):
        return redirect('adminlogin')

    users = UserDetails.objects.all().order_by(
        'hostel_name',
        'branch_name',
        'name'
    )

    branch_users = {}

    for user in users:

        hostel = (user.hostel_name or '').strip()
        branch = (user.branch_name or '').strip()

        key = f"{hostel} - {branch}"

        if key not in branch_users:
            branch_users[key] = []

        branch_users[key].append(user)


    # ===================== COUNTS =====================

    total_students = users.count()

    total_groups = len(branch_users)

    total_hostels = UserDetails.objects.values(
        'hostel_name'
    ).distinct().count()


    return render(
        request,
        'viewusers.html',
        {
            'branch_users': branch_users,
            'total_students': total_students,
            'total_groups': total_groups,
            'total_hostels': total_hostels,
        }
    )

# ===================== EDIT USER =====================

def edituser(request, user_id):

    if not request.session.get('admin_logged_in'):
        return redirect('adminlogin')

    user = UserDetails.objects.get(id=user_id)

    if request.method == 'POST':

        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.phone_no = request.POST.get('phone_no')
        user.hostel_name = request.POST.get('hostel_name')
        user.branch_name = request.POST.get('branch_name')
        user.room_no = request.POST.get('room_no')

        user.save()

        messages.success(
            request,
            'User details updated successfully!'
        )

        return redirect('viewusers')

    return render(
        request,
        'edituser.html',
        {
            'user': user
        }
    )

# ===================== DELETE USER =====================

def deleteuser(request, user_id):

    if not request.session.get('admin_logged_in'):

        return redirect('adminlogin')


    user = UserDetails.objects.get(
        id=user_id
    )


    user.delete()


    messages.success(
        request,
        'Student detail is successfully deleted!'
    )


    return redirect(
        'viewusers'
    )