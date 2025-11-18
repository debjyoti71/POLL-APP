from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from polls.models import Poll, Choice, VoteRecord
from .serializers import PollSerializer, ChoiceSerializer

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.select_related('owner').prefetch_related('choices').filter(is_public=True).order_by('-created_at')
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

        
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def vote(self, request, pk=None):
        poll = self.get_object()
        choice_id = request.data.get("choice_id")
        
        if not choice_id:
            return Response({"error": "choice_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            choice = Choice.objects.get(id=choice_id, poll=poll)
        except Choice.DoesNotExist:
            return Response({"error": "Choice not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if user already voted
        if VoteRecord.objects.filter(user=request.user, poll=poll).exists():
            return Response({"error": "You have already voted on this poll"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Record vote
        VoteRecord.objects.create(user=request.user, poll=poll)
        choice.votes += 1
        choice.save()

        return Response({
            "message": "Vote recorded successfully",
            "choice": choice.text,
            "votes": choice.votes
        })

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

