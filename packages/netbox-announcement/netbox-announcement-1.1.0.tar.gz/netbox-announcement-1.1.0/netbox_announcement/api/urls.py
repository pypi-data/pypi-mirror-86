from rest_framework import routers
from .views import AnnouncementsRootView, AnnouncementViewSet, AnnouncementStatusViewSet, AnnouncementUpdateViewSet, AnnouncementEmailPreConfigViewSet


router = routers.DefaultRouter()
router.APIRootView = AnnouncementsRootView

router.register('announcments', AnnouncementViewSet)
router.register('status', AnnouncementStatusViewSet)
router.register('announcement-updates', AnnouncementUpdateViewSet)
router.register('announcement-preset', AnnouncementEmailPreConfigViewSet)

app_name = 'netbox_announcement-api'
urlpatterns = router.urls
