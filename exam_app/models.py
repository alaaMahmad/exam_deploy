from django.db import models
import re
from datetime import datetime, date

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if not postData.get('first_name') or not postData.get('last_name') or not postData.get('email') or not postData.get('password'):
            errors["required"] = "All fields are required."
        
        if len(postData.get('first_name', '')) < 2:
            errors["first_name"] = "First name should be at least 2 characters."
            
        if len(postData.get('last_name', '')) < 2:
            errors["last_name"] = "Last name should be at least 2 characters."
            
        if not EMAIL_REGEX.match(postData.get('email', '')):
            errors["email"] = "Email must be a valid email."

        if User.objects.filter(email=postData.get('email')).exists():
            errors["email_exists"] = "Account email already exists."
            
        if len(postData.get('password', '')) < 8:
            errors["password_len"] = "Password minimum 8 characters."
            
        if postData.get('password') != postData.get('confirm_pw'):
            errors["pw_match"] = "PW and Confirm PW must match."
            
        return errors

class ShowManager(models.Manager):
    def show_validator(self, post_data, show_id=None):
        errors = {}
        if not post_data.get('title') or not post_data.get('network') or not post_data.get('comments') or not post_data.get('release_date'):
                    errors["required"] = "All fields are required."

        title = post_data.get('title', '').strip()
        if len(title) < 3:
            errors['title'] = "Title should be at least 3 characters."
        
    
        existing_shows = Show.objects.filter(title__iexact=title)
        if show_id:
            existing_shows = existing_shows.exclude(id=show_id)
        if existing_shows.exists():
            errors['title_unique'] = "A show with this title already exists in the database."


        network = post_data.get('network', '').strip()
        if len(network) < 3:
            errors['network'] = "Network should be at least 3 characters."


        release_date_str = post_data.get('release_date', '').strip()
        if not release_date_str:
            errors['release_date'] = "Release Date is required."
        else:
            try:
                input_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
                if input_date >= date.today():
                    errors['release_date_past'] = "Release Date should be in the past."
            except ValueError:
                errors['release_date_invalid'] = "Invalid release date format."


        comments = post_data.get('comments', '').strip()
        if len(comments) < 3:
            errors['comments'] = "comments must be at least 3 characters."

        return errors



class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    release_date = models.DateField()
    created_by = models.ForeignKey(User, related_name="shows", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()


class Comments(models.Model):
    test = models.TextField(blank=True)
    show = models.ForeignKey(Show, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)


def add_user(data, pw_hash):
    return User.objects.create(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=pw_hash
    )
def get_user_by_email(email):
    users = User.objects.filter(email=email)
    return users[0] if users else None
def get_user_by_id(user_id):
    return User.objects.get(id=user_id)



def add_show(data, user_id):
    user = get_user_by_id(user_id)
    comment = data['comments'].strip()
    return Comments.objects.create(
            test =comment,
            show=Show.objects.create(
                title=data['title'].strip(),
                network=data['network'].strip(),
                release_date=data['release_date'],
                created_by=user)   , 
             user=user 
            )
    

def get_all_shows():
    return Show.objects.all()

def get_show_by_id(id):
    return Show.objects.get(id=id)

def get_all_comments(show_id):
    show = get_show_by_id(show_id)
    return show.comments.all()

def update_show(show_id, data):
    show = get_show_by_id(show_id)
    show.title = data['title']
    show.network = data['network']
    show.release_date = data['release_date']
    show.comments.test = data['comments'].strip()
    show.save()
    return show


def delete_show(show_id, user_id):
    show = get_show_by_id(show_id)
    if show.created_by.id == user_id:
        show.delete()

def add_comment(text,id,user_id):
    show = get_show_by_id(id)
    user =User.objects.get(id=user_id)
    return Comments.objects.create(
            test =text,
            show=show,
            user=user 
        )
    
def delete_comment(comment_id):
    comment = Comments.objects.get(id=comment_id)
    comment.delete()


