from django.shortcuts import render, redirect
from rest_framework import generics,permissions, filters
from .models import Note
from .serializers import NoteSerializer, UserSerializer
from datetime import datetime
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class NoteList(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    serarch_fields = ['title', 'content']
    
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


# Ui for Example
def Home(request):
    if request.method in ['GET', 'POST']:
        title = request.GET.get('title', '')
        content = request.GET.get('content', '')
        
        if content: 
            Note.objects.create(
                title=title, 
                content=content, 
                created_at=datetime.now()
            )
            return redirect('/') 
    
    notes = Note.objects.all().order_by('-created_at')  
    return render(request, 'notes/index.html', {'notes': notes})


def Signin(request):
    return render(request, 'notes/sign_in.html')