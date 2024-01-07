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
from django.core.exceptions import ObjectDoesNotExist



import requests
from fcm_django.models import FCMDevice

def send_notification(registration_ids, message_title, message_desc, post_id):
    fcm_api = "AAAAkV-gc5c:APA91bF4PJPVDpihuGhCzMljtG1RjI-ZOn0xLr8UscqsQGw6nPZ7mDz9ttTeXZUj6LHjT1fdwkhUEdXYa22jR-dJ-OEr3_MDwTbVNUsTB8Wofl8H8ApQ8Sbo8dkEnFNTR5OXeOIrtKTS"
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

        return redirect('Authentication:home')

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

        return redirect('Authentication:home')

    else:
        return HttpResponse("Method must be 'POST'")



def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('Authentication:home')




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

