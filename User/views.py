from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, Experience, Education
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from datetime import date
from django.http import JsonResponse
from feed.models import Post, Like, Comment
from User.models import ConnectionRequest, Connection
from django.db.models import Q  
from .helper_functions import find_connection_posts, find_connection_userprofiles, find_liked_posts, find_child_comments, find_parent_comments
# Create your views here.
def login_page(request):
    return render(request, 'login.html')

def landing_page(request):
    return render(request, 'landing_page.html')

def signup_page(request):
    return render(request, 'signup.html')

def create_account(request):
    if request.method == "POST":
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        full_name = f"{first_name} {last_name}"

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("signup") 

        if UserProfile.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number is already registered.")
            return redirect("signup")

        user = User.objects.create_user(
            username=email,
            password=password,
        )

        UserProfile.objects.create(
            user=user,
            full_name=full_name,
            phone=phone
        )

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")  

    return render(request, "signup.html")

def signin(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        username = request.POST.get('email')
        password = request.POST.get('password')
        email = username
        if username.isdigit():
            phone_list = list(UserProfile.objects.filter(phone=username))
            if phone_list == []:
                messages.error(request, "Invalid username or password")
                return redirect('login')
            else:
                email = phone_list[0].user.username
        
        user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)  
        return redirect("home")
    else:
        messages.error(request, "Invalid username or password")
        return redirect('login')

def home(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    posts = find_connection_posts(request.user)
    parent_comments_map = {}
    for post in posts:
        parent_comments = find_parent_comments(post)
        parent_comments_map[post.id] = parent_comments
    liked_posts = find_liked_posts(request.user)
    child_comments_map = {}
    for parent_comment_list in parent_comments_map.values():
        for parent_comment in parent_comment_list:
            child_comments = parent_comment.replies.all().order_by('created_at')
            child_comments_map[parent_comment.id] = child_comments
    print("child_comments_map:", child_comments_map)
    context = {'user_profile': user_profile, 'posts': posts, 'liked_posts': liked_posts, 'parent_comments_map': parent_comments_map, 'child_comments_map': child_comments_map}
    return render(request, 'home.html', context)  

def add_comment(request):
    if request.POST.get("comment_type") == "parent":
        content = request.POST.get("content")
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        user_profile = get_object_or_404(UserProfile, user=request.user)
        Comment.objects.create(
            user=user_profile,
            post=post,
            content=content
        )
        return redirect("home")
    else:
        content = request.POST.get("content")
        post_id = request.POST.get("post_id")
        parent_id = request.POST.get("parent_id")
        post = get_object_or_404(Post, id=post_id)
        parent_comment = get_object_or_404(Comment, id=parent_id)
        user_profile = get_object_or_404(UserProfile, user=request.user)
        Comment.objects.create(
            user=user_profile,
            post=post,
            content=content,
            parent=parent_comment
        )
        return redirect("home")
    return redirect("home")





def profile(request):
    user_profile = request.user.userprofile
    experience_list = Experience.objects.filter(userprofile=user_profile)
    education_list = Education.objects.filter(userprofile=user_profile)
    context = {'experience_list': experience_list, 'education_list': education_list, 'user_profile': user_profile}
    return render(request, 'profile_page.html', context)

@login_required
def add_experience(request):
    try:
        userprofile = request.user.userprofile  
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect("profile")  

    if request.method == "POST":
        title = request.POST.get("title")
        employment_type = request.POST.get("employmentType")
        company = request.POST.get("company")
        is_current = request.POST.get("currentRole") == "on"
        start_month = request.POST.get("startMonth")
        start_year = request.POST.get("startYearExp")
        end_month = request.POST.get("endMonth")
        end_year = request.POST.get("endYearExp")
        location = request.POST.get("location")
        location_type = request.POST.get("locationType")
        description = request.POST.get("description")
        headline = request.POST.get("headline")  
        # Basic validation
        if not title or not company or not start_month or not start_year:
            messages.error(request, "Please fill all required fields (Title, Company, Start Date).")
            return redirect("add_experience")  # replace with your URL

        # Convert start date
        start_date = date(int(start_year), int(start_month), 1)

        # Convert end date if not current
        if not is_current and end_month and end_year:
            end_date = date(int(end_year), int(end_month), 1)
        else:
            end_date = None

        # Save experience
        Experience.objects.create(
            userprofile=userprofile,
            title=title,
            employment_type=employment_type,
            company=company,
            is_current=is_current,
            start_date=start_date,
            end_date=end_date,
            location=location,
            location_type=location_type,
            description=description
        )

        # Optional: update profile headline
        if headline:
            userprofile.headline = headline
            userprofile.save()

        messages.success(request, "Experience added successfully!")
        return redirect("profile")  # replace with profile URL
    return redirect("profile")  




def add_education(request):
    if request.method == "POST":
        # get the logged-in user's profile
        userprofile = request.user.userprofile  

        # extract form fields
        school = request.POST.get("school")
        degree = request.POST.get("degree")
        field_of_study = request.POST.get("field")
        grade = request.POST.get("grade")
        description = request.POST.get("description")

        # start date (month + year → date object, default to 1st of month)
        start_month = int(request.POST.get("startMonth"))
        start_year = int(request.POST.get("startYearEdu"))
        start_date = date(start_year, start_month, 1)

        # end date (can be empty → None)
        end_month = request.POST.get("endMonth")
        end_year = request.POST.get("endYearEdu")
        end_date = None
        if end_month and end_year:
            end_date = date(int(end_year), int(end_month), 1)

        # create and save Education entry
        Education.objects.create(
            userprofile=userprofile,
            school=school,
            degree=degree,
            field_of_study=field_of_study,
            start_date=start_date,
            end_date=end_date,
            grade=grade,
            description=description
        )

        return redirect("profile") 

def education_detail(request, id):
    edu = Education.objects.get(id=id)
    return JsonResponse({
        "id": edu.id,
        "school": edu.school,
        "degree": edu.degree,
        "field_of_study": edu.field_of_study,
        "grade": edu.grade,
        "description": edu.description,
        "start_date": edu.start_date,
        "end_date": edu.end_date,
    })

def experience_detail(request, id):
    user_profile_obj = request.user.userprofile
    profile_headline = user_profile_obj.headline
    try:
        exp = Experience.objects.get(id=id)
        return JsonResponse({
            "id": exp.id,
            "title": exp.title,
            "employment_type": exp.employment_type,
            "company": exp.company,
            "is_current": exp.is_current,
            "start_date": exp.start_date,
            "end_date": exp.end_date,
            "location": exp.location,
            "location_type": exp.location_type,
            "description": exp.description,
            "duration": exp.duration(),
            "profile_headline": profile_headline,
        })
    except Experience.DoesNotExist:
        return JsonResponse({"error": "Experience not found"}, status=404)

def userprofile_detail(request, id):
    try:
        profile = UserProfile.objects.get(id=id)
        return JsonResponse({
            "id": profile.id,
            "full_name": profile.full_name,
            "headline": profile.headline,
            "location": profile.location,
            "summary": profile.summary,
            # "profile_photo": profile.profile_photo.url if profile.profile_photo else None,
            "phone": profile.phone,
            # "background_photo": profile.background_photo.url if profile.background_photo else None,

        })
    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "UserProfile not found"}, status=404)


