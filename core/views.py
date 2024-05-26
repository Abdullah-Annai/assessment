from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Account, Destination
from .serializer import AccountSerializer, DestinationSerializer
import requests

class AccountListCreate(APIView):
    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountDetail(APIView):
    def get_object(self, pk):
        return Account.objects.get(accound_id=pk)

    def get(self, request, pk):
        account = self.get_object(pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def put(self, request, pk):
        account = self.get_object(pk)
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            account = self.get_object(pk)
            account.destination.all().delete()
            account.delete()
            return Response({'detail':'account and destination is deleted'},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'detail':"Account doesn't exist"})

class DestinationListCreate(APIView):
    def get(self, request):
        destinations = Destination.objects.all()
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DestinationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DestinationDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Destination, pk=pk)

    def get(self, request, pk):
        destination = self.get_object(pk)
        serializer = DestinationSerializer(destination)
        return Response(serializer.data)

    def put(self, request, pk):
        destination = self.get_object(pk)
        serializer = DestinationSerializer(destination, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        destination = self.get_object(pk)
        destination.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_destinations(request, account_id):
    account = get_object_or_404(Account, accound_id=account_id)
    destinations = account.destination.all()
    serializer = DestinationSerializer(destinations, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def incoming_data(request):
    token = request.headers.get('CL-X-TOKEN')
    if not token:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        account = Account.objects.get(secret_token=token)
    except Account.DoesNotExist:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data
    if not isinstance(data, dict):
        return Response({"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

    for destination in account.destination.all():
        headers = destination.headers
        url = destination.url
        method = destination.http_method
        if method == 'GET':
            response = requests.get(url, params=data, headers=headers)
        else:
            response = requests.request(method, url, json=data, headers=headers)
        print(response.status_code, response.text)

    return Response({"status": "success"}, status=status.HTTP_200_OK)
