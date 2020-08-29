from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.utils import timezone

from .models import Question, Choice
from django.views import generic
from .forms import NewQuestionForm, QuestionChoiceForm


# Create your views here.
class review_list(generic.ListView):
    template_name = 'review/review_list.html'
    context_object_name = 'review_lists'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class review_detail(generic.DeleteView):
    model = Question
    context_object_name = 'review'
    template_name = 'review/review_detail.html'


class review_result(generic.DeleteView):
    model = Question
    template_name = 'review/review_result.html'


def review_new(request):

    if request.method == 'POST':
        form = QuestionChoiceForm(request.POST)
        if form.is_valid():
            review = form.save()
            print(review)
            # post.author = User.objects.get(username=request.user)
            # review.published_date = timezone.now()
            # post.save()
            return redirect('review_detail', pk=review.pk)
    else:
        # 등록 Form을 보여준다
        form = NewQuestionForm()
    return render(request, 'review/review_new.html', {'form': form})


def review_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'review/review_detail.html', \
                      {'question': question,
                       'error_message': "You didn't select a choice."
                       })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('review_result', args=(question.id,)))
