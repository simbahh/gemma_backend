from rest_framework import views, status
from rest_framework.response import Response
from rest_framework import serializers
import replicate
import os
import re
import time
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

class QuizRequestSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=100)
    difficulty = serializers.CharField(max_length=20)
    num_questions = serializers.IntegerField(min_value=1, max_value=10, default=5)

class GenerateQuizView(views.APIView):
    def generate_questions_with_retry(self, prompt, max_retries=3, timeout=90):
        for attempt in range(max_retries):
            try:
                output = ""
                for event in replicate.stream(
                    "google-deepmind/gemma-2b-it:dff94eaf770e1fc211e425a50b51baa8e4cac6c39ef074681f9e39d778773626",
                    input={
                        "prompt": prompt,
                        "max_tokens": 4096,
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "timeout": timeout
                    }
                ):
                    output += str(event)
                return output
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(2)

    def parse_markdown_questions(self, text):
        questions = []
        question_blocks = re.split(r'\*\*Question \d+:\*\*|\d+\.\s+\*\*', text)
        question_blocks = [q.strip() for q in question_blocks if q.strip()]
        
        for block in question_blocks:
            try:
                question_text = block.split('\n')[0].strip()
                question_text = re.sub(r'\*\*|\*', '', question_text)
                
                options = []
                option_matches = re.findall(r'[a-d]\)(.*?)(?=(?:[a-d]\)|\n\n|$))', block, re.DOTALL)
                
                if len(option_matches) == 4:
                    for i, opt in enumerate(option_matches):
                        opt = opt.strip()
                        option_letter = chr(97 + i) + ')'
                        full_option = f"{option_letter} {opt}"
                        options.append(full_option)
                    
                    questions.append({
                        "question_text": question_text,
                        "options": options,
                        "correct_answer": options[0]
                    })
            except Exception:
                continue
                
        return questions

    def post(self, request):
        try:
            serializer = QuizRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            subject = serializer.validated_data['subject']
            difficulty = serializer.validated_data['difficulty']
            num_questions = serializer.validated_data['num_questions']

            prompt = f"""Generate exactly {num_questions} multiple choice questions about {subject} at {difficulty} difficulty level.
            
            STRICT FORMAT REQUIREMENTS:
            1. Number each question from 1 to {num_questions}
            2. Each question MUST have exactly 4 options labeled a) b) c) d)
            3. Use this exact format:

            **Question 1:**
            [Question text here]
            a) [Option 1]
            b) [Option 2]
            c) [Option 3]
            d) [Option 4]

            **Question 2:**
            [Continue pattern...]"""

            output = self.generate_questions_with_retry(prompt)

            if not output:
                return Response(
                    {'error': 'No response from AI service'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            questions = self.parse_markdown_questions(output)
            
            if not questions:
                return Response(
                    {'error': 'No valid questions could be parsed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(questions, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
def xai_chat(request):
    try:
        message = request.data.get('message')
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.XAI_API_KEY}"
        }
        
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "model": "grok-beta",
            "stream": False,
            "temperature": 0
        }
        
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        return Response(response.json())
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)