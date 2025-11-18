from rest_framework.routers import DefaultRouter
from .views import PollViewSet, ChoiceViewSet

router = DefaultRouter()
router.register(r'polls', PollViewSet)
router.register(r'choices', ChoiceViewSet)

urlpatterns = router.urls
