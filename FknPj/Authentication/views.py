from django.shortcuts import render
import os
from django.shortcuts import get_object_or_404, render, redirect
from . models import *
from FknAp.models import Post, Comment
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib import messages ,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Authentication.forms import ImageForm
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
                    return redirect('Authentication:home')

        else:
            messages.info(request, 'Please fill in all required fields.')
            return render(request, 'signup.html')

    return render(request, 'signup.html')



def terms_and_conditions(request):
    return render(request, 'terms.html')



def signout(request):
    auth.logout(request)
    return redirect('Authentication:home')



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
        return redirect('Authentication:profile')

    context = {'form': form, 'customuser': customuser}
    return render(request, 'upt_image.html', context)



from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
import json

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
        return HttpResponse(json.dumps({ 'message': 'token saved token'}))
    except:
        return HttpResponseBadRequest(json.dumps({'message': 'could not be saved'}))
    
