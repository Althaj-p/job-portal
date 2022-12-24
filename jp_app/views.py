from django.contrib.auth import authenticate, login, logout
from django.core.handlers import exception
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.db.models import Q



# Create your views here.
def index(request):
    return render(request, 'index.html')


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'admin_home.html')


def view_user(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = StudentUser.objects.all()
    d = {'data': data}
    return render(request, 'view_users.html', d)


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        use = authenticate(username=u, password=p)
        try:

            if use.is_staff:
                login(request, use)

                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"

    d = {'error': error}

    return render(request, 'admin_login.html', d)


def user_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                if user1.type == "student":
                    login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error': error}

    return render(request, 'user_login.html', d)


def recruiter_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "recruiter" and user1.status != "pending":
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error': error}
    return render(request, 'recruter_login.html', d)


def recruiter_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        e = request.POST['email']
        p = request.POST['pwd']
        gen = request.POST['gender']
        i = request.FILES['image']
        c = request.POST['company']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, password=p, username=e)
            Recruiter.objects.create(user=user, mobile=con, image=i, gender=gen, company=c, type="recruiter",
                                     status="pending")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'recruiter_signup.html', d)


def user_home(request):
    if 'q' in request.GET:
        q=request.GET['q']
        multiple_q=Q(Q(title__icontains=q) |Q(location__icontains=q)|Q(skills__icontains=q)|Q(salary__icontains=q))
        data=Job.objects.filter(multiple_q)
    else:
        data=Job.objects.all()
    return render(request,'user_home.html',{'data':data})


    # if q == "":
    #     return redirect(request.META.get('HTTP_REFERER'))
    # else:
        # if data:
        #     return render(request,'search.html',{'data':data})
        # else:
        #     messages.info(request,'search result for '+q+' not found')
    # return render(request,'user_home.html',{'data':data})
    
    # data=Job.objects.all()
    # return render(request,'user_home.html',{'data':data})


def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        # e = request.POST['email']
        # p = request.POST['pwd']
        gen = request.POST['gender']
        # i = request.FILES['image']
        # c = request.POST['company']

        recruiter.user.first_name=f
        recruiter.user.last_name = l
        recruiter.mobile = con
        recruiter.gender = gen
        try:
           recruiter.save()
           recruiter.user.save()
           error = "no"
        except:
            error = "yes"

    d = {'recruiter': recruiter,'error': error}
    return render(request, 'Recruiter_home.html',d)


def change_status(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    data = Recruiter.objects.get(id=pid)
    if request.method == 'POST':
        s = request.POST['status']
        data.status = s
        try:
            data.save()
            error = "no"
        except:
            error = "yes"
    d = {'data': data, 'error': error}
    return render(request, 'change_status.html', d)


def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == 'POST':
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'change_passwordadmin.html', d)


def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == 'POST':
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'change_passworduser.html', d)


def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == 'POST':
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'change_passwordrecruiter.html', d)


def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='pending')
    d = {'data': data}
    return render(request, 'recruiter_pending.html', d)


