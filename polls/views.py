from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404
from functools import wraps
from .models import Poll, Choice, VoteRecord, User
from .forms import PollForm, ChoiceFormSet

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        print(f"DEBUG: login_required check - session user_id: {user_id}")
        if not user_id:
            messages.error(request, 'Please log in to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def get_current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass
    return None

def home(request):
    return render(request, 'polls/home.html')

def poll_list(request):
    polls = Poll.objects.select_related('owner').prefetch_related('choices').filter(is_public=True).order_by('-created_at')
    return render(request, 'polls/poll_list.html', {'polls': polls})

def poll_detail(request, slug):
    poll = get_object_or_404(Poll, slug=slug)

    if not poll.is_public:
        # Allow owner to always see their poll
        current_user = get_current_user(request)
        if current_user and poll.owner == current_user:
            pass  # Owner can always access
        else:
            code = request.GET.get("code")
            if code != str(poll.private_code):
                return render(request, "polls/private_blocked.html")

    # Check if user already voted
    user_voted = False
    current_user = get_current_user(request)
    if current_user:
        user_voted = VoteRecord.objects.filter(user=current_user, poll=poll).exists()

    return render(request, 'polls/poll_detail.html', {
        'poll': poll,
        'user_voted': user_voted,
        'current_user': current_user
    })


@login_required
def create_poll(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        formset = ChoiceFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            poll = form.save(commit=False)
            poll.owner = get_current_user(request)    # assign poll creator
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
    current_user = get_current_user(request)
    polls = Poll.objects.filter(owner=current_user).order_by('-created_at')
    return render(request, 'polls/my_polls.html', {'polls': polls})


@login_required
def vote(request, pk):
    try:
        choice = get_object_or_404(Choice, pk=pk)
        poll = choice.poll

        # check if user already voted
        current_user = get_current_user(request)
        if VoteRecord.objects.filter(user=current_user, poll=poll).exists():
            messages.warning(request, 'You have already voted on this poll.')
            return redirect('poll_detail', slug=poll.slug)

        # record first vote
        VoteRecord.objects.create(user=current_user, poll=poll)

        # increment actual vote
        choice.votes += 1
        choice.save()

        messages.success(request, 'Your vote has been recorded!')
        return redirect('poll_detail', slug=poll.slug)
    except Exception as e:
        messages.error(request, 'An error occurred while voting.')
        return redirect('poll_list')


