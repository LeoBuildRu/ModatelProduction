from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page),
    path('catalog', views.catalog_page),
    path('filter/', views.filter_data, name='filter_data'),
    path('detail-page/<str:id>', views.detail_page, name='detail_page'),
    path('gallery', views.gallery_page),
    path('blog', views.blog_page),
    path('post-page/<str:id>', views.post_page, name='post_page'),
    path('about_us', views.about_us_page),
    path('privPol', views.PrivPol_page),
    path('contacts', views.contacts_page),
    path('send_email/', views.send_email, name='send_email'),
]