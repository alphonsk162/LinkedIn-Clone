from django.shortcuts import render, redirect
from User.models import UserProfile, Experience, Education, ConnectionRequest, Connection
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Post, Like, Comment
from User.helper_functions import find_connection_posts, find_connection_userprofiles, find_liked_posts, find_child_comments, find_parent_comments



# Create your views here.


def search_results(request):
    user_profile = request.user.userprofile
    search_input = request.POST.get('search_input')
    search_results = UserProfile.objects.filter(full_name__icontains=search_input)
    received_requests = ConnectionRequest.objects.filter(receiver=request.user)
    senders = [req.sender for req in received_requests]
    sent_requests = ConnectionRequest.objects.filter(sender = request.user)
    receivers = [req.receiver for req in sent_requests]
    connection_objs = Connection.objects.filter(
    Q(user1=request.user) | Q(user2=request.user))
    connections = []
    for connection_obj in connection_objs:
        if connection_obj.user1 == request.user:
            connections.append(connection_obj.user2)
        else:
            connections.append(connection_obj.user1)
    print(search_results)
    print(received_requests)
    print(sent_requests)
    print(connections)
    context = {'search_results': search_results, 'request_receivers': receivers, 'request_senders': senders, 'connections':connections}
    return render(request, 'search_results.html', context)

@login_required
def create_connection_request(request, id):
    print(request.user)
    print(id)
    if request.method == "POST":
        sender = request.user
        receiver_userprofile_obj = UserProfile.objects.get(id=id)
        receiver = receiver_userprofile_obj.user

        # prevent self-request
        if sender == receiver:
            return JsonResponse({"success": False, "message": "You cannot connect with yourself."}, status=400)

        # check if already exists
        conn_req, created = ConnectionRequest.objects.get_or_create(
            sender=sender,
            receiver=receiver,
        )

        if not created:
            return JsonResponse({"success": False, "message": "Request already sent."}, status=400)

        return JsonResponse({"success": True, "message": "Connection request sent."})

    return JsonResponse({"success": False, "message": "Invalid request."}, status=400)

@login_required
def delete_connection_request(request, receiver_id):
    receiver_userprofile = UserProfile.objects.get(id=receiver_id)
    receiver_id = receiver_userprofile.user.id
    if request.method == "POST":
        try:
            conn_req = ConnectionRequest.objects.get(
                Q(sender=request.user, receiver_id=receiver_id) |
                Q(sender_id=receiver_id, receiver=request.user)
            )
            conn_req.delete()
            return JsonResponse({"success": True})
        except ConnectionRequest.DoesNotExist:
            return JsonResponse({"success": False, "error": "Connection request does not exist"})
    return JsonResponse({"success": False, "error": "Invalid request"})

@login_required
def accept_connection_request(request):
    if request.method == "POST":
        sender_profile_id = request.POST.get("sender_id")  
        sender_profile = get_object_or_404(UserProfile, id=sender_profile_id)
        sender = sender_profile.user
        receiver = request.user  
        conn_request = get_object_or_404(ConnectionRequest, sender=sender, receiver=receiver, is_accepted=False, is_rejected=False)
        Connection.objects.get_or_create(user1=sender, user2=receiver)
        conn_request.delete()

        return JsonResponse({"status": "success", "message": "Connection accepted"})
    
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@login_required
def create_post(request):
    print("postpostpost")
    if request.method == "POST":
        content = request.POST.get("content")
        image = request.FILES.get("image")

        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return redirect("profile_setup")

        # Save post
        Post.objects.create(
            user=user_profile,
            content=content,
            image=image
        )

        return redirect("home")  

    return redirect("home")

@login_required
def toggle_like_post(request):
    print("pppppppppppppppppppppppppppppppppppppp")
    post_id = request.POST.get("postId")
    post = get_object_or_404(Post, id=post_id)

    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Check if user already liked the post
    like, created = Like.objects.get_or_create(user=user_profile, post=post)

    if not created:
        # If like already exists, unlike (delete it)
        like.delete()
        status = "unliked"
    else:
        status = "liked"

    return JsonResponse({
        "status": status,
        "postId": post_id,
        "likes_count": Like.objects.filter(post=post).count()
    })


def comment_page(request):
        return render(request, "comments_page.html")