def update_profile(request, id):
    userprofile = get_object_or_404(UserProfile, id=id)
    print("bitib4vtijnnjirnjr")
    print(id)
    if request.method == "POST":
        userprofile.full_name = request.POST.get("full_name")
        userprofile.headline = request.POST.get("headline")
        userprofile.location = request.POST.get("location")
        userprofile.phone = request.POST.get("phone")
        userprofile.summary = request.POST.get("summary")

        userprofile.save()
        return redirect("profile")

    return JsonResponse({"error": "Invalid request"}, status=400)

def update_profile_photo(request):
    if request.method == "POST" and request.FILES.get("profile_photo"):
        profile = get_object_or_404(UserProfile, user=request.user)
        profile.profile_photo = request.FILES["profile_photo"]
        profile.save()
        return redirect("profile")
    return redirect("profile")

def update_cover_photo(request):
    if request.method == "POST" and request.FILES.get("cover_photo"):
        profile = get_object_or_404(UserProfile, user=request.user)
        profile.background_photo = request.FILES["cover_photo"]
        profile.save()
        return redirect("profile")
    return redirect("profile")

def update_experience(request, id):
    experience_obj = Experience.objects.get(id=id)
    user_profile_obj = request.user.userprofile
    if request.method == "POST":
        experience_obj.title = request.POST.get("title")
        experience_obj.company = request.POST.get("company")
        experience_obj.employment_type = request.POST.get("employment_type")
        experience_obj.is_current = True if request.POST.get("is_current") == "on" else False
        experience_obj.location = request.POST.get("location")
        experience_obj.location_type = request.POST.get("location_type")
        experience_obj.description = request.POST.get("description")
        user_profile_obj.headline = request.POST.get("headline")

        start_month = request.POST.get("start_month")
        start_year = request.POST.get("start_year")
        if start_month and start_year:
            experience_obj.start_date = date(int(start_year), int(start_month), 1)

        if experience_obj.is_current:
            experience_obj.end_date = None
        else:
            end_month = request.POST.get("end_month")
            end_year = request.POST.get("end_year")
            if end_month and end_year:
                experience_obj.end_date = date(int(end_year), int(end_month), 1)
            else:
                experience_obj.end_date = None

        experience_obj.save()
        user_profile_obj.save()
        return redirect("profile")

    return redirect("profile")

@login_required
def update_education(request, id):
    # Get the education object for the logged-in user
    print("edaedaedaedaedaedaaaaaa")
    edu_obj = get_object_or_404(Education, id=id, userprofile=request.user.userprofile)

    if request.method == "POST":
        # Fetch values from form
        edu_obj.school = request.POST.get("school")
        edu_obj.degree = request.POST.get("degree")
        edu_obj.field_of_study = request.POST.get("field")
        edu_obj.grade = request.POST.get("grade")
        edu_obj.description = request.POST.get("description")

        # Start date
        start_month = request.POST.get("start_month")
        start_year = request.POST.get("start_year")
        if start_month and start_year:
            edu_obj.start_date = date(int(start_year), int(start_month), 1)

        # End date
        end_month = request.POST.get("end_month")
        end_year = request.POST.get("end_year")
        print(start_year, end_year)
        is_current = request.POST.get("is_current")  # checkbox value
        if is_current == "on":
            edu_obj.end_date = None
        elif end_month and end_year:
            edu_obj.end_date = date(int(end_year), int(end_month), 1)
        else:
            edu_obj.end_date = None

        # Save updated object
        edu_obj.save()

        # Redirect to profile page (adjust URL pattern as needed)
        return redirect("profile")

def view_profile(request, id):
    my_profile = request.user.userprofile
    user_profile = UserProfile.objects.get(id=id)
    experience_list = Experience.objects.filter(userprofile=user_profile)
    education_list = Education.objects.filter(userprofile=user_profile)
    context = {'experience_list': experience_list, 'education_list': education_list, 'user_profile': user_profile, 'my_profile': my_profile }
    return render(request, 'view_profile.html', context)