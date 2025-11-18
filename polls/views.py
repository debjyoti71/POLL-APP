from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Choice, VoteRecord
from .forms import PollForm, ChoiceFormSet
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'polls/home.html')

def poll_list(request):
    polls = Poll.objects.all().order_by('-created_at')
    return render(request, 'polls/poll_list.html', {'polls': polls})

def poll_detail(request, slug):
    poll = get_object_or_404(Poll, slug=slug)

    if not poll.is_public:
        code = request.GET.get("code")
        if code != str(poll.private_code):
            return render(request, "polls/private_blocked.html")

    return render(request, 'polls/poll_detail.html', {'poll': poll})


@login_required
def create_poll(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        formset = ChoiceFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            poll = form.save(commit=False)
            poll.owner = request.user    # assign poll creator
            poll.save()

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


@login_required
def vote(request, pk):
    choice = Choice.objects.get(pk=pk)
    poll = choice.poll

    # check if user already voted
    if VoteRecord.objects.filter(user=request.user, poll=poll).exists():
        return redirect('poll_detail', slug=poll.slug)

    # record first vote
    VoteRecord.objects.create(user=request.user, poll=poll)

    # increment actual vote
    choice.votes += 1
    choice.save()

    return redirect('poll_list')
