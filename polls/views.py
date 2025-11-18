from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Choice
from .forms import PollForm, ChoiceFormSet

def home(request):
    return render(request, 'polls/home.html')

def poll_list(request):
    polls = Poll.objects.all().order_by('-created_at')
    return render(request, 'polls/poll_list.html', {'polls': polls})

def poll_detail(request, slug):
    poll = get_object_or_404(Poll, slug=slug)
    return render(request, 'polls/poll_detail.html', {'poll': poll})

def create_poll(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        formset = ChoiceFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            poll = form.save()
            formset.instance = poll
            formset.save()
            return redirect('poll_detail', slug=poll.slug)
    
    else:
        form = PollForm()
        formset = ChoiceFormSet()

    return render(request, 'polls/create_poll.html', {
        'form': form,
        'formset': formset
    })    


def vote(request, pk):
    choice = Choice.objects.get(pk=pk)
    choice.votes += 1
    choice.save()
    return redirect('poll_list')
    