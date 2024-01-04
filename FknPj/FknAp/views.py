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


def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyDkyNO4aWT4qVCVJwkcb354_Rtc-TdFybk",' \
         '        authDomain: "fknpj-9c7bb.firebaseapp.com",' \
         '        databaseURL: "",' \
         '        projectId: "fknpj-9c7bb",' \
         '        storageBucket: "fknpj-9c7bb.appspot.com",' \
         '        messagingSenderId: "624374608791",' \
         '        appId: "1:624374608791:web:143bdac26d9762dcbb0ad2",' \
         '        measurementId: "G-93ZXLVMBCF"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")



from django.http.request import HttpHeaders
from django.shortcuts import render

from django.http import HttpResponse
import requests
import json



def send_notification(registration_ids , message_title , message_desc):
    fcm_api = "AAAAkV-gc5c:APA91bF4PJPVDpihuGhCzMljtG1RjI-ZOn0xLr8UscqsQGw6nPZ7mDz9ttTeXZUj6LHjT1fdwkhUEdXYa22jR-dJ-OEr3_MDwTbVNUsTB8Wofl8H8ApQ8Sbo8dkEnFNTR5OXeOIrtKTS"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+fcm_api}

    payload = {
        "registration_ids" :registration_ids,
        "priority" : "high",
        "notification" : {
            "body" : message_desc,
            "title" : message_title,
            "image" : "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
            "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",
            
        }
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers )
    print(result.json())




def send(request):
    resgistration  = ['enhsXcb0AkFu2xF3T3sAcX:APA91bGr5vsfBy7Jh7iim53-Ic14_XPwrAp9PpIGLqoc18YoHflom-9KKnPjIGO1chQa1AEFKZkVsauH7Bn6-LMMJ9zQV-SP5NQKM6pDdTrjakLHHsupvcmVQQwH0GYCCJP9AT0gR2q6']
    send_notification(resgistration , 'Code Keen added a new video' , 'Code Keen new video alert')
    return HttpResponse("sent")

