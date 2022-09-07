from django.shortcuts import redirect, render
from .models import *
from .forms import *
import django.views.generic as View


class IndexView(View.TemplateView):
    template_name = 'base.html'

# def index():
