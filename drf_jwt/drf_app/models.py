from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.models import AbstractUser

from drf_app.utils import define_exp_date



class RefCode(models.Model):
    ref_code = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name = 'Пользователь')
    creation_date = models.DateField(auto_now=True, verbose_name = 'Дата создания')
    exp_date = models.DateField(default=define_exp_date, verbose_name = 'Дата истечения срока')
    referrer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals', verbose_name='Реферер')

    def is_exp(self):
        return self.exp_date < timezone.now()
    

    
class User(AbstractUser):
     referral_id = models.ForeignKey(
        RefCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_referrals')
     groups = models.ManyToManyField(Group, verbose_name=('groups'), blank=True, help_text=('The groups this user belongs to. permissions granted to each of their groups.'),
                                    related_name='custom_user_groups') 
     
     user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='custom_user_permissions')
              


