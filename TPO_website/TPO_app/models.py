from django.db import models

# Create your models here.
class StudentInfo(models.Model):
    uname = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=200)
    phoneno = models.CharField(max_length=200)
    event = models.CharField(max_length=20)
    
    def __str__(self):
        return self.uname


class JobInfo(models.Model):
    uname = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=200)
    phoneno = models.CharField(max_length=200)
    college = models.CharField(max_length=20)
    graduation = models.DecimalField(max_digits=19, decimal_places=2)
    company = models.CharField(max_length=200)
    profile = models.CharField(max_length=200)

    def __str__(self):
        return self.company
        
class EventInfo(models.Model):
    eventname = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    eventdate = models.CharField(max_length=200)
    
    def __str__(self):
        return self.eventname

class CompanyInfo(models.Model):
    cname = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    salary = models.CharField(max_length=200)
    
    def __str__(self):
        return self.cname

from django.db import models

class NOCRequest(models.Model):
    PURPOSE_CHOICES = [
        ('Internship', 'Internship'),
        ('Placement', 'Placement'),
        ('Higher Studies', 'Higher Studies'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    roll = models.CharField(max_length=50)
    branch = models.CharField(max_length=100)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    message = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to='noc_documents/')
    status = models.CharField(max_length=20, default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.purpose}"
