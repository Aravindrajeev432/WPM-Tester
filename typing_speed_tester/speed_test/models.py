from django.db import models

# Create your models here.

class TypingTest(models.Model):
    text = models.TextField()
    wpm = models.IntegerField()
    accuracy = models.FloatField()
    time_taken = models.FloatField()  # in seconds
    created_at = models.DateTimeField(auto_now_add=True)
    mistakes = models.JSONField(default=list)  # Store mistakes as [{"expected": "x", "typed": "y", "position": 0}]
    word_mistakes = models.JSONField(default=list)  # Store word-level mistakes

    def __str__(self):
        return f"Test {self.id} - WPM: {self.wpm}, Accuracy: {self.accuracy}%"

    def get_word_at_position(self, position):
        """Get the word containing the character at the given position"""
        words = self.text.split()
        current_pos = 0
        
        for word in words:
            word_length = len(word)
            if current_pos <= position < current_pos + word_length:
                return word
            current_pos += word_length + 1  # +1 for space
        return None

class CustomWord(models.Model):
    word = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word
