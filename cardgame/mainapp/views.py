from django.shortcuts import render, redirect
from django.views import View
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from mainapp import models, game_engine, cards
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(View):
    def get(self, request):
        ctx = {'username': request.user.username}
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
            return redirect('home')
        else:
            ctx = {'username': request.user.username, 'user': user}
            return render(request, 'login.html', ctx)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')

class Profile(View):
    def get(self, request):
        user = request.user
        player = models.HumanPlayer.objects.get(user=user)
        ctx = {'username': request.user.username, 'user': user, 'player': player}
        return render(request, 'profile.html', ctx)


class GameModeChoice(LoginRequiredMixin, View):
    def get(self, request):
        user_id = request.user.id
        initial_states = models.HumanPlayer.objects.get(user_id=user_id).initial_states.all()
        ctx = {'username': request.user.username, 'initial_states': initial_states}
        return render(request, "gamemodechoice.html", ctx)
    def post(self, request):
        user_id = request.user.id
        initial_state = models.HumanPlayer.objects.filter(user_id=user_id)
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
        try:
            game_mode = models.InitialState.objects.get(tower=tower, wall=wall, mine=mine, gold=gold, fountain=fountain,
                                                        mana=mana, farm=farm, food=food, cov_tower=cov_tower,
                                                        cov_resources=cov_resources)
        except:
            game_mode = models.InitialState.objects.create(tower=tower, wall=wall, mine=mine, gold=gold,
                                                           fountain=fountain, mana=mana, farm=farm, food=food,
                                                           cov_tower=cov_tower, cov_resources=cov_resources)
        player = models.HumanPlayer.objects.get(user_id=user_id)
        player.initial_states.add(game_mode)
        ctx = {'username': request.user.username, 'initial_state': initial_state}
        return render(request, "gamemodechoice.html", ctx)

class Match(LoginRequiredMixin, View):
    def get(self, request):
        buttons = ['card1_usage', 'card2_usage', 'card3_usage', 'card4_usage', 'card5_usage']
        if not (request.GET.get(buttons[0]) or request.GET.get(buttons[1]) or request.GET.get(buttons[2])
                or request.GET.get(buttons[3]) or request.GET.get(buttons[4])):
            # UWAGA! NA RAZIE TYLKO JEDEN INITIAL STATE
            initial_state = models.InitialState.objects.get(tower=20, wall=10, mine=3, fountain=2, farm=3, gold=10,
                                                            mana=15,
                                                            food=10, cov_tower=60, cov_resources=250)
            try:
                game_engine.start_game(request, initial_state)
            except IntegrityError:
                pass
        else:
            game_engine.player1_card_usage(request)
            game_engine.check_victory_conditions(request)
        player1_state = models.Player1State.objects.get(user=request.user)
        match = models.MatchState.objects.get(player1=player1_state)
        player2_state = models.Player2State.objects.get()
        player1_state.save()
        match.save()
        player2_state.save()
        card_names = [models.CARDS[match.player1.card1-1], models.CARDS[match.player1.card2-1],
                      models.CARDS[match.player1.card3-1], models.CARDS[match.player1.card4-1],
                      models.CARDS[match.player1.card5-1]]
        card1_name = card_names[0][1]
        card2_name = card_names[1][1]
        card3_name = card_names[2][1]
        card4_name = card_names[3][1]
        card5_name = card_names[4][1]
        ctx = {'username': request.user.username, "match": match, "card1_name": card1_name, "card2_name": card2_name,
               "card3_name": card3_name, "card4_name": card4_name, "card5_name": card5_name}
        try:
            last_card_name = models.CARDS[match.last_card - 1][1]
            ctx["last_card_name"] = last_card_name
        except TypeError:
            pass
        try:
            second_last_card_name = models.CARDS[match.second_last_card-1][1]
            ctx["second_last_card_name"] = second_last_card_name
        except TypeError:
            pass
        return render(request, "match.html", ctx)
