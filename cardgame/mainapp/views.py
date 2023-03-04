from django.shortcuts import render
from django.views import View

class Home(View):
    def get(self, request):
        ctx = {}
        return render(request, "home.html", ctx)