from django.urls import path
from .views import (
    AccountListCreate,
    AccountDetail
)

urlpatterns = [
    path('accounts/', AccountListCreate.as_view(), name='account-list-create'),
    path('accounts/<uuid:pk>/', AccountDetail.as_view(), name='account-detail')
]
