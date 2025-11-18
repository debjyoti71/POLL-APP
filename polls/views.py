from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404
from .models import Poll, Choice, VoteRecord
from .forms import PollForm, ChoiceFormSet
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'polls/home.html')

def poll_list(request):
    polls = Poll.objects.select_related('owner').prefetch_related('choices').filter(is_public=True).order_by('-created_at')
    return render(request, 'polls/poll_list.html', {'polls': polls})

def poll_detail(request, slug):
    poll = get_object_or_404(Poll, slug=slug)

    if not poll.is_public:
        # Allow owner to always see their poll
        if request.user.is_authenticated and poll.owner == request.user:
            pass  # Owner can always access
        else:
            code = request.GET.get("code")
            if code != str(poll.private_code):
                return render(request, "polls/private_blocked.html")

    # Check if user already voted
    user_voted = False
    if request.user.is_authenticated:
        user_voted = VoteRecord.objects.filter(user=request.user, poll=poll).exists()

    return render(request, 'polls/poll_detail.html', {
        'poll': poll,
        'user_voted': user_voted
    })


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
def my_polls(request):
    polls = Poll.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'polls/my_polls.html', {'polls': polls})


@login_required
def vote(request, pk):
    try:
        choice = get_object_or_404(Choice, pk=pk)
        poll = choice.poll

        # check if user already voted
        if VoteRecord.objects.filter(user=request.user, poll=poll).exists():
            messages.warning(request, 'You have already voted on this poll.')
            return redirect('poll_detail', slug=poll.slug)

        # record first vote
        VoteRecord.objects.create(user=request.user, poll=poll)

        # increment actual vote
        choice.votes += 1
        choice.save()

        messages.success(request, 'Your vote has been recorded!')
        return redirect('poll_detail', slug=poll.slug)
    except Exception as e:
        messages.error(request, 'An error occurred while voting.')
        return redirect('poll_list')
