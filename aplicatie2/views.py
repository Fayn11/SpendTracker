from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .api import get_exchange_rates                                   #api
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView
from django_filters.views import FilterView
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from .api import get_exchange_rates
from .filters import TranzactieFilter
# from .utils import generate_balance_chart
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from aplicatie2.models import Tranzactie
from reportlab.lib import colors
from decimal import Decimal


class AddTransactionView(LoginRequiredMixin, CreateView):
    model = Tranzactie
    fields = ['expense_or_income', 'amount', 'category', 'description']
    template_name = 'aplicatie2/update_balance.html'

    def form_valid(self, form):
        if form.is_valid():
            instance = form.save(commit=False)
            transaction_type = form.cleaned_data['expense_or_income']
            amount = form.cleaned_data['amount']
            try:
                last_balance_transaction = Tranzactie.objects.filter(user=self.request.user).latest('date')
                last_balance = last_balance_transaction.balanta if last_balance_transaction else 0.00
            except Tranzactie.DoesNotExist:
                last_balance = 0.00

            if transaction_type == 'Expense':
                instance.balanta = last_balance - int(amount)
            elif transaction_type == 'Income':
                instance.balanta = last_balance + int(amount)
            instance.user = self.request.user
            instance.save()
            return redirect('home:add_successful')


class HistoryView(LoginRequiredMixin, FilterView):
    model = Tranzactie
    template_name = 'aplicatie2/history.html'
    filterset_class = TranzactieFilter

    def get_queryset(self):
        # Selectează doar tranzacțiile asociate utilizatorului curent
        return Tranzactie.objects.filter(user=self.request.user).order_by('-date')


@login_required()
def home(request):
    user_transactions = Tranzactie.objects.filter(user=request.user).order_by('date')

    balances = [0.0]  # Inițializează lista de balanțe cu valoarea zero
    expenses = [0.0]  # Inițializează lista de cheltuieli cu valoarea zero
    incomes = [0.0]   # Inițializează lista de venituri cu valoarea zero
    dates = []
    balance = Decimal('0.0')  # Inițializează balanța ca Decimal

    for transaction in user_transactions:
        if transaction.expense_or_income == 'Income':
            balance += transaction.amount
            incomes.append(float(transaction.amount))  # Adaugă venitul în lista de venituri
        else:
            balance -= transaction.amount
            expenses.append(float(abs(transaction.amount)))  # Adaugă valoarea absolută a cheltuielii
        balances.append(float(balance))  # Adaugă balanța ca float pentru a fi compatibilă cu Chart.js
        dates.append(transaction.date.strftime('%Y-%m-%d'))  # Adaugă datele tranzacțiilor

    last_transaction = user_transactions.last()
    if last_transaction:
        dates.append(last_transaction.date.strftime('%Y-%m-%d'))

    return render(request, 'aplicatie2/home.html', {'balanta': balance, 'dates': dates,
                                                    'balances': balances, 'expenses': expenses, 'incomes': incomes})


@login_required()
def update_success(request):
    return render(request, 'aplicatie2/update_success.html')


@login_required()
def exchange_rates_view(request):
    rates_data = get_exchange_rates()                     #api
    rates = rates_data.values
    base_currency = rates_data.keys
    return render(request, 'aplicatie2/currency_exchange.html', {'rates': rates, 'base_currency': base_currency})


@login_required
def export_history_pdf(request):
    # Creați un HttpResponse cu tipul de conținut 'application/pdf'
    response = HttpResponse(content_type='application/pdf')

    # Setarea numelui fișierului PDF
    filename = f"{request.user.username}_history.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Creați un obiect SimpleDocTemplate
    doc = SimpleDocTemplate(response, pagesize=A4)

    # Extrageți tranzacțiile utilizatorului
    transactions = Tranzactie.objects.filter(user=request.user).order_by('date')

    # Definiți datele pentru tabel
    data = [["Index", "Amount", "Type", "Category", "Date", "Description"]]
    for index, transaction in enumerate(transactions):
        data.append([
            index + 1,
            transaction.amount,
            transaction.expense_or_income,
            transaction.category,
            transaction.date.strftime("%Y-%m-%d"),
            transaction.description
        ])

    # Creați un obiect Table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Adăugați titlul și tabelul într-o listă de elemente
    elements = []

    # Adăugați titlul
    styles = getSampleStyleSheet()
    title = Paragraph(f"{request.user} transactions history", styles['Title'])
    elements.append(title)

    # Adăugați un spațiu între titlu și tabel
    elements.append(Spacer(1, 12))

    # Adăugați tabelul
    elements.append(table)

    # Construiți documentul
    doc.build(elements)

    return response

