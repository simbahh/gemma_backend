from rest_framework import serializers
from .models import TriviaQuestion

class TriviaQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriviaQuestion
        fields = ['question', 'options', 'correct_answer']

class TriviaRequestSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=100)
    difficulty = serializers.ChoiceField(choices=['easy', 'medium', 'hard'])
    num_questions = serializers.IntegerField(min_value=1, max_value=20, default=10) 