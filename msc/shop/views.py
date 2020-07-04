
from django.shortcuts import render
from .models import product,Contact,Orders,Orderupdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
from django.http import HttpResponse
MERCHANT_KEY = 'QEevan71044011577108'


# Create your views here.
from django.http import HttpResponse

def index(request):
    # products = product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products,range(1,nSlides),nSlides],
    #             [products,range(1,nSlides),nSlides]]
    allprods =[]
    catprods = product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allprods.append([prod, range(1,nSlides),nSlides])

    params ={'allProds': allprods}
    return render(request, 'shop/indexs.html', params)

def searchMatch(query,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allprods =[]
    catprods = product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query,item)]
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        if len(prod)!=0:
            allprods.append([prod, range(1,nSlides),nSlides])

    params ={'allProds': allprods,'msg':''}
    if len(allprods)==0 or len(query)<4:
        params={'msg':'Please Make sure to search relevant item'}
    return render(request, 'shop/search.html', params)



def about(request):
    return render(request, 'shop/about.html')



def contact(request):
    if request.method=='POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        number = request.POST.get('number','')
        desc = request.POST.get('desc','')
        contact =Contact(name=name,email=email,number=number,desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')



def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = Orderupdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({'status':'success','updates':updates,'itemsJson':order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse({'status':'noitem'})
        except Exception:
            return HttpResponse({'status':'error'})

    return render(request, 'shop/tracker.html')





def productview(request,myid):
    # fetching product using id 
    product1 = product.objects.filter(id=myid)
    return render(request, 'shop/prodview.html',{'product':product1[0]})



def checkout(request):
    if request.method=='POST':
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        amount = request.POST.get('amount','')
        email = request.POST.get('email','')
        number = request.POST.get('number','')
        address = request.POST.get('address','')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        order =Orders(items_json=items_json,name=name,email=email,number=number,address=address,address2=address2,city=city,state=state,zip_code=zip_code,amount=amount)
        order.save()
        update = Orderupdate(order_id=order.order_id,update_desc="The order ha sbeen Placed ")
        update.save()
        thank = True
        id = order.order_id

        # return render(request, 'shop/checkout.html',{'thank':thank,'id': id})
        # Return request to transfer the amount to your account after payment to user
        param_dict = {

                'MID': 'QEevan71044011577108',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})