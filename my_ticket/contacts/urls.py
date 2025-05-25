from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'contacts', views.ContactViewSet, basename='contact')
router.register(r'addresses', views.AddressViewSet, basename='address')

urlpatterns = router.urls
