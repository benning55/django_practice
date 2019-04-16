from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from polls.models import Poll, Question, Answer


# Create your views here.
def index(request):
    poll_list = Poll.objects.annotate(question_count=Count('question'))

    print(poll_list.query)
    context = {
        'poll_head': 'My Poll',
        'poll_list': poll_list,
    }
    return render(request, template_name='polls/index.html', context=context)


def detail(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    for question in poll.question_set.all():
        name = "choice" + str(question.id)
        choice_id = request.GET.get(name)

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
    # context1 = {
    # 'poll_index': poll_list[poll_id-1]
    # }*/
    return render(request, 'polls/detail.html', {'poll': poll})
