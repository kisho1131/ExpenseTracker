from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=266)

    def __str__(self) -> str:
        return self.owner.username + " --> Rs " + str(self.amount)+ " ( "+ self.category +" )"

    class Meta:
        ordering= ['-date']

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.name
