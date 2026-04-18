from collections import Counter
import json
import random

FINGER_MAP = {
    '1': 'Left Pinky', 'q': 'Left Pinky', 'a': 'Left Pinky', 'z': 'Left Pinky', '!': 'Left Pinky', 'Q': 'Left Pinky', 'A': 'Left Pinky', 'Z': 'Left Pinky', '`': 'Left Pinky', '~': 'Left Pinky',
    '2': 'Left Ring', 'w': 'Left Ring', 's': 'Left Ring', 'x': 'Left Ring', '@': 'Left Ring', 'W': 'Left Ring', 'S': 'Left Ring', 'X': 'Left Ring',
    '3': 'Left Middle', 'e': 'Left Middle', 'd': 'Left Middle', 'c': 'Left Middle', '#': 'Left Middle', 'E': 'Left Middle', 'D': 'Left Middle', 'C': 'Left Middle',
    '4': 'Left Index', 'r': 'Left Index', 'f': 'Left Index', 'v': 'Left Index', '$': 'Left Index', 'R': 'Left Index', 'F': 'Left Index', 'V': 'Left Index',
    '5': 'Left Index', 't': 'Left Index', 'g': 'Left Index', 'b': 'Left Index', '%': 'Left Index', 'T': 'Left Index', 'G': 'Left Index', 'B': 'Left Index',
    ' ': 'Thumbs',
    '6': 'Right Index', 'y': 'Right Index', 'h': 'Right Index', 'n': 'Right Index', '^': 'Right Index', 'Y': 'Right Index', 'H': 'Right Index', 'N': 'Right Index',
    '7': 'Right Index', 'u': 'Right Index', 'j': 'Right Index', 'm': 'Right Index', '&': 'Right Index', 'U': 'Right Index', 'J': 'Right Index', 'M': 'Right Index',
    '8': 'Right Middle', 'i': 'Right Middle', 'k': 'Right Middle', ',': 'Right Middle', '*': 'Right Middle', 'I': 'Right Middle', 'K': 'Right Middle', '<': 'Right Middle',
    '9': 'Right Ring', 'o': 'Right Ring', 'l': 'Right Ring', '.': 'Right Ring', '(': 'Right Ring', 'O': 'Right Ring', 'L': 'Right Ring', '>': 'Right Ring',
    '0': 'Right Pinky', 'p': 'Right Pinky', ';': 'Right Pinky', '/': 'Right Pinky', ')': 'Right Pinky', 'P': 'Right Pinky', ':': 'Right Pinky', '?': 'Right Pinky',
    '-': 'Right Pinky', '_': 'Right Pinky', '=': 'Right Pinky', '+': 'Right Pinky', '[': 'Right Pinky', '{': 'Right Pinky', ']': 'Right Pinky', '}': 'Right Pinky',
    '\\': 'Right Pinky', '|': 'Right Pinky', '\'': 'Right Pinky', '"': 'Right Pinky',
}

from django.core.paginator import Paginator
from django.db.models import Count, Min, Max
from django.db.models.functions import Length
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .models import CustomWord, TypingTest

def home(request):
    words_count = CustomWord.objects.count()
    if words_count > 0:
        agg = CustomWord.objects.annotate(word_len=Length('word')).aggregate(
            min_len=Min('word_len'),
            max_len=Max('word_len')
        )
        min_length = agg['min_len'] or 3
        max_length = agg['max_len'] or 25
    else:
        min_length = 3
        max_length = 25
        
    return render(request, 'speed_test/home.html', {
        'words_count': words_count,
        'min_length': min_length,
        'max_length': max_length
    })

