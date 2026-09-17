from django.urls import path

from .views import (
    BudgetListCreateAPIView, BudgetDetailAPIView,
    BudgetLineListCreateAPIView, BudgetLineDetailAPIView,
    FixedCostListCreateAPIView, FixedCostDetailAPIView,
    RevenueTargetListCreateAPIView, RevenueTargetDetailAPIView,
    COGSTargetListCreateAPIView, COGSTargetDetailAPIView,
    ForecastListCreateAPIView, ForecastDetailAPIView,
    RekapPurchaseOrderListAPIView, RekapPurchaseOrderDetailAPIView,
    RekapPurchaseOrderLiveAPIView, RekapPurchaseOrderGenerateAPIView,
)

urlpatterns = [
    path('budget/', BudgetListCreateAPIView.as_view(), name='finance-budget-list'),
    path('budget/<int:pk>/', BudgetDetailAPIView.as_view(), name='finance-budget-detail'),
    path('budget/<int:budget_pk>/lines/', BudgetLineListCreateAPIView.as_view(), name='finance-budgetline-list'),
    path('budget/<int:budget_pk>/lines/<int:pk>/', BudgetLineDetailAPIView.as_view(), name='finance-budgetline-detail'),

    path('fixed-cost/', FixedCostListCreateAPIView.as_view(), name='finance-fixedcost-list'),
    path('fixed-cost/<int:pk>/', FixedCostDetailAPIView.as_view(), name='finance-fixedcost-detail'),

    path('revenue-target/', RevenueTargetListCreateAPIView.as_view(), name='finance-revenuetarget-list'),
    path('revenue-target/<int:pk>/', RevenueTargetDetailAPIView.as_view(), name='finance-revenuetarget-detail'),

    path('cogs-target/', COGSTargetListCreateAPIView.as_view(), name='finance-cogstarget-list'),
    path('cogs-target/<int:pk>/', COGSTargetDetailAPIView.as_view(), name='finance-cogstarget-detail'),

    path('forecast/', ForecastListCreateAPIView.as_view(), name='finance-forecast-list'),
    path('forecast/<int:pk>/', ForecastDetailAPIView.as_view(), name='finance-forecast-detail'),

    path('rekap/purchase-order/', RekapPurchaseOrderListAPIView.as_view(), name='finance-rekap-po-list'),
    path('rekap/purchase-order/<int:pk>/', RekapPurchaseOrderDetailAPIView.as_view(), name='finance-rekap-po-detail'),
    path('rekap/purchase-order/live/', RekapPurchaseOrderLiveAPIView.as_view(), name='finance-rekap-po-live'),
    path('rekap/purchase-order/generate/', RekapPurchaseOrderGenerateAPIView.as_view(), name='finance-rekap-po-generate'),
]