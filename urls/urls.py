from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django.contrib import admin
from django.urls import (
    path,
    include,
)
from django.conf import settings

from rest_framework.routers import DefaultRouter

from apps.auths.views import CustomUserViewSet
from apps.subjectss.views import (
    GeneralSubjectViewSet,
    TrackWayViewSet,
    ClassViewSet,
    ClassSubjectViewSet,
    TopicViewSet,
)
from apps.chats.views import PersonalChatViewSet
from apps.tests.views import (
    QuizTypeViewSet,
)
from apps.chats import consumers


websocket_urlpatterns = [
    path('ws/chats/<int:chat_id>/', consumers.ChatConsumer.as_asgi()),
]

urlpatterns = [
    path(settings.ADMIN_SITE_URL, admin.site.urls),
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),


    # MVC routes
    # path(
    #     '',
    #     include('chats.urls')
    # )
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

# ------------------------------------------
# API Endpoints
#
router: DefaultRouter = DefaultRouter(trailing_slash=False)

router.register('auths/users', CustomUserViewSet)
router.register('subjects/general_subjects', GeneralSubjectViewSet)
router.register('subjects/trackways', TrackWayViewSet)
router.register('subjects/classes', ClassViewSet)
router.register('subjects/class_subjects', ClassSubjectViewSet)
router.register('subjects/topics', TopicViewSet)
router.register('chats/chats', PersonalChatViewSet)
router.register('tests/quiz_types', QuizTypeViewSet)

urlpatterns += [
    path(
        "api/v1/",
        include(router.urls)
    ),
]
