"""
REFERENCES:

Title: Django: detect admin login in view or template
URL: https://stackoverflow.com/questions/11916297/django-detect-admin-login-in-view-or-template

Title: Upload Images To Django - Django Wednesdays #38
URL: https://www.youtube.com/watch?v=O5YkEFLXcRg&ab_channel=Codemy.com

Title: Stack Overflow "Django, change username"
URLS: https://stackoverflow.com/questions/14355183/django-change-username
Date: 11/19/2023

Tite: What is the use of cleaned data in Django?
URL: https://stackoverflow.com/questions/53594745/what-is-the-use-of-cleaned-data-in-django

Title: What's the best way to store a phone number in Django models?
URL:https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-a-phone-number-in-django-models

Title: Django 2: upload media to Google Cloud Storage with google-cloud-storage
URL:https://stackoverflow.com/questions/57653663/django-2-upload-media-to-google-cloud-storage-with-google-cloud-storage
"""


from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import AdminAccount, Lost_Item, Notification, UserProfile
from django.conf import settings
from .forms import UploadItemForm, ChangeUsername, ChangePhonenum
from django.contrib.auth.decorators import login_required
import json
from django.core.files.storage import default_storage
from google.cloud import storage
from django.contrib.auth.models import User
from django.http import JsonResponse


def home(request):
    if request.user.is_authenticated:
        qs = Lost_Item.objects.all()
        lost_items = qs.filter(approved=True)
        username = request.user.username
        email = request.user.email
        admin = False
        for x in AdminAccount.objects.all():
            if x.email == email:
                admin = True
        if admin:
            return render(request, "admin.html", {"username": username, "email": email, "lost_items": lost_items})
        else:
            return render(request, "welcome.html", {"username": username, "email": email, "lost_items": lost_items})
    return render(request, "home.html")


def logout_view(request):
    logout(request)
    return redirect("/")


def welcome(request):
    qs = Lost_Item.objects.all()
    lost_items = qs.filter(approved=True)
    username = request.user.username
    name = request.user.get_full_name()
    email = request.user.email
    admin = False
    for x in AdminAccount.objects.all():
        if x.email == email:
            admin = True
    if admin:
        return render(request, "admin.html", {"name": name, "username": username, "email": email, "lost_items": lost_items})
    else:
        return render(request, "welcome.html", {"name": name, "username": username, "email": email, "lost_items": lost_items})


def upload_item_view(request):
    if request.method == 'POST':
        form = UploadItemForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            uploaded_file = request.FILES.get('item_image')
            if uploaded_file:  # Check if an image file was uploaded
                client = storage.Client()
                bucket = client.get_bucket('a25-image')
                # Create a blob in the specified bucket
                blob = bucket.blob(uploaded_file.name)
                # Upload the file to Google Cloud Storage
                blob.upload_from_string(
                    uploaded_file.read(),
                    content_type=uploaded_file.content_type
                )
                # Save the URL of the uploaded file in your model
                obj.image_url = blob.public_url
            obj.save()
            return redirect('success_upload')
        else:
            print(form.errors)
    else:
        form = UploadItemForm()

    return render(request, "upload.html", {'form': form})


def upload_item_view_admin(request):
    if request.method == 'POST':
        form = UploadItemForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            uploaded_file = request.FILES.get('item_image')
            if uploaded_file:  # Check if an image file was uploaded
                client = storage.Client()
                bucket = client.get_bucket('a25-image')
                # Create a blob in the specified bucket
                blob = bucket.blob(uploaded_file.name)
                # Upload the file to Google Cloud Storage
                blob.upload_from_string(
                    uploaded_file.read(),
                    content_type=uploaded_file.content_type
                )
                # Save the URL of the uploaded file in your model
                obj.image_url = blob.public_url
            obj.save()
            return redirect('admin_success_upload')
        else:
            print(form.errors)
    else:
        form = UploadItemForm()

    return render(request, "admin-upload.html", {'form': form})


def success_view(request):
    return render(request, 'success.html')


def admin_success_view(request):
    return render(request, 'admin_success.html')


def manage_uploads_view(request):
    qs = Lost_Item.objects.all()
    lost_items_pending = qs.filter(approved=False)
    lost_items_approved = qs.filter(approved=True)
    return render(request, 'manage-uploads.html', {'lost_items_pending': lost_items_pending, 'lost_items_approved': lost_items_approved})


def delete_item(request, item_id):
    item = Lost_Item.objects.get(pk=item_id)
    item.delete()
    return redirect('manage_uploads')


def my_uploads_admin_view(request):
    admin_uploads = Lost_Item.objects.filter(user=request.user)
    return render(request, 'admin-my-uploads.html', {'user_uploads': admin_uploads})


def my_uploads_user_view(request):
    user_uploads = Lost_Item.objects.filter(user=request.user)
    return render(request, 'user-my-uploads.html', {'user_uploads': user_uploads})


def notifications_user_view(request):
    return render(request, 'user-notifications.html')


