from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from polls.models import Poll, Question


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

    # context1 = {
    # 'poll_index': poll_list[poll_id-1]
    # }*/
    return render(request, 'polls/detail.html', { 'poll':poll })
