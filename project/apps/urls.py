
from django.conf.urls import url, include

urlpatterns = [
    url('order/',include("project.apps.order.urls")),
    url('catalogue/',include("project.apps.catalogue.urls")),

]
