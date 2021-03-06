from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import *
from django.db.models import Q
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings


def Sendmailold(email, msg):
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    html = get_template("mail.html").render({"msg":msg})
    #html = "<h1>Email</h1>"
    sub = "Thank you For your Registration on Social on"
    send_mail(sub, " ", from_email, to_email, html_message=html)


def Front(request):
    if request.user.is_authenticated:
       return redirect("UserProfile",request.user.username)
    companies=""
    companies = Company_Model.objects.all()
    Dict= {
        "data":companies
    }
    return render(request,'index.html',Dict)


def Login(request):
    if request.user.is_authenticated:
       return redirect("UserProfile",request.user.username)
    form=AddUser_Form()
    error = False
    if request.method == "POST":
        un = request.POST["un"]
        ps =  request.POST["ps"]
        usr = authenticate(username=un,password=ps)
        if usr!=None:
            login(request,usr)
            return redirect("UserProfile",usr.username)
        error=True
    Dict={
        "error":error,"form":form
        }
    return render(request,'login_register.html',Dict)



def Register(request):
    if request.method == "POST":
        form = AddUser_Form(request.POST,request.FILES)
        if form.is_valid():
            data=form.save(commit=False)
            un=request.POST["un"]
            ps=request.POST["ps"]
            email=data.email
            usr=User.objects.create_user(un,email,ps)
            data.usr=usr
            data.save()
            msg = "Hi,{name}, Thank You for your interest in Social on Project,It is just learning purpose project".format(name=un)
            print(email)
            print(msg)
            Sendmailold(email,msg)
            return redirect('login')
            error = True
    return HttpResponse("Register Your Self")



def Logout(request):
    logout(request)
    return redirect("front")


def UserProfile(request,Username):
    if not request.user.is_authenticated:
        return redirect("login")
    usr = User.objects.filter(username=Username)
    if not usr:
        loggen_in_username=request.user.username
        return redirect('UserProfile',loggen_in_username)
    connection = None
    if request.user.username != Username:
        user1 = User.objects.get(username = Username)
        user2 = User.objects.get(username=request.user.username)
        UserData1 = UserDataBase.objects.get(usr = user1)
        UserData2 = UserDataBase.objects.get(usr = user2)
        connection = connections.objects.filter\
            (Q(sender=UserData1, receiver=UserData2) | Q(sender=UserData2, receiver=UserData1))
        if connection:
            connection = connection[0]
    Usr=usr[0]
    user_detail=UserDataBase.objects.get(usr=Usr)
    blog_form = UserBlog_Form()
    all_post = Blogs_Model.objects.filter(usr = Usr).order_by("-date")
    like_by_me_Ids = []
    all_likes_by_me = BlogLikes.objects.filter(usr=request.user)
    for i in all_likes_by_me:
        like_by_me_Ids.append(i.blog.id)
    Dict={
        "profile":user_detail,"connection":connection,"form":blog_form,"posts":all_post,"like_by_me_Ids":like_by_me_Ids
    }
    return render(request,"user_details.html",Dict)


def Update_User_Details(request, Username):
    if not request.user.is_authenticated:
        return redirect("login")

    loggen_in_username = request.user.username
    if Username != loggen_in_username:
        return redirect("UserProfile", loggen_in_username)

    usr = User.objects.filter(username=Username)
    Usr = usr[0]
    User_Detail = UserDataBase.objects.get(usr=Usr)

    form = Edit_User_Details(request.POST or None, request.FILES or None, instance=User_Detail)
    if form.is_valid():
        form.save()
        return redirect("UserProfile", loggen_in_username)

    Dict = {
        "Profile": User_Detail, "form":form
    }
    return render(request, "Update_User_Details.html", Dict)



