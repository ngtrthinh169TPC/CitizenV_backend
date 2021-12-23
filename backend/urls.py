from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from accounts.views import AccountAPI
from users.views import UserAPI, CustomAuthToken
# from citizenss.views import CitizenAPI, CitizenAgesAPI
from citizens.views import CitizenAPI


urlpatterns = [
    path('admin/', admin.site.urls),
]

router = routers.DefaultRouter()
router.register(r'user', UserAPI)

urlpatterns += [
    url('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view(), name="obtain-token"),
]

urlpatterns += [
    path('account/', AccountAPI.as_view(), name="account"),
    path('citizen/', CitizenAPI.as_view(), name="citizen"),
    # path('statistics/ages/', CitizenAgesAPI.as_view(), name="citizen_ages"),
]
