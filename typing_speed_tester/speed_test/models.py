from django.db import models

# Create your models here.

class TypingTest(models.Model):
    text = models.TextField()
    wpm = models.IntegerField()
    accuracy = models.FloatField()
    time_taken = models.FloatField()  # in seconds
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test {self.id} - WPM: {self.wpm}, Accuracy: {self.accuracy}%"

class CustomWord(models.Model):
    word = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word
