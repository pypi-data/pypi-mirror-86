import uuid

from django.contrib.auth import get_user_model
from django.db import models


class IdMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class MoneyMixin(models.Model):
    amount = models.FloatField()
    type = models.CharField(max_length=7, choices=(('income', 'income'), ('expense', 'expense')))

    class Meta:
        abstract = True


class Budget(IdMixin):
    start_date = models.DateField()
    end_date = models.DateField()


class LineItem(IdMixin, MoneyMixin):
    budget = models.ForeignKey(Budget, null=True, on_delete=models.SET_NULL)
    category = models.CharField(max_length=100)
    sharing = models.CharField(max_length=8, choices=(('personal', 'personal'), ('shared', 'shared')))
    owner = models.ForeignKey(get_user_model(), editable=False, null=True, on_delete=models.SET_NULL)


class Transaction(IdMixin, MoneyMixin):
    line_item = models.ForeignKey(LineItem, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(get_user_model(), editable=False, null=True, on_delete=models.SET_NULL)
    merchant = models.CharField(max_length=100)
    comment = models.TextField(blank=True)
    date = models.DateField()
    last_modified = models.DateTimeField(auto_now=True)
