from django.urls import path
from aplicatie2 import views
# pentru api decomentam din: api.py, views.py, aici

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('update_balance/', views.AddTransactionView.as_view(), name='add_transaction'),
    path('success/', views.update_success, name='add_successful'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('currency_exchange/', views.exchange_rates_view, name='currency_exchange'),        #merge dar consumam api:)
    path('export_history_pdf/', views.export_history_pdf, name='export_history_pdf'),
]
