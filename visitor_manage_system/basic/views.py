from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
import datetime
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm

# @login_required(login_url='/')
def index(request):
    visitor = VisitDetails.objects.all().order_by('-visit_id')
    return render(request,'basic/dashboard.html',{'visitor':visitor,'k':True})





@unauthenticated_user
def handleSignup(request):
    form=createuserform()

    if request.method=='POST':
        form=createuserform(request.POST)
        if form.is_valid():
            form.save()
            
    context={'form':form}
    return render (request,'basic/dashboard.html',context)

@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin'])
def host(request):
    host =Host.objects.all().order_by('host_id')
    count = host.count()
    return render(request,'basic/host.html',{'host':host,'count':count,'k':False})
# def hostdynamic(request,pk):
#     host1 = Host.objects.get(host_id=pk)
#     return render(request,'basic/hostdynamic.html',{'host':host1,'k':False})




@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin'])
def createhost(request):
    form = HostForm()
    if request.method == 'POST':
        form = HostForm(request.POST)
        if form.is_valid():
            form.save()
            host =Host.objects.all().order_by('host_id')
            count = host.count()
            return render(request,'basic/host.html',{'host':host,'count':count})
    context={'form':form,'k':False}
    return render(request,'basic/create_host.html',context)
# @admin_only
@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin'])
def updateHost(request,pk):
    host = Host.objects.get(host_id=pk)
    form = HostForm(instance=host)
    if request.method == 'POST':
        form = HostForm(request.POST,instance=host)
        if form.is_valid():
            form.save()
            host =Host.objects.all().order_by('host_id')
            count = host.count()
            return render(request,'basic/host.html',{'host':host,'count':count,'k':False})    
    context={'form':form,'k':False}
    return render(request,'basic/create_host.html',context)

@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin'])
def deleteHost(request,pk):
    host = Host.objects.get(host_id=pk)
    if request.method == "POST":
        host.delete()
        host =Host.objects.all().order_by('host_id')
        count = host.count()
        return render(request,'basic/host.html',{'host':host,'count':count,'k':False})
    return render(request,'basic/delete_host.html',{'form':host,'k':False})



@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin','entryperson'])
def visitor(request):
    visitor = Visitor.objects.all().order_by('-visitor_id')
    return render(request,'basic/visitor.html',{'visitor':visitor,'k':False})

@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin','entryperson'])
def createvisitor(request):
    form = VisitorForm()
    if request.method == 'POST':
        form = VisitorForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            visitor = Visitor.objects.all().order_by('-visitor_id')
            return render(request,'basic/visitor.html',{'visitor':visitor,'k':False}) 
    context={'form':form,'k':False}
    return render(request,'basic/create_visitor.html',context)

@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin','entryperson'])
def updatevisitor(request,pk):
    visitor = Visitor.objects.get(visitor_id=pk)
    form = VisitorForm(instance=visitor)
    if request.method == 'POST':
        form = VisitorForm(request.POST,request.FILES,instance=visitor)
        if form.is_valid():
            form.save()
            visitor = Visitor.objects.all().order_by('-visitor_id')
            return render(request,'basic/visitor.html',{'visitor':visitor,'k':False})
    context={'form':form,'k':False}
    return render(request,'basic/create_visitor.html',context)

@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin'])
def deletevisitor(request,pk):
    visitor = Visitor.objects.get(visitor_id=pk)
    if request.method == "POST":
        visitor.delete()
        visitor = Visitor.objects.all().order_by('-visitor_id')
        return render(request,'basic/visitor.html',{'visitor':visitor,'k':False})
    return render(request,'basic/delete_visitor.html',{'form':visitor,'k':False}) 




@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin'])
def events(request):
    complete =0
    event = Event.objects.all()
    upcomming = event.count()
    for i in event:
        a = i.tag
        if a == 'Complete':
            complete +=1
            i.option1 = True
            i.option2 = False
        else:
            i.option1 = False
            i.option2 = True
    upcomming = upcomming - complete
    return render(request,'basic/events.html',{'form':event,'complete':complete,'upcomming':upcomming})

