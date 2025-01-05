from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator
from .models import TypingTest, CustomWord
from collections import Counter
import random
import json

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
        mistakes_json = request.POST.get('mistakes', '[]')
        
        try:
            mistakes = json.loads(mistakes_json)
            # Create word-level mistakes
            word_mistakes = []
            words = text.split()
            current_pos = 0
            word_positions = {}  # Map positions to words
            
            # Build position to word mapping
            for i, word in enumerate(words):
                word_length = len(word)
                for pos in range(current_pos, current_pos + word_length):
                    word_positions[pos] = word
                current_pos += word_length + 1  # +1 for space
            
            # Process mistakes
            for mistake in mistakes:
                pos = mistake['position']
                word = word_positions.get(pos, '')
                if word:
                    word_mistakes.append({
                        'word': word,
                        'expected': mistake['expected'],
                        'typed': mistake['typed'],
                        'position': pos
                    })
            
        except json.JSONDecodeError:
            mistakes = []
            word_mistakes = []
        except Exception as e:
            print(f"Error processing mistakes: {e}")  # For debugging
            mistakes = []
            word_mistakes = []
        
        test = TypingTest.objects.create(
            text=text,
            wpm=int(wpm),
            accuracy=float(accuracy),
            time_taken=float(time_taken),
            mistakes=mistakes,
            word_mistakes=word_mistakes
        )
        
        return JsonResponse({'status': 'success', 'id': test.id})
    return JsonResponse({'status': 'error'}, status=400)

def view_results(request):
    # Get all results ordered by most recent first
    all_results = TypingTest.objects.all().order_by('-created_at')
    
    # Add word count and process mistakes for each result
    for result in all_results:
        result.word_count = len(result.text.split())
        result.mistake_count = len(result.mistakes)
    
    # Create paginator
    paginator = Paginator(all_results, 5)  # Show 5 results per page
    page_number = request.GET.get('page', 1)
    results = paginator.get_page(page_number)
    
    return render(request, 'speed_test/results.html', {'results': results})

def view_mistakes(request):
    # Get all tests ordered by most recent first
    tests = TypingTest.objects.all().order_by('-created_at')
    
    # Calculate total tests and mistakes
    total_tests = tests.count()
    total_mistakes = sum(len(test.mistakes) for test in tests)
    
    # Process word-level mistakes
    word_mistake_counts = Counter()
    letter_mistake_counts = Counter()
    wrong_typed_counts = Counter()
    common_mistakes = Counter()
    
    for test in tests:
        # Process word mistakes
        for mistake in test.word_mistakes:
            word_mistake_counts[mistake['word']] += 1
        
        # Process character mistakes
        for mistake in test.mistakes:
            letter_mistake_counts[mistake['expected']] += 1
            wrong_typed_counts[mistake['typed']] += 1
            mistake_key = (mistake['expected'], mistake['typed'])
            common_mistakes[mistake_key] += 1
    
    # Get top 10 most mistaken words
    most_mistaken_words = [
        {'word': word, 'count': count}
        for word, count in word_mistake_counts.most_common(10)
    ]
    
    # Get top 10 most mistaken letters
    most_mistaken_letters = [
        {'letter': letter, 'count': count}
        for letter, count in letter_mistake_counts.most_common(10)
    ]
    
    # Get top 10 most wrongly typed letters
    most_wrong_typed = [
        {'letter': letter, 'count': count}
        for letter, count in wrong_typed_counts.most_common(10)
    ]
    
    # Get top 10 common mistakes
    common_mistakes_list = [
        {'expected': exp, 'typed': typed, 'count': count}
        for (exp, typed), count in common_mistakes.most_common(10)
    ]
    
    # Add mistake details to each test
    for test in tests:
        test.mistake_count = len(test.mistakes)
        test.word_count = len(test.text.split())
    
    # Create paginator
    paginator = Paginator(tests, 5)  # Show 5 tests per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tests': page_obj,
        'total_tests': total_tests,
        'total_mistakes': total_mistakes,
        'most_mistaken_words': most_mistaken_words,
        'most_mistaken_letters': most_mistaken_letters,
        'most_wrong_typed': most_wrong_typed,
        'common_mistakes': common_mistakes_list,
    }
    
    return render(request, 'speed_test/mistakes.html', context)

def delete_result(request, result_id):
    if request.method == 'POST':
        TypingTest.objects.filter(id=result_id).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

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
