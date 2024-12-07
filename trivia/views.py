import os
import json
import replicate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TriviaRequestSerializer, TriviaQuestionSerializer

class GenerateTrivia(APIView):
    def post(self, request):
        serializer = TriviaRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        subject = serializer.validated_data['subject']
        difficulty = serializer.validated_data['difficulty']
        num_questions = serializer.validated_data['num_questions']

        prompt = f"""Generate {num_questions} multiple choice {difficulty} difficulty trivia questions about {subject}. 
        Format the response as a JSON array with each question object having the following structure:
        {{
            "question": "the question text",
            "options": ["option1", "option2", "option3", "option4"],
            "correct_answer": "the correct option"
        }}
        Only return the JSON array, no additional text."""

        try:
            output = replicate.run(
                "google-deepmind/gemma-2b-it:dff94eaf770e1fc211e425a50b51baa8e4cac6c39ef074681f9e39d778773626",
                input={"prompt": prompt}
            )
            
            # Combine the streaming output into a single string
            response_text = "".join(output)
            
            # Parse the JSON response
            questions = json.loads(response_text)
            
            return Response(questions, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Failed to generate questions: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 