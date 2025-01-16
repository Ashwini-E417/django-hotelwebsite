from django.urls import path
from hotelapp import views
from django.conf.urls.static import static
from hotelweb import settings

urlpatterns = [
    path('index',views.index),
    path('login',views.ulogin),
    path('logout',views.ulogout),
    path('register',views.register),
    path('aboutus',views.aboutus),
    path('contact',views.contact),
    path('rdetails/<rid>',views.rdetails),
    path('custdetail/<rid>/<cin>/<cout>',views.custdetail),
    path('bedtype/<bid>',views.bedtype),
    path('sort',views.sort),
    path('checkavailbility/<cid>',views.checkavailbility),
    path('cancel/<rid>',views.cancel),
    path('confirm/<rid>/<cin>/<cout>',views.confirm),
    path('finalbooking',views.finalbooking),
    path('mybooking',views.mybooking),
    path('moredate/<mid>',views.moredate),
    path('remove/<bid>',views.remove),
    path('cancelbooking/<bid>',views.cancelbooking),
    path('booknow/<bid>',views.booknow),
    path('location',views.location),
    path('bookconfirm/<bid>',views.bookconfirm),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)