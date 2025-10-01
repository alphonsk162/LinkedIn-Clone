from feed.models import Post, Like, Comment
from User.models import ConnectionRequest, Connection, UserProfile
from django.db.models import Q  

def find_connection_userprofiles(user):
    connections = Connection.objects.filter(
        Q(user1=user) | Q(user2=user))
    connected_users = []
    for connection in connections:
        if connection.user1 == user:
            connected_users.append(connection.user2)
        else:
            connected_users.append(connection.user1)
    return connected_users

def find_connection_posts(user):
    connected_users = find_connection_userprofiles(user)
    posts = Post.objects.filter(user__user__in=connected_users).order_by('-created_at')
    return posts

def find_liked_posts(user):
    liked_objs = Like.objects.filter(user=user.userprofile)
    liked_posts = []
    for obj in liked_objs:
        liked_posts.append(obj.post)
    return liked_posts

def find_parent_comments(post_obj):
    return Comment.objects.filter(post=post_obj, parent__isnull=True).order_by('-created_at')



def find_child_comments(parent_comments):
    child_comments_dict = {}
    child_comments = Comment.objects.filter(parent__isnull=False)
    for parent_comment in parent_comments:
        child_comments_dict[parent_comment] = []
    for child_comment in child_comments:
        if child_comment.parent in child_comments_dict:
            child_comments_dict[child_comment.parent].append(child_comment)
    return child_comments_dict