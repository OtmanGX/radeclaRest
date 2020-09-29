"""radeclaRest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# Local view apps
from core import views as core_views
from radeclaRest import settings
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from django.conf.urls.static import static
from core.views import ReservationViewSet, MembreViewSet, CategorieViewSet, CotisationViewSet
from dashboard.views import dashboard_view, terrain_stats, top_hours_stats, training_stats, total_cotisation, \
    cotisation_a_payer, members_stats
from core.task import SerialThread
router = routers.DefaultRouter()
router.register(r'reservation', ReservationViewSet, basename='Reservations')
router.register(r'membre', MembreViewSet, basename='membre')
router.register(r'categories', CategorieViewSet, basename='categories')
router.register(r'cotisations', CotisationViewSet, basename='cotisations')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    # System
    path('hello/', core_views.HelloView.as_view(), name='hello'),
    # Auth
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/terrains', terrain_stats, name='terrain'),
    path('dashboard/hours', top_hours_stats, name='hours'),
    path('dashboard/training', training_stats, name='training'),
    path('dashboard/totalcotisation', total_cotisation, name='totalcotisation'),
    path('dashboard/cotisationapayer', cotisation_a_payer, name='cotisationapayer'),
    path('dashboard/members_stats', members_stats, name='members_stats'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# SerialThread().start()