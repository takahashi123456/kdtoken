from django.shortcuts import redirect, render
from .models import *
from .forms import *
import django.views.generic as View
from rest_framework import viewsets
from .serializers import SampleSerializer


class IndexView(View.TemplateView):
    template_name = 'base.html'

# class HorseViewSet(viewsets.ModelViewSet):
#     """PostオブジェクトのCRUD"""
#     queryset = SampleModel.objects.all().order_by('-created_at')
#     serializer_class = SampleSerializer

# def index():

def test(request):
    race_data = HorseModel.objects.get(race_id=3)

    context = {
    'test': race_data
    }
    return render(request, 'index.html', context)