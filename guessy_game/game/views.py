import random
from django.shortcuts import render, redirect
from .models import Game

def get_secret_num():
    """Generates a secret number with unique digits."""
    numbers = list('0123456789')
    random.shuffle(numbers)
    return ''.join(numbers[:3])

def index(request):
    if request.method == 'POST':
        # Start a new game
        secret_number = get_secret_num()
        Game.objects.create(secret_number=secret_number)
        return redirect('play')

    return render(request, 'index.html')

def play(request):
    game = Game.objects.last() # Get latest game instance

    if request.method == 'POST':
        guess = request.POST.get('guess')
        clues = get_clues(guess, game.secret_number)

        if guess == game.secret_number:
            return render(request, 'result.html', {'result': 'You got it!', 'clues': clues})

        game.guesses += 1
        game.save()

        if game.guesses >= 10:
            return render(request, 'result.html', {'resuult': 'Game Over!', 'clues': f'The number was {game.secret_number}'})

        return render(request, 'play.html', {'clues': clues})

    return render(request, 'play.html')

def get_clues(guess, secret_number):
    """Retuens clues based on the player's guess."""
    if guess == secret_number:
        return ['You got it!']

    clues = []
    for i in range(len(guess)):
        if guess[i] == secret_number[i]:
            clues.append('Woza') # correct digit in correct position
        elif guess[i] in secret_number:
            clues.append('Chop rice!') # correct digit but wrong position
    if not clues:
        return ['Yooh!'] #No correct digits

    return clues

