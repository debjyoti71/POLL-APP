from rest_framework import serializers
from polls.models import Poll, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'votes']

class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField()

    class Meta:
        model = Poll
        fields = [
            'id', 'question', 'is_public', 
            'created_at', 'slug', 'private_code', 
            'owner', 'choices'
        ]
