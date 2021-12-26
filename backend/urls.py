from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from accounts.views import AccountAPI, ChildofChildAccountAPI, EntryPermitAPI, ChildAccountAPI, ProgressAPI
from citizens.views import CitizenAPI, CitizenStatisticAPI
from reports.views import ReportAPI
from users.views import UserAPI, CustomAuthToken, WhoAmI


urlpatterns = [
    path('admin/', admin.site.urls),
]

router = routers.DefaultRouter()
router.register(r'user', UserAPI)

urlpatterns += [
    url('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view(), name="obtain-token"),
    path('whoami/', WhoAmI.as_view(), name="who-am-i")
]

urlpatterns += [
    path('account/', AccountAPI.as_view(), name="account"),
    path('account/children/', ChildAccountAPI.as_view(), name='child-account'),
    path('account/entry/', EntryPermitAPI.as_view(), name='change-entry-permit'),
    path('account/children/progress/', ProgressAPI.as_view(),
         name='child-account-progress'),
    path('account/children/find/', ChildofChildAccountAPI.as_view(),
         name='find-child-of-child'),
]

urlpatterns += [
    path('citizen/', CitizenAPI.as_view(), name="citizen"),
    # path('statistics/ages/', CitizenAgesAPI.as_view(), name="citizen_ages"),
    path('citizen/stats/', CitizenStatisticAPI.as_view(),
         name='citizen-statistics'),
]

urlpatterns += [
    path('report/', ReportAPI.as_view(), name="report")
]
