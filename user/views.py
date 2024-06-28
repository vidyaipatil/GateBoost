from django.shortcuts import render
from tests import models
from django.db.models import Q

# Create your views here.
def profile(request):
    
    user = request.user

    

    # attempted_questions = list(models.UserAttempt.objects.filter(user_id = user))
    attempted_questions_easy = list(models.UserAttempt.objects.filter(user_id = user, question_id__question_difficulty = 'easy'))
    attempted_questions_medium = list(models.UserAttempt.objects.filter(user_id = user, question_id__question_difficulty = 'medium'))
    attempted_questions_hard = list(models.UserAttempt.objects.filter(user_id = user, question_id__question_difficulty = 'hard'))
    

    question_figures = [0, 0, 0, 0]



    no_of_easy_questions = len(attempted_questions_easy)
    no_of_medium_questions = len(attempted_questions_medium)
    no_of_hard_questions = len(attempted_questions_hard) 
    total_no_of_questions = no_of_easy_questions + no_of_medium_questions + no_of_hard_questions

    question_figures = [total_no_of_questions ,no_of_easy_questions, no_of_medium_questions, no_of_hard_questions]

    context = {'user':user,
               'question_figures':question_figures}

    return render(request, 'user/profile.html', context)