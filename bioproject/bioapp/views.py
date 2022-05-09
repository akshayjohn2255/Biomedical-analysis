from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.db.models import Q

from .models import udetails, contents
from .models import dProfile
from .models import admin
import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.sessions.models import Session
from django.core.files.storage import FileSystemStorage

# Create your views here.
def about(request):
    return render(request,'about-us.html',{"home":1})
def ADabout(request):
    return render(request, 'about-us.html', {"admin": 2})
def userabout(request):
    return render(request,'about-us.html',{"user":3})
def docabout(request):
    return render(request,'about-us.html',{"doc":4})

def contact(request):
    return render(request,'contact.html')

def home(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def logincheck(request):
    utype=request.POST.get('utype')
    uname=request.POST.get('uname')
    pwd=request.POST.get('pwd')
    if utype=='Admin':
        try:
            if admin.objects.get(uname=uname) is not None:
                ad = admin.objects.get(uname=uname)
                if pwd == ad.pwd:
                    request.session['sid'] = ad.uname
                    return adminHome(request)
                else:
                    return HttpResponse(" Incorrect Password")
        except:
            return HttpResponse("Username Doesn't Exist")


    elif utype=='Doctor':

            if dProfile.objects.get(uname=uname) is not None:
                print("not nont")
                doc = dProfile.objects.get(uname=uname)
                if pwd == doc.pwd:
                    print("corct pwd")
                    request.session['sid'] = doc.uname
                    print("session set")
                    return docHome(request)
                else:
                    return HttpResponse(" Incorrect Password")
            else:
                return HttpResponse("Username doesn't exist")

    else:
        if udetails.objects.get(uname=uname) is not None:
            print("not nont")
            user = udetails.objects.get(uname=uname)
            if pwd == user.pwd:
                print("corct pwd")
                request.session['sid'] = user.uname
                print("session set")
                return userHome1(request)
            else:
                return HttpResponse(" Incorrect Password")
        else:
            return HttpResponse("Username doesn't exist")

def logout(request):
    try:
        Session.objects.all().delete()
        request.session['sname'].delete()

        return render(request, 'index.html')
    except:
        print('exception')
        return render(request, 'index.html')

#Admin


def adminHome(request):
    uname=request.session['sid']
    return render(request, 'admin/adminHome.html', {'uname': uname})


def viewNewDoc(request):
    if dProfile.objects.filter(Q(status='pending') | Q(status='rejected')| Q(status='deactivated')) is not None:
            new=dProfile.objects.filter(Q(status='pending') | Q(status='rejected')| Q(status='deactivated'))
            return render(request, 'admin/viewDoctors.html',{'doc':new,"status":"new"})

def manageDoc(request):
    id=request.POST.get('did')
    doc=dProfile.objects.get(did=id)

    if 'approve' in request.POST:
        doc.status='active'
    elif 'reject' in request.POST:
        doc.status='rejected'
    elif 'deactivate' in request.POST and doc.status=="active":
        doc.status = 'deactivated'
    doc.save()

    if dProfile.objects.filter(status='pending') is not None:
        new=dProfile.objects.filter(status='pending')
        return render(request, 'admin/viewDoctors.html',{'doc':new})
    else:
        return HttpResponse("No new Registrations")

def viewDoctorlist(request):
    if dProfile.objects.filter(status='active') is not None:
        doclist=dProfile.objects.filter(status='active')
        return render(request, 'admin/viewDoctors.html',{'doc':doclist})
    else:
        return HttpResponse("no active users")

def delDoc(request):
    db=dProfile.objects.get(did=request.POST.get('did')).delete()
    return viewDoctorlist(request)

def viewUsers(request):
    user=udetails.objects.all()
    for x in user:
        print("id=",x.uid)
    return render (request,'admin/viewUsers.html',{'user':user})

def adviewNewDislist(request):
    if contents.objects.filter(status="pending") is not None:
        doc=dProfile.objects.all()
        dis=contents.objects.filter(status="pending")
        return render(request, 'admin/viewDiseaselist.html',{'doc':doc,'dislist':dis,'status':"pending"})
    else:
        return HttpResponse("No new Diseases Uploaded")

def disManage(request):
    con = contents.objects.get(id=request.POST.get('disid'))

    if 'approve' in request.POST:
        con.status = 'active'
    elif 'reject' in request.POST:
        con.status = 'rejected'
    else:
        contents.objects.get(id=request.POST.get('disid')).delete()
    con.save()

    return adviewNewDislist(request)


def activeDiseases(request):
    if contents.objects.filter(status="active") is not None:
        doc=dProfile.objects.all()
        dis=contents.objects.filter(status="active")
        return render(request, 'admin/viewDiseaselist.html',{'doc':doc,'dislist':dis})
    else:
        return HttpResponse("No new Diseases Uploaded")

def reRank(request):
    urls=contents.objects.all()
    for x in urls:
        rnk=getRank(request,x.url)
        ur=contents.objects.get(id=x.id)
        ur.rank=rnk
        ur.save()
    if request.POST.get('pending'):
        return adviewNewDislist(request)
    else:
        return activeDiseases(request)



#user


def uregistration(request):
    if not udetails.objects.all():
        return render(request, 'user/uregistration.html',{'uid':1000})
    else:
        uid = udetails.objects.order_by('-uid').first().uid + 1
    return render(request, 'user/uregistration.html',{'uid':uid})

def uregistdb(request):
    user = udetails.objects.all()
    for x in user:
        if x.email == request.POST.get('email'):
            return HttpResponse("Mail Id allready registered")
        else:
            pass
    db = udetails(uid=request.POST.get('uid'),fname=request.POST.get('fname'), lname=request.POST.get('lname'),
                    dob=request.POST.get('dob'),email=request.POST.get('email'), ph=request.POST.get('ph'),
                  uname=request.POST.get('uname'),pwd=request.POST.get('pwd'))

    db.save()
    userid = udetails.objects.order_by('-uid').first().uid + 1
    return render(request, 'user/uregistration.html', {'stid': userid})


def userHome1(request):
    user=udetails.objects.get(uname=request.session['sid'])
    return render(request, 'user/userHome.html', {'user': user})


def uProfile(request):
    user=udetails.objects.get(uname=request.session['sid'])
    return render(request,'user/uProfile.html',{'user': user})

def uUpdatedb(request):
    email = request.POST.get('email')
    ph = request.POST.get('ph')
    pwd = request.POST.get('pwd')
    user1 = udetails.objects.all()
    for x in user1:
        if x.email == email and x.uname != request.POST.get('uname'):
            return HttpResponse("Mail id allready exist")
        elif x.ph == ph and x.uname != request.POST.get('uname'):
            return HttpResponse("Phone Number allready exist")
    user = udetails.objects.get(uname=request.POST.get('uname'))
    user.email = email
    user.ph = ph
    user.pwd = pwd
    user.qual = request.POST.get('qual')
    user.save()
    return uProfile(request)

def userViewDoctors(request):
    docs=dProfile.objects.all()
    now=datetime.datetime.now()
    return render(request,'user/userViewDoc.html',{'docs':docs,'now':now})

def searchDisease(request):
    disname=request.POST.get('dis')
    obj=contents.objects.filter(keyword__icontains=disname,status="active").order_by('rank')
    doc=dProfile.objects.all()
    return render(request, 'user/searchDisease.html',{'urllist':obj,'doc':doc})

def userViewDoc(request):
    doc = dProfile.objects.get(did=request.POST.get('did'))
    now = datetime.datetime.now()
    if request.POST.get('admin') is not None:
        return render(request, 'user/viewDocProfile.html', {'doc': doc, 'now': now,'admin':1})
    return render (request,'user/viewDocProfile.html',{'doc':doc,'now':now})

def getUrlContent(request):
    import requests
    from bs4 import BeautifulSoup
    obj = contents.objects.get(id=request.POST.get('id'))
    response = requests.get(obj.url, headers={'User-Agent': 'Mozilla/5.0'})
    html = response.content
    soup = BeautifulSoup(html, features="html.parser")
    print("title:",soup.title.text)
    article=[]
    print(article)
    for i in soup.findAll(['p','li']):

        if len(article)==0:
            if i.find('a'):
                pass
            else:
                article.insert(0,i.text)
        else:

            if i.find('a'):
                pass
            else:
                article.append(i.text)
    '''    
    for pg in soup.find_all('p'):
        print("NEw Para:",pg.text)
    '''
    return render(request,'user/content.html',{'contents':article,'dis':obj.keyword})

#Doctor

def docReg(request):
    if not dProfile.objects.all():
        return render(request, 'Doctor/docRegistration.html',{'did':2000})
    else:
        did = dProfile.objects.order_by('-did').first().did + 1
        return render(request, 'Doctor/docregistration.html', {'did': did})

def docRegDB(request):
    doc = dProfile.objects.all()
    if request.method == 'POST' and request.FILES['certify']:
        print("{yes")
        certificate = request.FILES['certify']
        fs = FileSystemStorage()
        fname = certificate.name
        fsize = certificate.size
        print(fname)
        print(fsize)
        filename = fs.save(fname, certificate)
        certificate_url = fs.url(filename)

        for x in doc:
            if x.uname == request.POST.get('uname'):
                return HttpResponse("Username allready registered")
            if x.email == request.POST.get('email'):
                return HttpResponse("Mail Id allready registered")
            else:
                pass

        '''day=datetime.datetime.today()
        exp=request.POST.get('exp')
        print(exp)
        ex=day.year-exp.year'''

        db = dProfile(did=request.POST.get('did'), fname=request.POST.get('fname'), lname=request.POST.get('lname'),
                      dob=request.POST.get('dob'), email=request.POST.get('email'), ph=request.POST.get('ph'),
                      lno=request.POST.get('lno'),uname=request.POST.get('uname'),qual=request.POST.get('qual'),
                      spec = request.POST.get('spec'),exp =request.POST.get('exp'),pwd=request.POST.get('pwd'),
                      file=certificate_url, status="pending")

        db.save()
        did = dProfile.objects.order_by('-did').first().did + 1
        return render(request, 'Doctor/docregistration.html', {'did': did})


def docHome(request):
    doc=dProfile.objects.get(uname=request.session['sid'])
    return render(request, 'Doctor/docHome.html', {'doc': doc})

def getDid(request):
    doc=dProfile.objects.get(did=request.session['sid'])
    return doc.did



def dateDiff(a):
    time_difference = relativedelta(datetime.datetime.now(),a)
    difference_in_years = time_difference.years
    return difference_in_years

def viewDprofile(request):
    doc=dProfile.objects.get(uname=request.session['sid'])
    exp=dateDiff(doc.exp)
    print("exp==",exp)
    return render(request,'Doctor/dProfileView.html',{'doc':doc,'exp':exp})


def docUpdate(request):
    email = request.POST.get('email')
    ph = request.POST.get('ph')
    pwd = request.POST.get('pwd')
    doc = dProfile.objects.all()
    for x in doc:
        if x.email == email and x.uname!=request.POST.get('uname'):
            return HttpResponse("Mail id allready exist")
        elif x.ph==ph and x.uname!=request.POST.get('uname'):
            return HttpResponse("Phone Number allready exist")
    doc1 = dProfile.objects.get(uname=request.POST.get('uname'))
    doc1.email = email
    doc1.ph=ph
    doc1.pwd=pwd
    doc1.qual= request.POST.get('qual')
    doc1.save()
    return viewDprofile(request)


def dAddDisease(request):
    return render(request, 'Doctor/docAddNewDisease.html')

def newDiseasedb(request):
    doc=dProfile.objects.get(did=request.POST.get('did'))
    db=contents(did=doc,keyword=request.POST.get('disname'),url=request.POST.get('loc'),status="pending")
    db.save()
    return docHome(request)

def docViewAddedDiseases(request):
    doc=dProfile.objects.get(uname=request.session['sid'])
    db=contents.objects.filter(did=doc)
    return render(request, 'Doctor/viewAddedDisease.html',{'dislist':db})

def disupdate(request):
    return render(request, 'Doctor/docAddNewDisease.html')



def getRank(request,url):
    from bioproject.bioapp import ranking
    rank=ranking.rankTest(request,url)
    print("rank=",rank)
    return  rank