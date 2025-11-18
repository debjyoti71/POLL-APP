from rest_framework import serializers
from polls.models import Poll, Choice
from django.contrib.auth.models import User

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'votes']

class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    private_code = serializers.UUIDField(read_only=True)

    class Meta:
        model = Poll
        fields = [
            'id', 'question', 'is_public', 
            'created_at', 'slug', 'private_code', 
            'owner', 'choices'
        ]
        read_only_fields = ['slug', 'created_at', 'owner']

    def validate_question(self):
        question = self.validated_data.get('question', '')
        if len(question.strip()) < 5:
            raise serializers.ValidationError('Question must be at least 5 characters long.')
        return question
