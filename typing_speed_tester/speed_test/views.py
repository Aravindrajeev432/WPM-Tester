from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import TypingTest, CustomWord
import random

def home(request):
    words_count = CustomWord.objects.count()
    return render(request, 'speed_test/home.html', {'words_count': words_count})

def get_text(request):
    words = list(CustomWord.objects.values_list('word', flat=True))
    if not words:
        return JsonResponse({
            'text': '',
            'error': 'No words available. Please add some words first.'
        })
    
    # Get word count from request, default to 10
    word_count = int(request.GET.get('word_count', 10))
    # Ensure word count is between 10 and 25
    word_count = max(10, min(25, word_count))
    # Ensure we don't try to select more words than available
    word_count = min(len(words), word_count)
    
    # Get the specified number of random words
    selected_words = random.sample(words, word_count)
    text = ' '.join(selected_words)
    return JsonResponse({'text': text})

def save_result(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        wpm = request.POST.get('wpm')
        accuracy = request.POST.get('accuracy')
        time_taken = request.POST.get('time_taken')
        
        test = TypingTest.objects.create(
            text=text,
            wpm=int(wpm),
            accuracy=float(accuracy),
            time_taken=float(time_taken)
        )
        
        return JsonResponse({'status': 'success', 'id': test.id})
    return JsonResponse({'status': 'error'}, status=400)

def view_results(request):
    # Get all results ordered by most recent first
    results = TypingTest.objects.all().order_by('-created_at')
    
    # Add word count to each result
    for result in results:
        result.word_count = len(result.text.split())
    
    return render(request, 'speed_test/results.html', {'results': results})

def manage_words(request):
    if request.method == 'POST':
        text = request.POST.get('words', '').strip()
        if text:
            # Split text into words and remove duplicates
            words = set(word.strip() for word in text.split())
            
            # Add new words to database, skip existing ones
            for word in words:
                CustomWord.objects.get_or_create(word=word)
    
    words = CustomWord.objects.all().order_by('-created_at')
    return render(request, 'speed_test/manage_words.html', {'words': words})

def delete_word(request, word_id):
    if request.method == 'POST':
        CustomWord.objects.filter(id=word_id).delete()
    return redirect('speed_test:manage_words')
