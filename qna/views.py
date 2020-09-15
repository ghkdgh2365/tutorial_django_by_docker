from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Answer

class IndexView(generic.ListView):
  template_name = 'qna/index.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    """return the last five published questions (not including those set to be published in the future)."""
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
  model = Question
  template_name = 'qna/detail.html'
  
  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
  model = Question
  template_name = 'qna/results.html'

def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_answer = question.answer_set.get(pk=request.POST['answer'])
  except (KeyError, Answer.DoesNotExist):
    # Redisplay the question voting form.
    return render(request, 'qna/detail.html', {
      'question': question,
      'error_message': "You're didn't select a answer.",
    })
  else:
    selected_answer.votes += 1
    selected_answer.save()
    # Always return an HttpResponseRedirect after successfully dealing with POST data.
    # this prevents data from being posted twice if a user hits the Back button.
    return HttpResponseRedirect(reverse('qna:results', args=(question.id,)))


# Create your views here.
