from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from core.forms import *
from core.models import *
import datetime
from django.shortcuts import get_object_or_404


all_tags = ['Book', 'Business', 'Cartoon', 'Cosmetic', 'communication', 'Electronic Devices', 'Education', 
            'Entertainment', 'Friend', 'Food', 'Family', 'Game', 'Healthy', 'Love', 'Life style', 
            'Music', 'Movie', 'Social', 'Social network', 'Sport', 'Travel', 'Vehicle']

# Create your views here.
def home(request):
    count = User.objects.count()
    topic_all = Topic.objects.all()
    time_create_topic = Create.objects.all()

    zip_topic_user = zip(topic_all,time_create_topic)

    return render(request, 'home.html', {
        'count': count,'topic_all': topic_all , 'zip_topic_user' : zip_topic_user, 'all_tags': all_tags
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })

def create_topic(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login")
    elif request.method == 'POST':
        form = create_topic_form(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)

            create_title = request.POST.get('title')
            create_content = request.POST.get('content')

            topic.title = create_title
            topic.content = create_content
            topic.user_name = request.user
            topic.like = 0
            topic.save()

            tag = request.POST.getlist('tags')

            for i in tag:
                create_tag_topic = Tag.objects.create(topicid=topic,
                                                        tag=i)

            #time create topic
            create_time_topic = Create.objects.create(userid=request.user,
                                                        topicid=topic,
                                                        date=datetime.datetime.now())
            return HttpResponseRedirect("/")
    else:
        form = create_topic_form()
        return render(request, 'create_topic.html', {
        'form': form,
        'all_tags': all_tags
    })

def create_comment(request,topic_id):
    select_topic = Topic.objects.get(topicid=topic_id)

    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login")
    elif request.method == 'POST':
        tpid = Topic.objects.get(topicid= topic_id)
        form = create_comment_form(request.POST)

        if form.is_valid():
            create_comment = request.POST.get('content')
            comment = form.save(commit=False)
            comment.comuserid = request.user
            comment.comtopicid = tpid
            comment.content = create_comment
            comment.like = 0
            comment.date = datetime.datetime.now()
            comment.save()

        url_redirect = '/topic/' + str(topic_id)
        return HttpResponseRedirect(url_redirect)
    else:
        form = create_comment_form()
        return render(request, 'view_topic.html', {
        'form': form , 'select_topic' : select_topic
    })

def view_topic(request,topic_id):
    select_topic = Topic.objects.get(topicid=topic_id)

    comment_topic = Comment.objects.filter(comtopicid=topic_id)

    tags_topic = Tag.objects.filter(topicid=topic_id)

    time_create_topic = Create.objects.get(userid=select_topic.user_name,topicid=select_topic)

    if not request.user.is_authenticated:
         return render(request, 'view_topic.html', { 'select_topic' : select_topic, 'comment_topic' : comment_topic, 
                        'time_create_topic':time_create_topic})
    else:
        try:
            user_like = LikeTopic.objects.get(userid=request.user,like_topicid=select_topic)
        except LikeTopic.DoesNotExist:
            user_like = None

        user_like_comment = LikeComment.objects.filter(topicid=topic_id,userid=request.user)

        list_comment = []
        list_user_like = []
        list_check = []
        list_tag = []

        for i in comment_topic:
            print(i.commentid) 
            list_comment.append(str(i.commentid)) 
        
        for j in user_like_comment:
            print(j.like_commentid)
            list_user_like.append(str(j.like_commentid))

        for check in list_comment:
            if check in list_user_like:
                print('True')
                list_check.append(True)
            else:
                print('False')
                list_check.append(False)

        zip_com_user = zip(comment_topic, list_check)

        for tag in tags_topic:
            list_tag.append(tag)

        return render(request, 'view_topic.html', { 'select_topic' : select_topic,
                        'time_create_topic':time_create_topic, 'user_like':user_like, 
                        'zip_com_user':zip_com_user, 'list_tag': list_tag})

def edit_topic(request,topic_id):
    select_topic = Topic.objects.get(topicid=topic_id)
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login")
    elif request.method == 'POST':
        form = edit_topic_form(request.POST)
        if form.is_valid():
            edit_title = request.POST.get('title')
            edit_content = request.POST.get('content')
            
            edit_topic = Topic.objects.filter(topicid=topic_id).update(title=edit_title, content=edit_content)

        url_redirect = '/topic/' + str(select_topic.topicid)
        return HttpResponseRedirect(url_redirect)
    else:
        form = edit_topic_form()
        return render(request, 'edit_topic.html', {'form' : form, 'select_topic' : select_topic})

def delete_topic(request, topic_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login")
    else:
        delete_topic = Topic.objects.filter(topicid=topic_id).delete()
        delete_comment = Comment.objects.filter(comtopicid=topic_id).delete()

        return HttpResponseRedirect("/")

def edit_comment(request, comment_id):
    select_comment = Comment.objects.get(commentid=comment_id)
    get_id_topic = Comment.objects.get(commentid=comment_id)
    select_topic = Topic.objects.get(title=get_id_topic.comtopicid)

    topic_id = select_topic.topicid
    select_topic = Topic.objects.get(topicid=topic_id)

    comment_topic = Comment.objects.filter(comtopicid=topic_id)

    time_create_topic = Create.objects.get(userid=select_topic.user_name,topicid=select_topic)

    try:
        user_like = LikeTopic.objects.get(userid=request.user,like_topicid=select_topic)
    except LikeTopic.DoesNotExist:
        user_like = None

    user_like_comment = LikeComment.objects.filter(topicid=topic_id,userid=request.user)

    list_comment = []
    list_user_like = []
    list_check = []

    for i in comment_topic:
        list_comment.append(str(i.commentid))
    
    for j in user_like_comment:
        list_user_like.append(str(j.like_commentid))

    for check in list_comment:
        if check in list_user_like:
            print('True')
            list_check.append(True)
        else:
            print('False')
            list_check.append(False)

    zip_com_user = zip(comment_topic, list_check)

    if request.method == 'POST':
        edit_content = request.POST.get('content')
        edit_comment = Comment.objects.filter(commentid=comment_id).update(content=edit_content)

        url_redirect = '/topic/' + str(topic_id)
        return HttpResponseRedirect(url_redirect)

    
    return render(request, 'edit_comment.html', { 'select_topic' : select_topic, 
    'comment_topic' : comment_topic, 'user_like':user_like, 'zip_com_user':zip_com_user,
    'select_comment' : select_comment, 'time_create_topic' : time_create_topic})

def delete_comment(request, comment_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login")
    else:
        get_id_topic = Comment.objects.get(commentid=comment_id)
        select_topic = Topic.objects.get(title=get_id_topic.comtopicid)

        topic_id = select_topic.topicid
        delete_comment = Comment.objects.filter(commentid=comment_id).delete()
        
        url_redirect = '/topic/' + str(topic_id)
        return HttpResponseRedirect(url_redirect)

def like_topic(request, topic_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login")

    else:
        select_topic = Topic.objects.get(topicid=topic_id)
        create_user_like_topic = LikeTopic.objects.create(userid=request.user,like_topicid=select_topic)

        like_topic = Topic.objects.get(topicid=topic_id).like
        like_topic += 1

        increase_like_topic = Topic.objects.filter(topicid=topic_id).update(like=like_topic)

        url_redirect = '/topic/' + str(topic_id)
        return HttpResponseRedirect(url_redirect)



def unlike_topic(request, topic_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login")

    else:
        select_topic = Topic.objects.get(topicid=topic_id)
        delete_user_like_topic = LikeTopic.objects.get(userid=request.user,like_topicid=select_topic).delete()


        like_topic = Topic.objects.get(topicid=topic_id).like
        like_topic -= 1

        decrease_like_topic = Topic.objects.filter(topicid=topic_id).update(like=like_topic)

        url_redirect = '/topic/' + str(topic_id)
        return HttpResponseRedirect(url_redirect)

def like_comment(request, comment_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login")

    else:
        select_comment = Comment.objects.get(commentid=comment_id)
        get_id_topic = Comment.objects.get(commentid=comment_id)
        select_topic = Topic.objects.get(title=get_id_topic.comtopicid)

        topic_id = select_topic.topicid

        create_user_like_comment = LikeComment.objects.create(userid=request.user, 
                                                                like_commentid=select_comment, 
                                                                topicid=select_topic)

        
        like_comment = Comment.objects.get(commentid=comment_id).like
        like_comment += 1

        increase_like_topic = Comment.objects.filter(commentid=comment_id).update(like=like_comment)

        print(increase_like_topic)

        url_redirect = '/topic/' + str(topic_id)
        return HttpResponseRedirect(url_redirect)



def unlike_comment(request, comment_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login")

    else:
        select_comment = Comment.objects.get(commentid=comment_id)
        get_id_topic = Comment.objects.get(commentid=comment_id)
        select_topic = Topic.objects.get(title=get_id_topic.comtopicid)

        topic_id = select_topic.topicid

        delete_user_like_comment = LikeComment.objects.get(userid=request.user, 
                                                                like_commentid=select_comment, 
                                                                topicid=select_topic).delete()
        
        print(delete_user_like_comment)
        like_comment = Comment.objects.get(commentid=comment_id).like
        like_comment -= 1

        decrease_like_topic = Comment.objects.filter(commentid=comment_id).update(like=like_comment)

        url_redirect = '/topic/' + str(topic_id)
        return HttpResponseRedirect(url_redirect)


def show_tag(request, tag):

    topic_tag = Topic.objects.filter(tag__tag=tag)
    time_create_topic = Create.objects.filter(topicid__tag__tag=tag)

    zip_topic_user = zip(topic_tag,time_create_topic)

    return render(request, 'tag.html', {
        'topic_all': topic_tag , 
        'zip_topic_user' : zip_topic_user,
        'tag': tag
    })
