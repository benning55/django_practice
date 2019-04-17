from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect

from polls.forms import PollForm, CommentForm, ChangePasswordForm
from polls.models import Poll, Question, Answer, Comment


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
    if request.method == 'POST':
        form = PollForm(request.POST)

        if form.is_valid():
            poll = Poll.objects.create(
                title=form.cleaned_data.get('title'),
                start_date=form.cleaned_data.get('body'),
                end_date=form.cleaned_data.get('email')
            )

            for i in range(1, form.cleaned_data.get('no_questions') + 1):
                Question.objects.create(
                    text='QQQQ' + str(i),
                    type='01',
                    poll=poll
                )
    else:
        form = PollForm()

    context = {"form": form}
    return render(request, 'polls/create.html', context=context)


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
