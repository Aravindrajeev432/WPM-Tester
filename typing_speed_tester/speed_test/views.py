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
    # Get all typing tests with mistakes
    all_tests = TypingTest.objects.exclude(mistakes=[]).order_by('-created_at')
    
    # Aggregate mistake statistics
    letter_mistakes = Counter()  # expected -> typed
    mistaken_letters = Counter()  # most mistaken letters
    wrong_typed_letters = Counter()  # most wrongly typed letters
    word_mistakes = Counter()  # most mistaken words
    
    for test in all_tests:
        test.word_count = len(test.text.split())
        test.mistake_count = len(test.mistakes)
        
        # Process mistakes for statistics
        for mistake in test.mistakes:
            # Track letter mistakes
            key = f"{mistake['expected']}|{mistake['typed']}"
            letter_mistakes[key] += 1
            
            # Track individual letter statistics
            mistaken_letters[mistake['expected']] += 1
            wrong_typed_letters[mistake['typed']] += 1
        
        # Process word mistakes
        for word_mistake in test.word_mistakes:
            word = word_mistake.get('word', '')
            if word:
                word_mistakes[word] += 1
    
    # Create paginator
    paginator = Paginator(all_tests, 5)  # Show 5 tests per page
    page_number = request.GET.get('page', 1)
    tests = paginator.get_page(page_number)
    
    # Get top 10 for each category
    common_mistakes = [
        {'expected': k.split('|')[0], 'typed': k.split('|')[1], 'count': v}
        for k, v in letter_mistakes.most_common(10)
    ]
    
    context = {
        'tests': tests,
        'common_mistakes': common_mistakes,
        'total_mistakes': sum(test.mistake_count for test in all_tests),
        'total_tests': all_tests.count(),
        'most_mistaken_words': [
            {'word': word, 'count': count}
            for word, count in word_mistakes.most_common(10)
        ],
        'most_mistaken_letters': [
            {'letter': letter, 'count': count}
            for letter, count in mistaken_letters.most_common(10)
        ],
        'most_wrong_typed': [
            {'letter': letter, 'count': count}
            for letter, count in wrong_typed_letters.most_common(10)
        ]
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