def All_Profession(request, what):
    if not request.user.is_authenticated:
        return redirect("login")

    logged_in_user = User.objects.get(username = request.user.username)
    me = UserDataBase.objects.get(usr=logged_in_user)
    ###### Count Request Section #########
    con_request = connections.objects.filter(receiver=me, status="sent")
    con_sent = connections.objects.filter(sender=me, status="sent")
    con_friend = connections.objects.filter(Q(sender=me, status="friend") | Q(receiver=me, status="friend")).order_by( "-date")

    #-----X Count Request Section End ---X_------#
    data = ""
    if what == "all":
        data = UserDataBase.objects.all()
    if what == "myreceived":
        connection = connections.objects.filter(receiver=me, status = "sent")
        User_Data = []
        for c in connection:
            ud = UserDataBase.objects.get(id = c.sender.id)
            User_Data.append(ud)
        data = User_Data
    if what == "Sent":
        connection = connections.objects.filter(sender=me, status = "sent")
        User_Data = []
        for c in connection:
            ud = UserDataBase.objects.get(id=c.receiver.id)
            User_Data.append(ud)
        data = User_Data
    if what == "Friends":
        connection = connections.objects.filter(Q(sender=me, status = "friend") | Q(receiver=me, status = "friend")).order_by("-date")
        Data = []
        for c in connection:
            UserData = UserDataBase.objects.get(id = c.sender.id)
            if UserData.id != me.id:
                Data.append(UserData)

            UserData = UserDataBase.objects.get(id=c.receiver.id)
            if UserData.id != me.id:
                Data.append(UserData)
            data = Data
    Dict = {
        "all_users":data, "what":what, "con_request":con_request, "con_sent":con_sent,
        "con_friend":con_friend
    }
    return render(request, "professionals.html", Dict)



def Manage_your_connections(request,action,u_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if action == "Send_Request":
        senderUser=User.objects.get(username = request.user.username)
        sender = UserDataBase.objects.get(usr = senderUser)
        receiver = UserDataBase.objects.get(id = u_id)
        connections.objects.create(sender = sender,receiver = receiver)
        return redirect('UserProfile',receiver.usr.username)
    if action == "Accept_Request" or action == "Reject_Request":
        ReceiverUser = User.objects.get(username=request.user.username)
        receiver = UserDataBase.objects.get(usr=ReceiverUser)
        sender = UserDataBase.objects.get(id=u_id)
        connection = connections.objects.filter(sender=sender, receiver=receiver)
        if connection:
            for c in connection:
                if action == "Accept_Request":
                    c.status = "friend"
                    c.save()
                if action == "Reject_Request":
                    c.status = "rejected"
        return redirect("professional", "all")
    return HttpResponse("you want" + str(action) +"for user" + str(u_id))


def Add_Company(request):
    if not request.user.is_authenticated:
        return redirect("login")
    form = StartCompany_Form()
    if request.method == "POST":
        form = StartCompany_Form(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            Map = data.map_embad
            if 'width="600"' in Map:
                Map = Map.split('width="600"')
                Map.insert(1, 'width="100%"')
                Map = " ".join(Map)
                data.map_embad = Map
            data.usr = request.user
            data.save()
            return redirect("login")
    Dict = {
        "form":form
    }
    return render(request, "add_company.html", Dict)

def Companies(request):
    if not request.user.is_authenticated:
        return redirect("login")
    companies = Company_Model.objects.all()
    Dict = {
        "companies":companies
    }
    return render(request,"companies.html",Dict)


def CompanyDetails(request,c_id):
    if not request.user.is_authenticated:
        return redirect("login")

    company = Company_Model.objects.get(id = c_id)
    if not company:
        return redirect("companies")
    print(company)
    Dict = {
        "company":company
    }
    return render(request, "companies_detail.html",Dict)


def NewPost(request):
    if request.method == "POST":
        form = UserBlog_Form(request.POST)
        if form.is_valid():
            data = form.save(commit = False)
            data.usr = request.user
            data.save()
            print("Blog Submitted...@")
    return redirect("login")


def Like_By_Me(request, b_id, Username):
    if not request.user.is_authenticated:
        return redirect("login")
    blog = Blogs_Model.objects.get(id=b_id)
    BlogLikes.objects.create(usr=request.user, blog=blog)
    return redirect("UserProfile", Username)

def Contact(request):
    return render(request,"contact.html")