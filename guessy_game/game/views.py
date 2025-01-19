import random
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Game

def get_secret_num():
    """Generates a secret number with unique digits."""
    numbers = list('0123456789')
    random.shuffle(numbers)
    return ''.join(numbers[:3])

def get_clues(guess, secret_number):
    """Returns clues based on the player's guess."""
    if guess == secret_number:
        return ['You got it!']

    clues = []
    for i in range(len(guess)):
        if guess[i] == secret_number[i]:
            clues.append('Woza')  # Correct digit in the correct position
        elif guess[i] in secret_number:
            clues.append('Chop_rice')  # Correct digit but in the wrong position

    if not clues:
        return ['Yooh!']  # No correct digits

    return clues

def index(request):
    if request.method == 'POST':
        # Start a new game
        secret_number = get_secret_num()
        Game.objects.create(secret_number=secret_number, guesses=0)
        return redirect('play')

    return render(request, 'index.html')

def play(request):
    game = Game.objects.last()  # Get the latest game instance

    if request.method == 'POST':
        guess = request.POST.get('guess')
        clues = get_clues(guess, game.secret_number)

        if guess == game.secret_number:
            messages.success(request, f'You got it! The secret number was {game.secret_number}')
            return redirect('index')  # Redirect to index after winning
        
        game.guesses += 1
        game.save()

        if game.guesses >= 10:
            messages.info(request, f'Game Over! The correct number was {game.secret_number}')
            return redirect('index')  # Redirect to index after game over

        return render(request, 'play.html', {'clues': clues})

    return render(request, 'play.html')

