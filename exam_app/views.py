from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from . import models

def landing_page(request):
    if 'user_id' in request.session:
        return redirect('/shows')
    return render(request, 'landing.html')

def register(request):
    if request.method == 'POST':
        errors = models.User.objects.register_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        
        user = models.add_user(request.POST, pw_hash)
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        return redirect('/shows')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        user = models.get_user_by_email(request.POST['email'])
        if user and bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            return redirect('/shows')
        
        messages.error(request, "Invalid account or password.")
        return redirect('/')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')



def shows(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    context = {
        'logged_user': models.get_user_by_id(request.session['user_id']),
        'all_shows': models.get_all_shows()
    }
    return render(request, 'shows.html', context)

def create_show(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    if request.method == 'POST':
        errors = models.Show.objects.show_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/create')
            
        models.add_show(request.POST, request.session['user_id'])
        return redirect('/shows')
        
    context = {'logged_user': models.get_user_by_id(request.session['user_id'])}
    return render(request, 'create_show.html', context)

def edit_show(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
        
    if request.method == 'POST':
        errors = models.Show.objects.show_validator(request.POST,show_id=id)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/edit/{id}')
            
        models.update_show(id, request.POST)
        return redirect('/shows')

    context = {
        'logged_user': models.get_user_by_id(request.session['user_id']),
        'show': models.get_show_by_id(id)
    }
    return render(request, 'edit_show.html', context)

def view_show(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
        
    context = {
        'logged_user': models.get_user_by_id(request.session['user_id']),
        'show': models.get_show_by_id(id),
        'all_comments': models.get_all_comments(id)
    }
    return render(request, 'view_show.html', context)

def delete_show(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
        
    models.delete_show(id, request.session['user_id'])
    return redirect('/shows')

def add_comment(request,id):
    if 'user_id' not in request.session:
            return redirect('/')
    if request.method == 'POST':
        text = request.POST.get('comments', '').strip()
        if len(text) < 2:
            messages.error(request,"it must be 2 char or above")
        else:
            models.add_comment(text,id,request.session['user_id'])
    return redirect(f'/view/{id}')

def delete_comment(request,id,show_id):
    if 'user_id' not in request.session:
                return redirect('/')
    if request.method == 'POST':
        comment = models.Comments.objects.get(id = id)
        if comment.user.id == request.session['user_id']:
            models.delete_comment(id)
            return redirect(f'/view/{show_id}')


