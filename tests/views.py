from django.shortcuts import render, redirect
from . import models
# Create your views here.



import random


from django.db.models import Q

def fetch_questions(user, subject, difficulty, question_type, prev_include, test_type):
    subject_id = subject.subject_id
    


    user_attempts_id = models.UserAttempt.objects.filter(user_id = user).values_list('question_id', flat=True)

    user_correct_attempts_id = models.UserAttempt.objects.filter(user_id = user, correctly_answered = True).values_list('question_id', flat=True)
    
    query = Q(subject_id = subject_id)
    query &= Q(question_difficulty__in = difficulty)
    query &= Q(question_type__in = question_type)

    if not prev_include:
        query &= ~Q(question_id__in = user_attempts_id)
    else:
        query &= ~Q(question_id__in = user_correct_attempts_id)
    
    question_list = models.Question.objects.filter(query).order_by('?')
    

    try:

        if test_type == 'small':
            question_list = question_list[:15]
        elif test_type == 'medium':
            question_list = question_list[:30]
        else:
            question_list = question_list[:65]

    except:
        print("sorry questions are less")
    
    finally:
        return question_list

def fetch_answers(question_list):
    query = Q(question_id__in = question_list)

    answer_list = models.Answer.objects.filter(query).order_by('?')
    return answer_list


def test_selection(request):


    branch = request.user.userinfo.branch
    subjects = models.Subject.objects.filter(branch_id__branch_code = branch)
    context = {'Subjects':subjects}

    return render(request, 'tests/selectionpage.html', context)




from django.core.serializers import serialize
def test(request):

    user = request.user

    context = request.session.get('context', {})

    if request.method == "POST":

        # for key, value in request.POST.items():
        #     print(key, value)


        
        subject_name = request.POST.get('subject_name')
        print(subject_name)
        subject = models.Subject.objects.get(subject_name = subject_name)
        question_difficulties = request.POST.getlist('difficulty')
        question_types = request.POST.getlist('question_type')
        print(question_types)

        prev = 'prev_include' in request.POST
        if prev:
            prev_include = True
        else:
            prev_include = False

        test_type = request.POST.get('test_type')

        # Set default difficulty if none is selected
        if not question_difficulties:
            question_difficulties = ['easy','medium']

        # Set default question type if none is selected
        if not question_types:
            question_types = ['mcq', 'msq', 'nat']

        # Set default test type if none is selected
        if not test_type:
            test_type = 'medium'

        question_list = fetch_questions(user=user,
                                        subject=subject,
                                        difficulty=question_difficulties,
                                        question_type=question_types,
                                        prev_include=prev_include,
                                        test_type=test_type)
        
        answer_list = fetch_answers(question_list=question_list)
        if test_type == "medium":
            seconds=3600
        elif test_type == "easy":
            seconds=1800
        else:
            seconds=10800
        context = {'question_list':question_list, 'answer_list':answer_list, 'seconds':seconds}
        # print(context)
        # return redirect('tests:instructions')
        return render(request,'tests/test.html', context=context)
        
    
    return render(request,'tests/test.html', context=context)

    


def instructions(request):
    return render(request, 'tests/instructions.html', {})

def save_user_answer(user, question, is_correct):
    user_answer, created = models.UserAttempt.objects.get_or_create(
        user_id = user,
        question_id = question,
        defaults={'correctly_answered':is_correct}
        )
    if not created:
        user_answer.correctly_answered = is_correct
        user_answer.save()

from django.http import HttpResponse
def result(request):
    if request.method == "POST":
        correct_answer_list = []
        incorrect_answer_list = []

        for key , value in request.POST.items():
            if key.startswith('q_'):

                ques_id = int(key.split('_')[1]) 
                ans_id = int(value)

                # Get correct answer for the ques_id from database
                correct_ans = models.Answer.objects.get(question_id = ques_id, is_correct = True)

                # Check if submitted answer correct
                question = models.Question.objects.get(question_id = ques_id)
                given_ans = models.Answer.objects.get(answer_id=ans_id)
                is_correct =  ans_id == correct_ans.answer_id
                if is_correct:
                    correct_answer_list.append((question, correct_ans))
                else:
                    incorrect_answer_list.append((question, correct_ans,given_ans, ans_id))
                
                no_of_correct_ans = len(correct_answer_list)
                print('printing correct ans:',no_of_correct_ans)
                no_of_incorrect_ans = len(incorrect_answer_list)
                total_attempted = no_of_correct_ans + no_of_incorrect_ans
                # figures = [0,0,0]
                figures = [no_of_correct_ans, no_of_incorrect_ans, total_attempted]
                user = request.user
                save_user_answer(user,question, is_correct)

        try:
            context_dict = {'c_ans_list':correct_answer_list, 'ic_ans_list':incorrect_answer_list,'figures':figures}
        except:
            return HttpResponse('No questions attempted')
        
        # print(context_dict)
        return render(request, 'tests/result.html', context_dict)

    else:
        return redirect('tests:testhome')
    

def revise(request):
    user = request.user

    

    revision_questions = models.UserAttempt.objects.filter(user_id=user, correctly_answered=False).select_related('question_id')

    answerslist = models.Answer.objects.filter(Q(question_id__in=revision_questions.values_list('question_id__question_id', flat=True)))

    if len(revision_questions) == 0:
        # return HttpResponse("Great! You have attempted all the questions right")
        no_questions = True
        return render(request, 'tests/revise.html',{'username':user, 'noquest':no_questions})


    

    # print(user)
    # print(revision_questions, answerslist)
    return render(request, 'tests/revise.html',{'username':user,
                                                  'question_list':revision_questions,
                                                  'answer_list':answerslist})