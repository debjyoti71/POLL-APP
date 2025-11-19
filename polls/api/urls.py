from rest_framework.routers import DefaultRouter
from .views import PollViewSet, ChoiceViewSet

# API URL Examples:
# GET /api/polls/ - List all public polls
# POST /api/polls/ - Create new poll
# GET /api/polls/{id}/ - Get specific poll
# POST /api/polls/{id}/vote/ - Vote on poll (requires choice_id in body)
# GET /api/choices/ - List all choices
# POST /api/choices/ - Create new choice

router = DefaultRouter()
router.register(r'polls', PollViewSet)
router.register(r'choices', ChoiceViewSet)

urlpatterns = router.urls
