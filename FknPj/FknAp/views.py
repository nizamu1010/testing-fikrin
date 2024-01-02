import os
from django.shortcuts import get_object_or_404, render, redirect
from . models import *
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib import messages ,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import ImageForm
from django.core.exceptions import ObjectDoesNotExist
# Create your views here. CustomUser    profile_pic

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment

import json
import requests
from firebase_admin.messaging import Message, Notification
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from fcm_django.models import FCMDevice



@csrf_exempt
@require_http_methods(['POST'])
def save_token(request):

    body_dict = json.loads(request.body.decode('utf-8'))
    token = body_dict['token']
    existe = FCMDevice.objects.filter(registration_id=token, active=True)

    if len(existe) > 0:
        return HttpResponseBadRequest(json.dumps ({ 'message': 'the token already exists'}))
    
    divice = FCMDevice()
    divice.registration_id = token
    divice.active= True

    #solo si el usuario esta autenticado procederemos a enlazarlo
    if request.user.is_authenticated: divice.user = request.user

    try:
        divice.save()
        return HttpResponse(json.dumps({ 'message': 'token guardado'}))
    except:
        return HttpResponseBadRequest(json.dumps({'message': 'no se ha podido guardar'}))
    


def send_notification(registration_ids, message_title, message_desc, post_id):
    fcm_api = "AAAAnvinOgI:APA91bGqvTyi96rSym5-ntZqPF3cWb9IVLsYu_Vtr9YWRZUeUutCYZIUO2Y6qzu0owSUHxEQdvaTostXYYfAQpP0B5Kxxw_IHXsrwcE9LyC9_1r-d_7vB6mGjWeY-oSt7iXzCLACmc4I"
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
        "Content-Type": "application/json",
        "Authorization": 'key=' + fcm_api
    }

    payload = {
        "registration_ids": registration_ids,
        "priority": "high",
        "notification": {
            "body": message_desc,
            "title": message_title + ": ",
        },
        "data": {
            "post_id": post_id,
        }
    }

    result = requests.post(url, data=json.dumps(payload), headers=headers)
    print(result.json())


def home(request):
    posts = Post.objects.all().order_by('-date_created')
    if request.user.is_authenticated:
        try:
            customuser = CustomUser.objects.get(username=request.user.username)
            context = {'customuser': customuser, 'posts': posts}
            return render(request, 'index.html', context)
        except ObjectDoesNotExist:
            pass

    return render(request, 'index.html', {'posts': posts,'comments':comments})



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('FknAp:home')
        else:
            error_message = 'Incorrect username or password.'
            return render(request, 'login.html',{'error_message':error_message})

    return render(request, 'login.html')



def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmation = request.POST.get('confirm-password')
        mobile_number = request.POST.get('mobile-number')

        if   username and password and mobile_number:
            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'signup.html',{'message_username':'This username is not available.'})

            elif CustomUser.objects.filter(mobile_number=mobile_number).exists():
                return render(request, 'signup.html',{'message_mbnumber':'This mobile number is already taken.'})

            elif password != confirmation:
                return render(request, 'signup.html',{'message_password':'Passwords must match.'})

            else:
                user = CustomUser.objects.create_user(username=username, password=password, mobile_number=mobile_number)
                user.mobile_number = mobile_number
                user.save()
                user = auth.authenticate(username=username,password=password)

                if user is not None:
                    auth.login(request,user)
                    return redirect('FknAp:home')

        else:
            messages.info(request, 'Please fill in all required fields.')
            return render(request, 'signup.html')

    return render(request, 'signup.html')



def terms_and_conditions(request):
    return render(request, 'terms.html')



def signout(request):
    auth.logout(request)
    return redirect('FknAp:home')



def profile(request):
    customuser = CustomUser.objects.get(username=request.user.username)
    context = {'customuser': customuser}
    return render(request, "profile.html", context)



