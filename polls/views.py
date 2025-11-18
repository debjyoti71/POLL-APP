from .models import Poll

def poll_list(request):
    polls = Poll.objects.all().order_by('-created_at')
    return render(request, 'polls/poll_list.html', {'polls': polls})

def poll_detail(request, slug):
    poll = Poll.objects.get(slug=slug)
    return render(request, 'polls/poll_detail.html', {'poll': poll})