def decline_item(request, item_id):
    if request.method == 'POST':
        item = Lost_Item.objects.get(pk=item_id)
        explanation = request.POST.get('explanation')
        item.admin_explanation = explanation
        item.delete()
        Notification.objects.create(
            user=item.user, message=f"Your upload '{item.name}' was declined. Reason: {explanation}")
    return redirect('manage_uploads')


def approve_item(request, item_id):
    item = Lost_Item.objects.get(pk=item_id)
    item.approved = True
    item.save()
    Notification.objects.create(
        user=item.user, message=f"Your upload '{item.name}' was approved.")
    return redirect('manage_uploads')


def notifications_user_view(request):
    notifications = Notification.objects.filter(
        user=request.user).order_by('-date')
    return render(request, 'user-notifications.html', {'notifications': notifications})


def claim_item(request, item_id):
    item = Lost_Item.objects.get(pk=item_id)
    username = request.user.username
    email = request.user.email
    phone = request.user.userprofile.phone_number
    owner_phone = item.user.userprofile.phone_number
    if phone == "":
        Notification.objects.create(
            user=item.user, message=f"Your upload '{item.name}' was claimed by '{username}'. You can contact them at '{email}'."
        )
    else:
        Notification.objects.create(
            user=item.user, message=f"Your upload '{item.name}' was claimed by '{username}'. You can contact them at '{email}' or phone number: '{phone}'."
        )
    if owner_phone == "":
        Notification.objects.create(
            user=request.user, message=f"You claimed '{item.name}' which was posted by '{item.user.username}'. You can contact them at '{item.user.email}'."
        )
    else:
        Notification.objects.create(
            user=request.user, message=f"You claimed '{item.name}' which was posted by '{item.user.username}'. You can contact them at '{item.user.email}' or phone number: '{owner_phone}'."
        )
    return JsonResponse({"status": "success", "message": "Item claimed successfully"})

# Title: Django date query from newest to oldest
# URL: https://stackoverflow.com/questions/30314741/django-date-query-from-newest-to-oldest


def notifications_admin_view(request):
    notifications = Notification.objects.filter(
        user=request.user).order_by('-date')
    return render(request, 'admin-notifications.html', {'notifications': notifications})


def my_account_user_view(request):
    user = request.user
    message = ""
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'name_form':
            form = ChangeUsername(request.POST)
            phone_form = ChangePhonenum(instance=profile)
            if form.is_valid():
                new_username = form.cleaned_data['new_username']
                exists = False
                users = User.objects.all()
                for u in users:
                    if u.username == new_username:
                        exists = True
                message = "The username " + new_username + \
                    " was already taken. Please try again!"
                if not exists:
                    user.username = new_username
                    message = "Your username was successfully changed to " + new_username + "."
                    user.save()
        elif form_type == 'phone_form':
            phone_form = ChangePhonenum(request.POST, instance=profile)
            form = ChangeUsername()
            if phone_form.is_valid():
                # Update phone number
                phone_form.save()
                message = "Phone number updated successfully."
            # return redirect('user_my_account')
    else:
        form = ChangeUsername()
        phone_form = ChangePhonenum()

    context = {
        'form': form,
        'phone_form': phone_form,
        'username': user.username,
        'email': user.email,
        'phone': profile.phone_number,
        'message': message,
    }
    return render(request, 'user-my-account.html', context)


def delete_notification(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.delete()
    return redirect('user_notifications')


def admin_delete_notification(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.delete()
    return redirect('admin_notifications')


def user_delete_upload(request, item_id):
    item = Lost_Item.objects.get(pk=item_id)
    item.delete()
    return redirect('my_uploads')


def admin_delete_upload(request, item_id):
    item = Lost_Item.objects.get(pk=item_id)
    item.delete()
    return redirect('my_uploads_admin')


def my_account_admin_view(request):
    user = request.user
    message = ""

    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'name_form':
            form = ChangeUsername(request.POST)
            phone_form = ChangePhonenum(instance=profile)
            if form.is_valid():
                new_username = form.cleaned_data['new_username']
                exists = False
                users = User.objects.all()
                for u in users:
                    if u.username == new_username:
                        exists = True
                message = "The username " + new_username + \
                    " was already taken. Please try again!"
                if not exists:
                    user.username = new_username
                    message = "Your username was successfully changed to " + new_username + "."
                    user.save()
        elif form_type == 'phone_form':
            phone_form = ChangePhonenum(request.POST, instance=profile)
            form = ChangeUsername()
            if phone_form.is_valid():
                # Update phone number
                phone_form.save()
                message = "Phone number updated successfully."
            # return redirect('user_my_account')
    else:
        form = ChangeUsername()
        phone_form = ChangePhonenum()

    context = {
        'form': form,
        'phone_form': phone_form,
        'username': user.username,
        'email': user.email,
        'phone': profile.phone_number,
        'message': message,
    }
    return render(request, 'admin-my-account.html', context)
