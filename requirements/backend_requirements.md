# Project overview
Use this guide to build an ai powered quiz/trivia app were user enter a subject and difficult level to start quiz with 10 questions and given a score at the end.
App uses replicate -gemini model to generate questions and answers.

# Feature requirements
- We will django rest framework to build the backend and endpoints.
- Mainly one endpoint to generate the questions and answers takes 3 parameters: subject, difficult level, number of questions.
- Endpoint should return the questions and answers and correct answer for each question.


# Relevant docs
https://replicate.com/google-deepmind/gemma-2b-it/api
Set the REPLICATE_API_TOKEN environment variable

export REPLICATE_API_TOKEN=r8_duF**********************************

Visibility

Copy
Learn more about authentication

Install Replicate’s Python client library

pip install replicate

Copy
Learn more about setup
Run google-deepmind/gemma-2b-it using Replicate’s API. Check out the model's schema for an overview of inputs and outputs.

import replicate

input = {}

for event in replicate.stream(
    "google-deepmind/gemma-2b-it:dff94eaf770e1fc211e425a50b51baa8e4cac6c39ef074681f9e39d778773626",
    input=input
):
    print(event, end="")
    #=> "\n\n"



# Current File structure
gemma_2_trivia_backend/
├── .env
├── gemma_2_trivia_backend/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── quiz/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── requirements/
│   ├── backend_requirements.md
│   └── requirements.txt
├── .myenv
└── manage.py

#Rules
- All new endpoints should be added to the urls.py file.
- All keys should be stored in the .env file and loaded in the settings.py file.
- All new apps should be added to the INSTALLED_APPS in the settings.py file.

