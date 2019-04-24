import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from polls.forms import PollForm, CommentForm, ChangePasswordForm, PollModelForm, QuestionForm, ChoiceModelForm
from polls.models import Poll, Question, Answer, Comment, Choice


def my_login(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password!'

    next_url = request.POST.get('next')
    if next_url:
        context['next_url'] = next_url

    return render(request, template_name='polls/login.html', context=context)


def my_logout(request):
    logout(request)
    return redirect('login')


# Create your views here.
def index(request):
    poll_list = Poll.objects.annotate(question_count=Count('question'))

    #print(request.user.email)
    context = {
        'poll_head': 'My Poll',
        'poll_list': poll_list,
    }
    return render(request, template_name='polls/index.html', context=context)


@login_required
@permission_required('polls.view_question')
def detail(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == "POST":
        for question in poll.question_set.all():
            name = "choice" + str(question.id)
            choice_id = request.POST.get(name)

            if choice_id:
                try:
                    ans = Answer.objects.get(question_id=question.id)
                    ans.choice_id = choice_id
                    ans.question_id = question.id
                    ans.save()
                except Answer.DoesNotExist:
                    Answer.objects.create(
                        choice_id=choice_id,
                        question_id=question.id
                    )

            print(choice_id)

    print(request.GET)
    print(request.POST)
    # context1 = {
    # 'poll_index': poll_list[poll_id-1]
    # }*/
    return render(request, 'polls/detail.html', {'poll': poll})


@login_required
@permission_required('polls.add_poll')
def create(request):
    context = {}
    QuestionFormSet = formset_factory(QuestionForm, extra=2)
    if request.method == 'POST':
        form = PollModelForm(request.POST)
        formset = QuestionFormSet(request.POST)

        if form.is_valid():
            poll = form.save()
            if formset.is_valid():
                for question_form in formset:
                    Question.objects.create(
                        text=question_form.cleaned_data.get("text"),
                        type=question_form.cleaned_data.get("type"),
                        poll=poll
                    )
                context['success'] = "Poll %s is created successfully" % poll.title

    else:
        form = PollModelForm()
        formset = QuestionFormSet()

    context['form'] = form
    context['formset'] = formset
    return render(request, 'polls/create.html', context=context)


@login_required
@permission_required('polls.change_poll')
def update(request, poll_id):

    poll = Poll.objects.get(id=poll_id)
    QuestionFormSet = formset_factory(QuestionForm, extra=2, max_num=10)

    if request.method == 'POST':
        form = PollModelForm(request.POST, instance=poll)
        formset = QuestionFormSet(request.POST)
        if form.is_valid():
            form.save()
            if formset.is_valid():
                for question_form in formset:
                    # has question_id -> update
                    if question_form.cleaned_data.get('question_id'):
                        question = Question.objects.get(id=question_form.cleaned_data.get('question_id'))
                        if question:
                            question.text = question_form.cleaned_data.get('text')
                            question.type = question_form.cleaned_data.get('type')
                            question.save()
                    # No question_id -> create a new question
                    else:
                        if question_form.cleaned_data.get('text'):
                            Question.objects.create(
                                text=question_form.cleaned_data.get('text'),
                                type=question_form.cleaned_data.get('type'),
                                poll=poll
                            )
    else:
        form = PollModelForm(instance=poll)

        data = []
        for question in poll.question_set.all():
            data.append(
                {
                    'text': question.text,
                    'type': question.type,
                    'question_id': question.id
                }
            )
        print(data)

        formset = QuestionFormSet(initial=data)

    context = {"form": form, 'formset': formset, 'poll_obj': poll}

    return render(request, 'polls/update.html', context=context)


@login_required
@permission_required('polls.change_poll')
def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    return redirect('update_poll', poll_id=question.poll.id)


@login_required
@permission_required('polls.change_poll')
def add_choice(request, question_id):
    question = Question.objects.get(id=question_id)

    context = {'question': question}

    return render(request, 'choices/add.html', context=context)


@csrf_exempt
def add_choice_api(request, question_id):
    if request.method == 'POST':
        choice_list = json.loads(request.body)
        error_list = []

        for choice in choice_list:
            data = {
                'text': choice['text'],
                'value': choice['value'],
                'question': question_id
            }
            form = ChoiceModelForm(data)
            if form.is_valid():
                form.save()
            else:
                error_list.append(form.errors.as_text())
        if len(error_list) == 0:
            return JsonResponse({'message': 'success', 'no_choice': 2}, status=200)
        else:
            print(error_list)
            return JsonResponse({'message': error_list}, status=400)

    return JsonResponse({'message': 'This API does not accept GET request.'}, status=405)


def comment(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        print(poll.title)

        if form.is_valid():
            comment = Comment.objects.create(
                title=form.cleaned_data.get('title'),
                body=form.cleaned_data.get('body'),
                email=form.cleaned_data.get('email'),
                tel=form.cleaned_data.get('tel'),
                poll=poll
            )
    else:
        form = CommentForm()

    context = {
        "form": form,
        "comment_head": "New Comment",
        "poll": poll
    }
    return render(request, template_name='polls/comment.html', context=context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        old_pass = request.POST.get('old_pass')
        new_pass = request.POST.get('new_pass')
        confirm_pass = request.POST.get('confirm_pass')
        print(old_pass)
        print(new_pass)
        print(confirm_pass)

        print(request.user)
        print(request.user.password)
    else:
        form = ChangePasswordForm()

    context = {
        "form": form,
        'reset_title': 'เปลี่ยนรหัสผ่าน'
    }

    return render(request, template_name='polls/change_password.html', context=context)
