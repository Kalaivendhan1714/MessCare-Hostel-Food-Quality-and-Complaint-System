from django.db import models

# Create your models here.
class UserDetails(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=10)
    hostel_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    room_no = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    student_name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=20)
    hostel_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    complaint_type = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return self.student_name

class Feedback(models.Model):
    student_name = models.CharField(max_length=100)
    hostel_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    rating = models.IntegerField(
        choices=[
            (1, 'Very Poor'),
            (2, 'Poor'),
            (3, 'Average'),
            (4, 'Good'),
            (5, 'Excellent'),
        ]
    )
    feedback = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name

class TodayDish(models.Model):
    breakfast = models.CharField(max_length=200)
    breakfast_time = models.CharField(max_length=50)

    lunch = models.CharField(max_length=200)
    lunch_time = models.CharField(max_length=50)

    dinner = models.CharField(max_length=200)
    dinner_time = models.CharField(max_length=50)

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.date)


class FoodSafetyComplaint(models.Model):
    student_name = models.CharField(max_length=100)
    hostel_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=20)
    food_type = models.CharField(max_length=20)
    issue_type = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    photo = models.ImageField(
        upload_to='food_safety/',
        null=True,
        blank=True
    )

    votes = models.IntegerField(default=0)
    status = models.CharField(
        max_length=30,
        default='Pending'
    )

    def __str__(self):
        return self.student_name

class FoodSafetyVote(models.Model):
    complaint = models.ForeignKey(
        FoodSafetyComplaint,
        on_delete=models.CASCADE
    )

    student = models.ForeignKey(
        UserDetails,
        on_delete=models.CASCADE
    )

    student_name = models.CharField(max_length=100)
    hostel_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('complaint', 'student')

    def __str__(self):
        return self.student_name