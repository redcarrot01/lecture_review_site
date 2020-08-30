from django import forms
from .models import Question, Choice
from django.utils import timezone

class NewQuestionForm(forms.Form):
    question_text = forms.CharField(label='질문 제목', max_length=100)


class ChoiceForm(forms.Form):
    question = forms.ModelChoiceField(queryset=Question.objects.all())
    choice_text = forms.CharField(label='text', max_length=30)
    votes = forms.IntegerField()

class QuestionChoiceForm(forms.ModelForm):
    model = Question
    question_text = forms.CharField(required=True)

    class Meta:
        model = Question
        fields = ['question_text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(type(args[0]))
        for i in range(len(args)):
            print(args[i])


    def clean(self):
        choices = set()
        i = 0
        field_name = 'choice_text_%s' % (i,)
        while self.cleaned_data.get(field_name):
            choice_text = self.cleaned_data[field_name]
            if choice_text in choices:
                self.add_error(field_name, 'Duplicate')
            else:
                choices.add(choice_text)
            i += 1
            field_name = 'choice_text_%s' % (i,)
        self.cleaned_data['choices'] = choices

    def save(self):
        question = Question(question_text=self.cleaned_data['question_text'], pub_date=timezone.now(), deadline_date=timezone.now(),)
        question.save()
        question.choice_set.all().delete()
        print(self.cleaned_data['choices'])
        for choice in self.cleaned_data['choices']:
            Choice.objects.create(
                question = question,
                choice_text=choice,
            )
        return question