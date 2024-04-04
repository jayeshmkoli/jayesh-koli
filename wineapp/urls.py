from django.urls import path
from wineapp import views
from django.conf import settings
from django.conf.urls.static import static
from .views import forget_password

urlpatterns = [
    path('home',views.home),
    path('pdetails/<pid>',views.product_details),
    path('about',views.about),
    path('contact',views.contact),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('cart',views.cart),
    path('remove/<cid>',views.remove),
    path('viewcart',views.viewcart),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
   #path('makepayment',views.makepayment),
   path('forget', views.forget_password),
   


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