def add_job(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == 'POST':
        jt = request.POST['jobtitle']
        sd = request.POST['startdate']
        ed = request.POST['enddate']
        sal = request.POST['salary']
        l = request.FILES['logo']
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']
        a = request.user
        recruiter = Recruiter.objects.get(user=a)

        # job=Job.objects.filter(recruiter=recruiter)
        try:

            Job.objects.create( recruiter=recruiter,start_date=sd, end_date=ed, title=jt, salary=sal, image=l, description=des, experience=exp, location=loc, skills=skills, creationdate=date.today())
            # if form.is_valid():
            #     instance=form.save(commit=False)
            #     instance.recruiter=request.user
            error = "no"
        except:
        # except exception as e:
        #     print(e)
            error = "yes"
    d = {'error': error}

    return render(request,'add_job.html', d)


def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    job=Job.objects.filter(recruiter=recruiter)
    d= {'job':job }    
    return render(request, 'job_list.html',d)

def home_joblist(request):
    # if not request.user.is_authenticated:
    #     return redirect('recruiter_login')
    # user=request.user
    # recruiter=Recruiter.objects.get(user=user)
    # job=Job.objects.filter(recruiter=recruiter)
    job=Job.objects.all().order_by('-start_date')

    d= {'job':job }
    return render(request, 'home_joblist.html',d)
def user_joblist(request):
    # if not request.user.is_authenticated:
    #     return redirect('recruiter_login')
    # user=request.user
    # recruiter=Recruiter.objects.get(user=user)
    # job=Job.objects.filter(recruiter=recruiter)
    job=Job.objects.all()
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for i in data:
        li.append(i.job.id)



    d= {'job':job,'li':li }
    return render(request, 'user_joblist.html',d)

def job_detail(request,pid):
    job=Job.objects.get(id=pid)
    data=wishlist.objects.filter(user=request.user)
    li=[]
    for i in data:
        li.append(i.job.id)


    d= {'job':job,'li':li }
    return render(request, 'job_detail.html',d)

def recruiters_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.all()
    d = {'data': data}
    return render(request, 'recruiters_all.html', d)


def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Reject')
    d = {'data': data}
    return render(request, 'recruiter_rejected.html', d)


def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Accept')
    d = {'data': data}
    return render(request, 'recruiter_accepted.html', d)


def delete_user(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    del_id = User.objects.get(id=pid)
    del_id.delete()
    return redirect('view_user')


def delete_recruiter(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    del_id = User.objects.get(id=pid)  # User enn kodthal Usernn pokum allenkil Recruiternn mathre poku
    del_id.delete()
    return redirect('recruiters_all')


def user_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        e = request.POST['email']
        p = request.POST['pwd']
        gen = request.POST['gender']
        i = request.FILES['image']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, password=p, username=e)
            StudentUser.objects.create(user=user, mobile=con, image=i, gender=gen, type="student")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'user_signup.html', d)


def Logout(request):
    logout(request)
    return redirect('index')


def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    job=Job.objects.get(id=pid)
    if request.method == 'POST':
        jt = request.POST['jobtitle']
        sd = request.POST['startdate']
        ed = request.POST['enddate']
        sal = request.POST['salary']
        # l = request.FILES['logo']
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']


        job.title=jt
        job.salary = sal
        job.experience =exp
        job.location = loc
        job.skills = skills
        job.description = des

        # job=Job.objects.filter(recruiter=recruiter)
        try:
            job.save()

            error = "no"
        except:
            error = "yes"
        if sd:
            try:
              job.start_date=sd
              job.save()
            except:
                pass
        else:
            pass
        if ed:
            try:
              job.end_date=ed
              job.save()
            except:
                pass
        else:
            pass

    d = {'error': error,'job':job}

    return render(request,'edit_jobdetail.html', d)

def edit_companylogo(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    job=Job.objects.get(id=pid)
    if request.method == 'POST':
        cl = request.FILES['logo']



        job.image=cl

        try:
            job.save()

            error = "no"
        except:
            error = "yes"


    d = {'error': error,'job':job}

    return render(request,'edit_companylogo.html', d)

def apply_job(request,id):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    user=request.user
    student=StudentUser.objects.get(user=user)
    job=Job.objects.get(id=id)
    date1=date.today()
    if job.end_date < date1:
        error="close"
    elif job.start_date > date1:
        error="not open"
    else:
        if request.method=='POST':
            r=request.FILES['resume']
            obj=Apply.objects.create(job=job,student=student,resume=r,applydate=date.today())
            obj.save()
            error="done"
    d={'error':error}
    return render(request,'apply_job.html',d)
def candidate_applied(request):
    user=request.user.id
    data=Apply.objects.filter(job__recruiter__user__id=user)
    return render(request,'candidate_applied.html ',{'data':data})


def user_appliedjobs(request):
    user=request.user
    data=Apply.objects.filter(student__user=user)
    return render(request,'user_appliedjobs.html',{'data':data})


def delete_application(request,id):
    obj=Apply.objects.get(id=id)
    obj.delete()
    return redirect('user_appliedjobs')

def contact(request):
    if request.method=='POST':
        email=request.POST['email'] 
        subject=request.POST['subject']       
        message=request.POST['message']
        send_mail(subject,message,settings.EMAIL_HOST_USER,[email],fail_silently=False)
        messages.success(request,'Email send successfully')

    return render(request,'contact.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    student = StudentUser.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        # e = request.POST['email']
        # p = request.POST['pwd']
        gen = request.POST['gender']
        # i = request.FILES['image']
        # c = request.POST['company']

        student.user.first_name = f
        student.user.last_name = l
        student.mobile = con
        student.gender = gen
        try:
            student.save()
            student.user.save()
            error = "no"
        except:
            error = "yes"

    d = {'student': student, 'error': error}
    return render(request, 'profile.html',d)

def addWishlist(request,id):
    job=Job.objects.get(id=id)
    # if job.id in wishlist:

    obj=wishlist.objects.create(user=request.user,job=job,created_at=date.today())
    obj.save()
    return redirect('wishlist')


def all_wishlist(request):
    obj=wishlist.objects.filter(user=request.user)
    return render(request,'wishlist.html',{'data':obj})

def deleteWishlist(request,id):
    user=request.user
    job=Job.objects.get(id=id)
    obj=wishlist.objects.filter(user=user,job=job)
    obj.delete()
    return redirect('wishlist')
def delete_savedjob(request,id):
    obj=wishlist.objects.get(id=id)
    obj.delete()
    return redirect('wishlist')


def search(request):
    # if 'q' in request.GET:
    q=request.GET['q']
    if q == "":
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        multiple_q=Q(Q(title__icontains=q) |Q(location__icontains=q)|Q(skills__icontains=q)|Q(salary__icontains=q))
        data=Job.objects.filter(multiple_q)
        if data:
            return render(request,'search.html',{'data':data})
        else:
            messages.info(request,'search result for '+q+' not found')
    return render(request,'search.html',{'data':data})