@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin','host'])
def createevent(request):
    form =EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            complete =0
            event = Event.objects.all()
            upcomming = event.count()
            for i in event:
                a = i.tag
                if a == 'Complete':
                    complete +=1
                    i.option1 = True
                    i.option2 = False
                else:
                    i.option1 = False
                    i.option2 = True
            upcomming = upcomming - complete
            return render(request,'basic/events.html',{'form':event,'complete':complete,'upcomming':upcomming})
    return render(request,'basic/create_event.html',{'form':form,'k':False})

@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin','host'])
def updateevent(request,pk):
    event = Event.objects.get(event_id=pk)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST,instance=event)
        if form.is_valid():
            form.save()
            event = Event.objects.all()
            return render(request,'basic/events.html',{'form':event,'k':False})
    context={'form':form,'k':False}
    return render(request,'basic/create_event.html',context)
@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin','host'])
def deleteevent(request,pk):
    event = Event.objects.get(event_id=pk)
    if request.method == "POST":
        event.delete()
        event = Event.objects.all()
        return render(request,'basic/events.html',{'form':event,'k':False})
    return render(request,'basic/delete_event.html',{'form':event,'k':False}) 





@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin','entryperson'])
def visitdetails(request):
    form = VisitDetailsForm()
    visitdetail = VisitDetails.objects.all()
    count = visitdetail.count()
    date_object = datetime.date.today()
    date_object = str(date_object)
    count = 0
    for i in visitdetail:
        a = i.visit_date
        day = a.day
        month = a.month
        year = a.year
        if day <10:
            day = str(0)+str(day)
        if month<10:
            month = str(0)+str(month)
        date1 = str(year)+str('-')+str(month)+str('-')+str(day)
        if date_object == date1:
            count =count +1
    if request.method == 'POST':
        a = request.POST
        a1=a['duration']
        a2=a['purpose']
        a3=a['visit_detail']
        a4=a['flat_no']
        a3 = Visitor.objects.get(visitor_id=a3)
        visitdetails = VisitDetails(duration=a1,purpose=a2,visit_detail=a3,flat_no=a4)
        visitdetails.save()
        # messages.success(request,"visit entered successfull")
        return redirect('/')
    context={'form':form,'count':count,'k':False}
    return render(request,'basic/visitdetails.html',context)




@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin','entryperson'])
def eventvisitor(request):
    form =EventVisitorForm()
    if request.method == 'POST':
        form = EventVisitorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Event guest  entered successfull")
            form =EventVisitorForm()
            return render(request,'basic/eventvisitor.html',{'form':form,'k':False})
    return render(request,'basic/eventvisitor.html',{'form':form,'k':False})


@unauthenticated_user
def handlelogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password=password)
        if user is not None:
            login(request,user)
            group = request.user.groups.all()[0].name
            if group == 'host':
                return redirect('/user')
            if group is not 'host':
                return redirect('/')

        else:
            messages.error(request,'Creadential wrond')
            visitor = VisitDetails.objects.all().order_by('-visit_id')
            return render(request,'basic/dashboard.html',{'visitor':visitor,'k':True})
    visitor = VisitDetails.objects.all().order_by('-visit_id')
    return render(request,'basic/dashboard.html',{'visitor':visitor,'k':True})

def handlelogout(request):
    logout(request)
    return redirect('/')
        

@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin','host'])
def userpage(request):
    a = request.user
    try:
        host = Host.objects.get(user=a)
    except:
        host = None
    if host is not None:
        k = []
        bst=[]
        b = 'b'
        forms = Event.objects.all()
        for i in forms:
            if str(i.organizer) == host.name:
                k.append(i.event_id)
        for i in range(len(k)):
            b = b+str(i)
            a = Event.objects.get(event_id = k[i])
            bst.append(a)
            b = 'b'
        return render(request,'basic/user.html',{'form':bst})
    else:
        return  render(request,'basic/user.html',{'form':''})



@login_required(login_url='/')
@allowed_users(allowed_roles = ['admin','host'])
def accountsettings(request):
    user = request.user.host
    form = HostForm(instance=user)
    if request.method == 'POST':
        form = HostForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
    return render(request,'basic/account_settings.html',{'form':form})