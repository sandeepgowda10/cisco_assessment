import json

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import RouterDetails
from .serializers import RouterDetailsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class RouterDetail(APIView):
    # permission_classes = (IsAuthenticated,)   
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'
  
    def get(self, request, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        queryset = RouterDetails.objects.filter(status=False)
        return Response({'router_data': queryset})

    def delete(self, request, *args, **kwargs):
        data = RouterDetails.objects.get(id=kwargs['router_id'])
        data.status=True
        data.save()
        return Response({'message': 'Data deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class RouterData(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'details.html'
    # serializer_class = RouterDetailsSerializer

    def get(self, request, *args, **kwargs):
        queryset = RouterDetails.objects.get(id=kwargs['router_id'])
        return Response({'data' : queryset})            

    def put(self, request, *args, **kwargs):
        snippet = RouterDetails.objects.get(id=kwargs['router_id'])
        data = json.loads(request.body)
        serializer = RouterDetailsSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            print('record saved')
            return Response({'message' : 'Record updated successfully'}, status=status.HTTP_200_OK)
        return Response({'message' : 'Record cannot be updated'})

class AddData(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'add.html'

    def get(self, request):
        return Response({'message' : 'Add new data'})

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        serializer = RouterDetailsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : 'Record inserted successfully'}, status=status.HTTP_200_OK)
        return Response({'message' : 'Record cannot be added'})


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)