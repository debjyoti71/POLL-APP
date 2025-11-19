from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from polls.models import Poll, Choice, VoteRecord, User
from .serializers import PollSerializer, ChoiceSerializer
from .permissions import IsSuperAdminAuthenticated

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.select_related('owner').prefetch_related('choices').order_by('-created_at')
    serializer_class = PollSerializer
    permission_classes = [IsSuperAdminAuthenticated]

    def perform_create(self, serializer):
        # Get user from session for custom auth
        user_id = self.request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                serializer.save(owner=user)
            except User.DoesNotExist:
                serializer.save(owner=None)
        else:
            serializer.save(owner=None)

        
    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        poll = self.get_object()
        choice_id = request.data.get("choice_id")
        
        if not choice_id:
            return Response({"error": "choice_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            choice = Choice.objects.get(id=choice_id, poll=poll)
        except Choice.DoesNotExist:
            return Response({"error": "Choice not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get user from session for custom auth
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user already voted
        if VoteRecord.objects.filter(user=user, poll=poll).exists():
            return Response({"error": "You have already voted on this poll"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Record vote
        VoteRecord.objects.create(user=user, poll=poll)
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
    permission_classes = [IsSuperAdminAuthenticated]

