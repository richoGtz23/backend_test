from django.urls import path, include
from rest_framework import routers

from backend_test.views.numToEnglish import num_to_english_view
from backend_test.views.User import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'num_to_english', num_to_english_view)
]
