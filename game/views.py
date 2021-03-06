from django.shortcuts import render, render_to_response, redirect
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from game.models import Image, UserProfile
from game.models import ClassificationResult, CountResult

import os
import logging

logger = logging.getLogger(__name__)

def csrf_render(request, htmlpage, context):
    '''Wrapper for rendering to response with CSRF token in context'''
    context.update(csrf(request))
    return render_to_response(htmlpage, context)

# @login_required
def index(request):
    '''Home page'''
    logger.debug('Serve index')
    
    user = request.user
    splash_url = "/game/game-splash"
    if user.is_authenticated():
        up = UserProfile.objects.get(user=user)
        if up.game_mode == UserProfile.COUNTING:
            splash_url = "/game/game2-splash"
        else:
            splash_url = "/game/game-splash"
    
    return csrf_render(request,'index.html', locals())

@login_required
def game(request):
    '''Classification game'''
    logger.debug('Serve game mode 1 page')
    
    c = {}
    user = request.user
    image_url = Image.objects.order_by('?')[0].url # TODO: Redundant
    if user.is_authenticated():
        image_url = Image.objects.filter(status=Image.NEW)[user.userprofile.img_idx].url
    
    c.update({'image_url' : image_url})
    return csrf_render(request, 'game.html', c) 

@login_required
def game2(request):
    '''Counting game'''
    logger.debug('Serve game mode 2 page')
    
    c = {}
    user = request.user
    image_url = Image.objects.order_by('?')[0].url # TODO: Redundant
    if user.is_authenticated():
        image_url = Image.objects.filter(status=Image.NEW)[user.userprofile.img_idx].url

    c.update({'image_url' : image_url})
    return csrf_render(request, 'game2.html', c) 

@login_required
def gameSplash(request):
    logger.debug('Serve game mode 1 splash')
    return render_to_response('game-splash.html', locals()) 

@login_required
def game2Splash(request):
    logger.debug('Serve game mode 2 splash')
    return render_to_response('game2-splash.html', locals()) 

@login_required
def game_submit_task(request):
    logger.debug(request)
    
    if request.method == "POST":
        logger.debug("Get the post from the game")
        post = request.POST.copy()
        
        flowerbool = True if int(post.get('flowerbool')) else False
        budbool = True if int(post.get('budbool')) else False
        fruitbool = True if int(post.get('fruitbool')) else False
       
        logger.debug("POST request data: %s, %s, %s" % \
                        (flowerbool,
                        budbool,
                        fruitbool))
        
        user = request.user
        if user.is_authenticated():
            userprofile = UserProfile.objects.get(user=user)
            result = ClassificationResult(user=userprofile.user.username, \
                         image=Image.objects.all()[userprofile.img_idx], \
                         flower_bool=flowerbool, \
                         bud_bool=budbool, \
                         fruit_bool=fruitbool)
            result.save()
            
            if len(Image.objects.all()) > userprofile.img_idx + 1:
                userprofile.img_idx += 1
                userprofile.save()
            else:
                return redirect('/game/done')
        
        return redirect('/game/game')
    else:
        return HttpResponseServerError("post error: not a post")

@login_required
def game2_submit_task(request):
    logger.debug(request)
    
    if request.method == "POST":
        logger.debug("Get the post from game 2")
        post = request.POST.copy()
        coords = post.get('coords')
        logger.debug("POST request data: %s" % coords) 
        
        user = request.user
        if user.is_authenticated():
            userprofile = UserProfile.objects.get(user=user)
            result = CountResult(user=userprofile.user.username, \
                         image=Image.objects.all()[userprofile.img_idx], \
                         coords=coords)
            result.save()

            if len(Image.objects.all()) > userprofile.img_idx + 1:
                userprofile.img_idx += 1
                userprofile.save()
            else:
                return redirect('/game/done')
        
        return redirect('/game/game2')
    else:
        return HttpResponseServerError("post error: not a post")

@login_required
def game_skip(request):
    logger.debug("Get the skip from game")
    if request.method == "POST":
        user = request.user
        if user.is_authenticated():
            userprofile = UserProfile.objects.get(user=user)
            if len(Image.objects.all()) > userprofile.img_idx + 1:
                userprofile.img_idx += 1
                userprofile.save()
            else:
                return redirect('/game/done')

        return redirect('/game/game')    
    else:
        return HttpResponseServerError("post error: not a post")

@login_required
def game2_skip(request):
    logger.debug("Get the skip from game 2")
    if request.method == "POST":
        user = request.user
        if user.is_authenticated():
            userprofile = UserProfile.objects.get(user=user)
            if len(Image.objects.all()) > userprofile.img_idx + 1:
                userprofile.img_idx += 1
                userprofile.save()
            else:
                return redirect('/game/done')

        return redirect('/game/game2')
    else:
        return HttpResponseServerError("post error: not a post")

@login_required
def session_complete(request):
    logger.debug("Session completed")
    username = request.user.username
    return render_to_response("session-complete.html", locals())