def profile_cropping(request, user_id):
    form = ImageForm(request.POST or None, request.FILES or None)
    customuser = CustomUser.objects.get(username=request.user.username)

    if form.is_valid() and 'profile_pic' in request.FILES:
        # Remove the old profile image if it exists
        if customuser.profile_pic:
            if os.path.isfile(customuser.profile_pic.path):
                os.remove(customuser.profile_pic.path)

        # Save the new profile picture
        form.save_profile_pic(user_id)
        return redirect('FknAp:profile')

    context = {'form': form, 'customuser': customuser}
    return render(request, 'upt_image.html', context)



@login_required
def create_post(request):
    if request.method == 'POST':
        content_text = request.POST.get('content_text')

        post = Post.objects.create(creater=request.user, content_text=content_text)

        # Get the ID of the newly created post
        post_id = post.id

        try:
            devices = FCMDevice.objects.filter(active=True)
            registration_ids = [device.registration_id for device in devices]

            if registration_ids:
                message_title = request.user
                message_desc = content_text
                send_notification(registration_ids, message_title, message_desc, post_id)
                print('Notification sent to {} devices.'.format(len(registration_ids)))
            else:
                print('No active devices found for sending notifications.')

        except ObjectDoesNotExist:
            print('An error occurred: FCMDevice model not found or misconfigured.')
        except Exception as e:
            print('An error occurred:', str(e))


        return redirect('FknAp:home')

    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})



@csrf_exempt
def edit_post(request, post_id):
    if request.method == 'POST':
        text = request.POST.get('edit_text')
        post = get_object_or_404(Post, pk=post_id)
        post.content_text = text
        new_text = post.content_text
        post.edit_post(new_text=new_text)

        return redirect('FknAp:home')

    else:
        return HttpResponse("Method must be 'POST'")



def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('FknAp:home')




def comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        parent_comment_id = request.POST.get('parent_comment_id')
        parent_comment = None

        if parent_comment_id:
            parent_comment = Comment.objects.get(id=parent_comment_id)

        new_comment = Comment.objects.create(
            post=post,
            commenter=request.user,
            comment_content=comment_text,
            parent_comment=parent_comment,
        )

        return redirect('FknAp:comments', post_id)
    else:
        comments = Comment.objects.filter(post=post, parent_comment=None).order_by('-comment_time')
        customuser = CustomUser.objects.get(username=request.user.username)
        context = {
            'comments': comments,
            'post': post,
            'customuser': customuser
        }

        return render(request, 'comments.html', context)


def add_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    parent_comment = get_object_or_404(Comment, pk=comment_id)
    commenter = request.user  # Assuming you're using Django's authentication

    if request.method == 'POST':
        body = request.POST.get('body')  # Retrieve the reply content from the request

        new_reply = Comment.objects.create(
            post=parent_comment.post,
            commenter=commenter,
            comment_content=body,
            parent_comment=parent_comment
        )

        # return JsonResponse({'message': 'Reply added successfully!', 'reply_id': new_reply.id})
        comments = Comment.objects.filter(post=post, parent_comment=None).order_by('-comment_time')
        customuser = CustomUser.objects.get(username=request.user.username)
        context = {
            'comments': comments,
            'post': post,
            'customuser': customuser
        }

        return render(request, 'comments.html', context)

    return JsonResponse({'error': 'Invalid request'})


def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
        comments = Comment.objects.filter(post=post, parent_comment=None).order_by('-comment_time')

        customuser = CustomUser.objects.get(username=request.user.username)
        context = {
            'comments': comments,
            'post': post,
            'customuser': customuser
        }

        return render(request, 'comments.html', context)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



import firebase_admin
from firebase_admin import messaging

# Function to send push notifications using FCM
def send_push_notification(registration_token, title, message_body):
    # Create a message
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=message_body,
        ),
        token=registration_token,
    )

    # Send the message using the Firebase Admin SDK
    try:
        response = messaging.send(message)
        print("Successfully sent message:", response)
    except Exception as e:
        print("Error sending message:", e)


# Example usage in a Django view
from django.http import JsonResponse

def send_notification_view(request):
    # Get the device token from the request or database
    device_token = "DEVICE_TOKEN_HERE"

    # Send a push notification
    send_push_notification(
        token=device_token,
        title="New Message",
        body="You have a new message!"
    )

    return JsonResponse({"success": True})
