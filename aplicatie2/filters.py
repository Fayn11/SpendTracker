import django_filters
from .models import Tranzactie


class TranzactieFilter(django_filters.FilterSet):
    class Meta:
        model = Tranzactie
        fields = ['amount', 'expense_or_income', 'category', 'date', 'description']
