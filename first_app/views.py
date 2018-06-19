from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Question, Choice
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import six 

# def index(request):
#     return HttpResponse("Hello, world. You're at the first_app index.")


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

class IndexView(generic.ListView):
    template_name = 'first_app/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'first_app/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'first_app/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'first_app/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('first_app:results', args=(question.id,)))

def hello_world(request):
    # print(request.GET)
    get_dict = dict(six.iterlists(request.GET))
    post_dict = dict(six.iterlists(request.POST))
    print(get_dict)
    print(post_dict)
    return render(request, 'first_app/helloworld.html', get_dict)