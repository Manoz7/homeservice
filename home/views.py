from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

import json

from django.contrib import messages
from home.models import *


# Create your views here.
def index(request):
    return render(request, 'index.html')

def notification():
    status = Status.objects.get(status='pending')
    new = Service_Man.objects.filter(status=status)
    count=0
    for i in new:
        count+=1
    d = {'count':count,'new':new}
    return d


def about(request):
    return render(request, 'about.html')


def contact(request):
    messages.success(request, 'Please Fill up the form to contact us!!')
    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if name != "" and email != "" and phone != "" and content != "":
            mycontact = Contact(name=name, email=email,
                                phone=phone, content=content)
            mycontact.save()
            messages.success(
                request, 'Thank You For submitting form. We will reach you ASAP!!')

        else:
            messages.error(request, 'Please Fill Up the Form Correctly!!')

    return render(request, 'contact.html')


def search(request):
    query = request.GET.get('search')

    if len(query) > 78:
        service = Service.objects.none()

    else:
        allServiceTitle = Service.objects.filter(service_name__icontains=query)
        allServicedesc = Service.objects.filter(service_desc__icontains=query)
        service = allServiceTitle.union(allServicedesc)

    context = {'service': service, 'query': query}
    return render(request, 'search.html', context)


def handleLogin(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('loginusername')
        password = request.POST.get('loginpass')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                messages.success(request, 'User login successfully!')
                return redirect('admin_home')
            else:
                # print(user)
                messages.success(request, 'User login successfully!')
                return redirect('index')
        
        else:
            messages.error(request, 'Username and password does not match!! Please enter right credential!')
            return redirect('login')
            
    context = {'page': page}
    return render(request, 'login_register.html', context)


def admin_register(request):
    page = 'admin'
    
    if request.method == 'POST':
        username = request.POST['admin_username']
        email = request.POST['admin_email']
        password1 = request.POST['pw1'] 
        password2 = request.POST['pw2'] 
        fname = request.POST['a_fname']
        lname = request.POST['a_lname']
                
        # Create the admin user
        user = User.objects.create_superuser(username= username.lower(), email=email, password=password1, first_name=fname, last_name=lname)
        user.save()
        
        login(request, user)
        return redirect('admin_home')
    
    context = {'page': page}
    return render(request, 'login_register.html', context)

def user_register(request):
    page = 'user_register'
    services = Service.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        # Create the user

        user = User.objects.create_user(username=data['user_username'].lower(
        ), email=data['user_email'], password=data['user_pass1'], first_name=data['user_fname'], last_name=data['user_lname'])
        user.save()

        Service_Man.objects.create(
            user=user, image=image, phone=data['user_phone'], address=data['user_address'], service=data['service'])
        login(request, user)
        return redirect("/")

    context = {'page': page, 'services': services}
    return render(request, 'login_register.html', context)


def customer_register(request):
    page = 'customer_register'

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('c_image')

        # Create the user
        customer = User.objects.create_user(
            data['customer_username'].lower(), data['customer_email'], data['customer_pass1'], first_name=data['customer_fname'], last_name=data['customer_lname'])
        customer.save()

        Customer.objects.create(user=customer,  image=image,
                                phone=data['customer_phone'], address=data['customer_address'])
        login(request, customer)
        return redirect("/")

    context = {'page': page}
    return render(request, 'login_register.html', context)


def handleLogout(request):
    logout(request)
    messages.success(request, 'User logout successfully!')
    return redirect('index')


def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})


def serviceView(request, myid):
    messages.success(
        request, 'What are you waiting for? --> Get your “To-Do” list ready and call us')
    service = Service.objects.filter(service_id=myid)[0]

    context = {'service': service}

    return render(request, 'service_view.html', context)


def addService(request):

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if Service.objects.filter(service_name=data['service_name']).exists():
            print('Service Already Exists.')

        else:
            service = Service.objects.create(
                service_name=data['service_name'],
                service_desc=data['service_desc'],
                image=image
            )
            return redirect('services')

    return render(request, 'add_service.html')


def profile(request):
    users = User.objects.get(id=request.user.id)
    
    try:
        profile = Customer.objects.get(user=users)
    
    except:
        profile = Service_Man.objects.get(user = users)


    return render(request, 'profile.html', {'profile': profile})


def book_service(request):
    # service = Service.objects.filter()[0]

    if request.method == 'POST':
        itemsJson = request.POST['itemsJson']
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        issue = request.POST['message']

        book = BookService(items_json=itemsJson, name=name, email=email,
                           address=address, phone=phone, book_desc=issue)

        book.save()

        update = BookUpdate(
            book_id=book.book_id, update_desc="Your Service has been in Notice. We will call you as soon as possible!!")

        update.save()

        thank = True
        id = book.book_id

        context = {'thank': thank, 'id': id}

        return render(request, 'book_service.html', context)

    # context = {'service': service}

    return render(request, 'book_service.html')
    # return render(request, 'book_service.html', context)


def tracker(request):
    if request.method == "POST":
        bookId = request.POST.get('bookId', '')
        email = request.POST.get('email', '')

        try:
            book = BookService.objects.filter(book_id=bookId, email=email)

            if len(book) > 0:
                update = BookUpdate.objects.filter(book_id=bookId)
                updates = []

                for item in update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.timestamp})

                    response = json.dumps(
                        {'status': 'success', 'updates': updates, 'itemsJson': book[0].items_json}, default=str)

                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "noitem"}')

        except Exception as e:
            print(e)
            return HttpResponse('{"status": "error"}')

    return render(request, 'tracker.html')



def user_profile(request):
    category = request.GET.get('category')
    
    
    if category == None:
        services = Service.objects.all()
        return render(request, 'user_profile.html', {'services': services})
        

    elif category == 'users':
        users = Service_Man.objects.all()
        return render(request, 'user_profile.html', {'users': users})
        
    
    elif category == 'customer':
        customers = Customer.objects.all()
        return render(request, 'user_profile.html', {'customers': customers})
        
    else:
        return render(request, 'user_profile.html')


def admin_home(request):
    services = Service.objects.all()
    users = Service_Man.objects.all()
    customers = Customer.objects.all()

    context = {'services': services, 'users':users, 'customers': customers}
    
    return render(request, 'admin_home.html', context)