def get_text(request):
    words = list(CustomWord.objects.values_list('word', flat=True))
    max_length = request.GET.get('max_length')
    
    if max_length and max_length.isdigit():
        max_len = int(max_length)
        words = [w for w in words if len(w) <= max_len]

    if not words:
        return JsonResponse({
            'text': '',
            'error': 'No words available. Please add some words or increase max word length.'
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
            # Only save if there are mistakes
            if not mistakes:
                return JsonResponse({'status': 'success', 'id': None})
            
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
    
    total_wpm = 0
    max_wpm = 0
    total_time = 0
    total_accuracy = 0
    test_count = len(all_results)
    
    typed_words = Counter()
    mistaken_words = Counter()
    
    # Process stats and word counts
    for result in all_results:
        total_wpm += result.wpm
        if result.wpm > max_wpm:
            max_wpm = result.wpm
        total_time += result.time_taken
        total_accuracy += result.accuracy
        
        words = result.text.split()
        result.word_count = len(words)
        result.mistake_count = len(result.mistakes)
        
        for w in words:
            typed_words[w] += 1
            
        for wm in result.word_mistakes:
            mistaken_words[wm['word']] += 1
            
    avg_wpm = total_wpm / test_count if test_count > 0 else 0
    avg_accuracy = total_accuracy / test_count if test_count > 0 else 0
    
    active_words = set(CustomWord.objects.values_list('word', flat=True))
    
    # Easiest words: Typed frequently with highest success rate
    easiest_words_list = []
    for word, count in typed_words.items():
        if count >= 1 and word in active_words:
            mistakes = mistaken_words.get(word, 0)
            success_rate = (count - mistakes) / count
            easiest_words_list.append({
                'word': word, 
                'success_rate': success_rate * 100,
                'typed': count, 
                'mistakes': mistakes
            })
            
    # Sort by success rate (desc), then total typed (desc)
    easiest_words_list.sort(key=lambda x: (x['success_rate'], x['typed']), reverse=True)
    top_5_easiest = easiest_words_list[:5]
    
    # Create paginator
    paginator = Paginator(all_results, 5)  # Show 5 results per page
    page_number = request.GET.get('page', 1)
    results = paginator.get_page(page_number)
    
    context = {
        'results': results,
        'avg_wpm': round(avg_wpm),
        'max_wpm': max_wpm,
        'avg_accuracy': round(avg_accuracy, 1),
        'total_time': round(total_time / 60, 1),
        'top_easiest': top_5_easiest,
        'total_tests': test_count
    }
    
    return render(request, 'speed_test/results.html', context)

def view_mistakes(request):
    # Get all tests with mistakes ordered by most recent first
    tests = TypingTest.objects.exclude(mistakes=[]).order_by('-created_at')
    
    # Calculate total tests and mistakes
    total_tests_all = TypingTest.objects.count()
    total_tests = tests.count()
    total_mistakes = sum(len(test.mistakes) for test in tests)
    avg_mistakes = total_mistakes / total_tests_all if total_tests_all > 0 else 0
    
    # Process word-level mistakes
    word_mistake_counts = Counter()
    letter_mistake_counts = Counter()
    wrong_typed_counts = Counter()
    common_mistakes = Counter()
    finger_mistake_counts = Counter()
    
    for test in tests:
        # Process word mistakes
        for mistake in test.word_mistakes:
            word_mistake_counts[mistake['word']] += 1
        
        # Process character mistakes
        for mistake in test.mistakes:
            expected = mistake['expected']
            letter_mistake_counts[expected] += 1
            wrong_typed_counts[mistake['typed']] += 1
            mistake_key = (expected, mistake['typed'])
            common_mistakes[mistake_key] += 1
            
            finger = FINGER_MAP.get(expected, 'Unknown')
            finger_mistake_counts[finger] += 1
    
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
    
    finger_mistakes = [
        {'finger': finger, 'count': count}
        for finger, count in finger_mistake_counts.most_common()
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
        'total_tests': total_tests_all,
        'total_mistakes': total_mistakes,
        'avg_mistakes': round(avg_mistakes, 1),
        'most_mistaken_words': most_mistaken_words,
        'finger_mistakes': finger_mistakes,
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

def custom_test(request):
    return render(request, 'speed_test/custom_test.html')

def get_custom_text(request):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            # Split text into words and remove empty strings
            words = [word for word in text.split() if word]
            # Randomize the word order
            random.shuffle(words)
            # Join words back with spaces
            shuffled_text = ' '.join(words)
            return JsonResponse({'text': shuffled_text})
    return JsonResponse({'error': 'No text provided'}, status=400)
