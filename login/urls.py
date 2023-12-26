#REFERENCES
#Title: Upload Images To Django - Django Wednesdays #38
#URL: https://www.youtube.com/watch?v=O5YkEFLXcRg&ab_channel=Codemy.com

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home),
    path("logout", views.logout_view),
    path('welcome/', views.welcome, name='welcome'),
    path("welcome/claim_item/<int:item_id>/",
         views.claim_item, name="claim_item"),
    path("welcome/logout", views.logout_view),
    path("welcome/upload_an_item", views.upload_item_view, name="upload_item"),
    path("welcome/success", views.success_view, name="success_upload"),
    path("welcome/manage_uploaded_items",
         views.manage_uploads_view, name="manage_uploads"),
    path("welcome/manage_uploaded_items/delete_item/<int:item_id>/",
         views.delete_item, name="delete_item"),
    path("welcome/manage_uploaded_items/approve_item/<int:item_id>/",
         views.approve_item, name="approve_item"),
    path("welcome/admin_my_uploads",
         views.my_uploads_admin_view, name="my_uploads_admin"),
    path("welcome/my_uploads", views.my_uploads_user_view, name="my_uploads"),
    path("welcome/admin_upload_an_item",
         views.upload_item_view_admin, name="upload_item_admin"),
    path("welcome/admin_success", views.admin_success_view,
         name="admin_success_upload"),
    path("welcome/notifications", views.notifications_user_view,
         name="user_notifications"),
    path("welcome/notifications_admin",
         views.notifications_admin_view, name="admin_notifications"),
    path("welcome/my_account", views.my_account_user_view, name="user_my_account"),
    path('welcome/notifications/delete_notification/<int:notification_id>/',
         views.delete_notification, name='delete_notification'),
    path('welcome/notifications_admin/delete_notification/<int:notification_id>/',
         views.admin_delete_notification, name='admin_delete_notification'),
    path("welcome/my_uploads/user_delete_upload/<int:item_id>/",
         views.user_delete_upload, name="user_delete_upload"),
    path("welcome/admin_my_uploads/admin_delete_upload/<int:item_id>/",
         views.admin_delete_upload, name="admin_delete_upload"),
    path("welcome/admin_my_account",
         views.my_account_admin_view, name="admin_my_account"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
