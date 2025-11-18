from django.shortcuts import render, get_object_or_404
from .models import Poll

def home(request):
    return render(request, 'polls/home.html')

def poll_list(request):
    polls = Poll.objects.all().order_by('-created_at')
    return render(request, 'polls/poll_list.html', {'polls': polls})

def poll_detail(request, slug):
    poll = get_object_or_404(Poll, slug=slug)
    return render(request, 'polls/poll_detail.html', {'poll': poll})