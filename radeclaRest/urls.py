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
from config.views import read_config_request
from core import views as core_views
from radeclaRest import settings
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from django.conf.urls.static import static
from core.views import ReservationViewSet, MembreViewSet, CategorieViewSet, CotisationViewSet
from dashboard.views import dashboard_view, terrain_stats, top_hours_stats, training_stats, total_cotisation, \
    cotisation_a_payer, members_stats, export_membres_toexcel, main_stats, terrain_stats_hours, lighting_stats
from core.task import SerialThread
from school.views import SchoolViewSet
from tournament.views import TournamentViewSet, some_view

router = routers.DefaultRouter()
router.register(r'reservation', ReservationViewSet, basename='Reservations')
router.register(r'membre', MembreViewSet, basename='membre')
router.register(r'categories', CategorieViewSet, basename='categories')
router.register(r'cotisations', CotisationViewSet, basename='cotisations')
router.register(r'tournois', TournamentViewSet, basename='tournois')
router.register(r'schools', SchoolViewSet, basename='schools')

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
    path('dashboard/excel_membres', export_membres_toexcel, name='excel_membres'),
    path('dashboard/main_stats', main_stats, name='main_stats'),
    path('dashboard/terrain_stats_hours', terrain_stats_hours, name='terrain_stats_hour'),
    path('dashboard/lighting_stats', lighting_stats, name='lighting_stats'),
    # Config
    path('config/configs', read_config_request, name='configs'),
    #Download
    path('download/tournoi', some_view, name='download'),

]

# SerialThread().start()