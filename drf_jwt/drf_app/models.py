from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from drf_app.utils import define_exp_date


class RefCode(models.Model):
    ref_code = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name = 'Пользователь')
    creation_date = models.DateField(auto_now=True, verbose_name = 'Дата создания')
    exp_date = models.DateField(default=define_exp_date, verbose_name = 'Дата истечения срока')

    def is_exp(self):
        return self.exp_date < timezone.now()
            

