from django.conf.urls import url
from . import views
import django
from django.views import static


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^to_index$', views.index, name='to-index'),
    # auth
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^authenticate$', views.authenticate, name='authenticate'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^signup/submit$', views.signup_submit, name='signup-submit'),
    url(r'^set_info$', views.set_info, name='set-info'),
    url(r'^set_info/submit$', views.set_info_submit, name='set-info-submit'),
    url(r'^activities_list$', views.activities_list, name='activities-list'),
    url(r'^delete_activity/([1-9][0-9]*)$', views.delete_activity, name='delete-activity'),
    url(r'^choose_activity_from_list/([1-9][0-9]*)$', views.choose_activity_from_list, name='choose-from-list'),
    url(r'^activity_info/([1-9][0-9]*)$', views.activity_info, name='activity-info'),
    url(r'^activity_info/([1-9][0-9]*)/submit$', views.activity_info_submit, name='activity-info-submit'),
    url(r'^to_list$', views.to_list, name='to-list'),
    url(r'^to_search$', views.to_search, name='to-search'),
    url(r'^search/submit$', views.search_submit, name='search-submit'),
    url(r'^arrange$', views.arrange, name='arrange'),
    url(r'^type_in_single$', views.type_in_single, name='type-in-single'),
    url(r'^type_in_single/submit$', views.type_in_single_submit, name='type-in-single-submit'),
    url(r'^type_in_multi$', views.type_in_multi, name='type-in-multi'),
    url(r'^type_in_multi/submit$', views.type_in_multi_submit, name='type-in-multi-submit'),
    url(r'^static/(?P<path>.*)', django.views.static.serve,
        {'document_root': '/Users/JHT/Desktop/python/activity_arrangements/arrangements/static/img'}),
    url(r'^arrange/download$', views.arranged_file, name='MyArrangement'),
]

