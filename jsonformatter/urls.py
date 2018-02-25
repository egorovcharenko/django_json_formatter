from django.urls import path

from jsonformatter.views import FormatSubmitView, FormatAjaxSubmitView

app_name = 'formatter'
urlpatterns = [
    path('', FormatSubmitView.as_view(), name='index'),
    path('format-submit-view', FormatAjaxSubmitView.as_view(), name='format-submit-view'),
]
