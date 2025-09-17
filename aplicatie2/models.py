from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Tranzactie(models.Model):
    transanction_choises = (('Expense', 'Expense'),
                            ('Income', 'Income'),)
    category_choises = (('Food', 'Food'),
                        ('Transport', 'Transport'),
                        ('Entertainment', 'Entertainment'),
                        ('Health', 'Health'),
                        ('Gifts and Donations', 'Gifts and Donations'),
                        ('Maintenance', 'Maintenance'),
                        ('Other', 'Other'))
    expense_or_income = models.CharField(max_length=100, choices=transanction_choises)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=100, choices=category_choises)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000)
    active = models.BooleanField(default=True)
    balanta = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=None)

    def __str__(self):
        tip = "Expense" if self.expense_or_income else "Income"
        return (f'{tip}: {self.amount} euro, noua balanta este: {self.balanta}, category: {self.category},'
                f' date: {self.date}, description: {self.description}')

