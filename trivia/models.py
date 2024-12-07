from django.db import models

class TriviaQuestion(models.Model):
    question = models.TextField()
    options = models.JSONField()
    correct_answer = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.question[:50]}..." 