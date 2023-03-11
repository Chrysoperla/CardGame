from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from mainapp import models
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(View):
    def get(self, request):
        ctx = {}
        return render(request, "home.html", ctx)


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Zalogowano")
        else:
            return HttpResponse("Logowanie nie powiodło się")

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class GameModeChoice(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {}
        return render(request, "gamemodechoice.html", ctx)
    def post(self, request):
        tower = int(request.POST.get("tower"))
        if tower < 1 or tower > 999:
            raise Exception("You can only choose numbers between 1 and 999")
        wall = int(request.POST.get("wall"))
        if wall < 0 or wall > 999:
            raise Exception("You can only choose numbers between 0 and 999")
        mine = int(request.POST.get("mine"))
        if mine < 1 or mine > 99:
            raise Exception("You can only choose numbers between 1 and 99")
        gold = int(request.POST.get("gold"))
        if gold < 1 or gold > 999:
            raise Exception("You can only choose numbers between 1 and 999")
        fountain = int(request.POST.get("fountain"))
        if fountain < 1 or fountain > 99:
            raise Exception("You can only choose numbers between 1 and 99")
        mana = int(request.POST.get("mana"))
        if mana < 1 or mana > 999:
            raise Exception("You can only choose numbers between 1 and 999")
        farm = int(request.POST.get("farm"))
        if farm < 1 or farm > 99:
            raise Exception("You can only choose numbers between 1 and 99")
        food = int(request.POST.get("food"))
        if food < 1 or food > 999:
            raise Exception("You can only choose numbers between 1 and 999")
        cov_tower = int(request.POST.get("cov_tower"))
        if cov_tower < 1 or cov_tower > 999:
            raise Exception("You can only choose numbers between 1 and 999")
        cov_resources = int(request.POST.get("cov_resources"))
        if cov_resources < 1 or cov_resources > 999:
            raise Exception("You can only choose numbers between 1 and 999")
        game_mode = models.InitialState.objects.create(tower=tower, wall=wall, mine=mine, gold=gold, fountain=fountain, mana=mana,
                                        farm=farm, food=food, cov_tower=cov_tower, cov_resources=cov_resources)
        user = request.user
        player = models.HumanPlayer.objects.get(user=user)
        player.game_modes.add(game_mode)
        ctx = {}
        return render(request, "gamemodechoice.html", ctx)

class Game(LoginRequiredMixin, View):
    def get(self):
        return HttpResponse("test")
