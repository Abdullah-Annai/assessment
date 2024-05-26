from django.urls import path
from .views import (
    AccountListCreate,
    AccountDetail,
    DestinationListCreate,
    DestinationDetail,
    get_destinations,
    incoming_data
)

urlpatterns = [
    path('accounts/', AccountListCreate.as_view(), name='account-list-create'),
    path('accounts/<uuid:pk>/', AccountDetail.as_view(), name='account-detail'),
    path('destinations/', DestinationListCreate.as_view(), name='destination-list-create'),
    path('destinations/<int:pk>/', DestinationDetail.as_view(), name='destination-detail'),
    path('accounts/<uuid:account_id>/destinations/', get_destinations, name='get_destinations'),
    path('server/incoming_data/', incoming_data, name='incoming_data'),
]
