from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    USER_TYPES = [
        ('admin', 'Admin'),
        ('lender', 'Lender'),
        ('borrower', 'Borrower')
    ]

    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(auto_now=True,null=True)

    #Basic details
    user_type = models.CharField(max_length=255, choices=USER_TYPES, default='lender')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=50,unique=True,null=True,blank=True)
    mobile = models.CharField(max_length=15,unique=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE,db_column='user_id')
    username = models.CharField(max_length=100,unique=True)
    code = models.CharField(max_length=15,unique=True)

    def __str__(self):
        return self.first_name+'('+self.username+')'

    class Meta:
        db_table = 'userprofile'

class GeneralFields(models.Model):
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    created_by_id = models.ForeignKey(UserProfile, related_name='+', on_delete=models.CASCADE,db_column='created_by_id')
    updated_on = models.DateTimeField(auto_now=True,null=True)
    updated_by_id = models.ForeignKey(UserProfile, related_name='+', on_delete=models.CASCADE,db_column='updated_by_id')

    class Meta:
        abstract=True


class AccessToken(GeneralFields):
    key = models.CharField(max_length=255)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,db_column='user_id')

    class Meta:
        db_table = 'accesstoken'
