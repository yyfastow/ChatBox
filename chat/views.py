from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic import DetailView

from chat import models, forms


def friend_list(user):
    """returns a list of pk's of all the persons friends"""
    friends_list = user.split(',')
    print(friends_list)
    try:
        friends = [int(x) for x in friends_list]
        return friends
    except:
        return False


@login_required()
def chat_box_posts(request):
    """ the main page"""
    user = models.Profile.objects.get(username=request.user.username)
    friends = friend_list(user.friends)
    posts_list = models.Chat.objects.filter(distance_from_sourse=1).order_by("-time_posted")
    form = forms.ChatPostForm(request.POST, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = user
        post.save()
        messages.success(request, "Posted!")
    paginator = Paginator(posts_list, 40)  # Show 40 contacts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'chat/chatbox.html', {'user': user, 'friends': friends, 'posts': posts, 'form': form})


class ProfileDetailView(DetailView):
    model = models.Profile


@login_required
def friends(request):
    """returns all friends of a person"""
    user = models.Profile.objects.get(username=request.user.username)
    fri = friend_list(user.friends)
    if fri == False:
        messages.info(request, "Lets find some friends for you")
        return HttpResponseRedirect(reverse("chat:find_friends"))
    friends = models.Profile.objects.filter(pk__in=fri)
    return render(request, 'chat/friends.html', {'friends': friends})


@login_required
def find_friends(request):
    """ page to show all profiles or search fo pacific profile's"""
    search = request.GET.get("q")
    user = models.Profile.objects.get(username=request.user.username)
    old_friends = friend_list(user.friends)
    your_friends = None
    if search:
        friends = models.Profile.objects.filter(username__icontains=search)
        your_friends = models.Profile.objects.filter(pk__in=old_friends)
    else:
        friends = models.Profile.objects.exclude(pk__in=old_friends).exclude(pk=user.pk).order_by()
    return render(request, "chat/find_friends.html", {'friends': friends, 'user': user, 'your_friends': your_friends})


@login_required()
def request_friend(request):
    """request friends"""
    pk = request.GET.get('friend')
    print(pk)

    user = models.Profile.objects.get(email=request.user.email, username=request.user.username)
    to = models.Profile.objects.get(pk=pk)
    models.FriendMessage.objects.create(
        from_user=user.username,
        to_user=to,
        title="Friend Request"
    )
    messages.success(request, "Friend Request to {} sent!".format(to.username))
    if request.is_ajax():
        pass
    return HttpResponseRedirect(reverse('chat:find_friends'))


@login_required
def confirm_friend(request):
    """confirm friend request"""
    user = request.user
    pk = request.GET.get('message_pk')
    you = models.Profile.objects.get(username=user.username)
    message = models.FriendMessage.objects.get(pk=pk)
    friend = models.Profile.objects.get(username=message.from_user)
    you.friends = "{},{}".format(you.friends, friend.pk)
    friend.friends = "{},{}".format(friend.friends, you.pk)
    you.save()
    friend.save()
    message.delete(keep_parents=True)
    models.FriendMessage.objects.create(
        from_user=you.username,
        to_user=friend,
        title="Friend Accepted"
    )
    messages.success(request, "Friend Accepted!")
    return HttpResponseRedirect(reverse('chat:messages'))


@login_required
def like_unlike(request):
    """ likes and unlikes post"""
    user = models.Profile.objects.get(username=request.user.username)
    pk = request.POST.get('pk')
    post = models.Chat.objects.get(pk=pk)
    likes = friend_list(post.likes)
    if likes == False:
        post.amount_likes = 1
        post.likes = "0,{}".format(user.pk)
        post.save()
        print("he had no likes loser")
        flash_message = "First Liked!"
        messages.success(request, "First like! {}: ____ {} ".format(post.amount_likes, post.likes))
        return HttpResponseRedirect(reverse("chat:chat"))
    if user.pk in likes:
        # unlike
        post.amount_likes -= 1
        likes.remove(user.pk)
        post.likes = ",".join(str(x) for x in likes)
        post.save()
        flash_message = "unLiked!"
    else:
        # likes
        post.amount_likes += 1
        print(likes)
        post.likes += ",{}".format(user.pk)
        post.save()
        flash_message = "liked!"
    if request.is_ajax():
        return JsonResponse({
            'flash_message': flash_message,
            'likes': post.amount_likes,
            'post_pk': pk
        })
    else:
        messages.success(request, flash_message)
    return HttpResponseRedirect(reverse("chat:chat"))


@login_required()
def share(request):
    """ Shares post show friends of user could also see the post """
    user = models.Profile.objects.get(username=request.user.username)
    pk = request.POST.get('pk')
    post = models.Chat.objects.get(pk=pk)
    post.users.add(user)
    post.save()
    if request.is_ajax():
        return JsonResponse({
            'post_title': post.title, # needs to be post.title
            'post_pk': pk
        })
    else:
        messages.success(request, "Post Shared!")
    return HttpResponseRedirect(reverse("chat:chat"))


@login_required()
def message_seen(request):
    """deletes message """
    user = request.user
    pk = request.GET.get('message_pk')
    message = models.FriendMessage.objects.get(pk=pk)
    if message.to_user.username != user.username:
        messages.error(request, "YOU cant delete this message its not for you")
    else:
        message.delete(keep_parents=True)
        messages.success(request, "messages marked as seen adn deleted")
    return HttpResponseRedirect(reverse('chat:messages'))


@login_required()
def messages_list(request):
    user = models.Profile.objects.get(username=request.user.username)
    messages = models.FriendMessage.objects.filter(to_user=user.pk)
    return render(request, 'chat/messages.html', {'messages': messages})


@login_required()
def post_chat(request):
    user = models.Profile.objects.get(username=request.user.username)
    form = forms.ChatPostForm()
    if request.method == "POST":
        form = forms.ChatPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()
            messages.success(request, "New ChatBox posted")
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'chat/post_chat.html', {'form': form})


@login_required()
def fast_post(request):
    text = request.GET.get("text", "")
    user = models.Profile.objects.get(email=request.user.email)
    share = request.GET.get("share")
    print("IT went thorugh")
    models.Chat.objects.create(text=text, share="Public", title="Post", user=user)
    messages.success(request, "Posted!")
    return HttpResponseRedirect(reverse("chat:chat"))


@login_required()
def make_comments(request, pk):
    user = models.Profile.objects.get(username=request.user.username)
    post = get_object_or_404(models.Chat, pk=pk)
    form = forms.CommentForm()
    if request.method == "POST":
        form = forms.CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.share = "Public"
            comment.comment = post
            comment.distance_from_sourse = post.distance_from_sourse + 1
            comment.save()
            messages.success(request, "Comment added")
            return HttpResponseRedirect(reverse('home'))


@login_required()
def post_comment(request):
    """Posting comments"""
    user = models.Profile.objects.get(username=request.user.username)
    pk = request.POST.get("pk")
    post = get_object_or_404(models.Chat, pk=pk)
    form = forms.CommentForm(request.POST, request.FILES)
    # image = request.GET.get("image")
    # text = request.GET.get("text")
    comment = ""
    if form.is_valid():
        print("Form is valid")
        comment = form.save(commit=False)
        comment.user = user
        comment.share = "Public"
        comment.comment = post
        comment.distance_from_sourse = post.distance_from_sourse + 1
        comment.save()
        print("Comment is saved")
    if request.is_ajax():
        return JsonResponse({
            'pk': comment.pk,
            'comment': comment.text
        })
    # messages.error(request, "Comment need either a picture or a comment")
    return HttpResponseRedirect(reverse('home'))
