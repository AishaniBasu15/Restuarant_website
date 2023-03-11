from django.shortcuts import render ,redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from paywix.payu import Payu
# Create your views here.
import random 
import hashlib
from django.http import JsonResponse

payu_config = settings.PAYU_CONFIG
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

# Create Payu Object for making transaction
# The given arguments are mandatory
payu = Payu(merchant_key, merchant_salt, surl, furl, mode)
# Create your views here.
def HOME(request):
	return render(request,"homepage.html")
def about(request):
	return render(request,"AboutPage.html")
def contact(request):
	return render(request,"ContactPage.html")
def products(request):
	ob=product.objects.all()
	return render(request,"Items.html",{"records":ob})
def details(request,items_id):
	# print("-----------------------------------",items_id)
	item_ob=product.objects.get(slug=items_id)
	# print(item_ob)
	return render(request,"details.html",{"records":item_ob})
def cart(request):
	# print("heelo")
	v_quantity=request.POST['quantity']
	v_slug=request.POST['slug']
	print(v_quantity)
	print(v_slug)
	
	item_ob1=product.objects.get(slug=v_slug)
	single_item={v_slug:[item_ob1.product_image_set.all()[0].img.url,item_ob1.pname,item_ob1.price,v_quantity]}
	# print (single_item)
	try:
		var=request.session['Cart_info']
		print("old vses ",var)
		f=0
		for x in var:
			# print(x)
			# print("check")
			if v_slug in x:
				# print("help")
				h=int(x[v_slug][-1])
				h+=int(v_quantity)
				x[v_slug][-1]=str(h)
				print(x[v_slug])
				f=1
		# print("hello ")
		if f==0:
			var.append(single_item)
		request.session['Cart_info']=var
	except Exception as e:
		# print("world")
		request.session['Cart_info']=[single_item]
	request.session['Cart_count']=len(request.session['Cart_info'])
	print(request.session['Cart_info'])
	return redirect('/CartDisplay')

def cart_details(request):
	try:
		carts=request.session['Cart_info']
		# print("hello",carts)
		request.session['cart_disp_count']=True
		# print(carts)
		grossTotal=0
		for i in carts:
			for k,v in i.items():
				grossTotal+=int(v[-1])*int(v[-2])
		request.session['totalAmount'] = grossTotal
		if(carts==[]):
			request.session['cart_disp_count']= False
		return render(request,"CartItems.html",{'all_cart':carts})
	except:
		request.session['cart_disp_count']=False
		return render(request,"CartItems.html")
		# print("hello",carts)
def remove_cart(request,k_slug):
	i=0
	sess=request.session['Cart_info']
	print(sess)
	for x in sess:
		if k_slug in x:
			break
		else:
			i+=1
	sess.pop(i)
	#print(sess)
	#print(i)
	request.session['Cart_info']=sess
	request.session['Cart_count']=len(request.session['Cart_info'])
	return redirect('/CartDisplay')
def signin(request):
	return render(request,"signinPage.html")
def sign_up_value(request):
	Name=request.POST['name']
	Address=request.POST['address']
	Email=request.POST['email']
	Phn=request.POST['phone']
	u_name=request.POST['user']
	pswrd=request.POST['password']
	
	s=signup()
	s.name=Name
	s.address=Address
	s.email=Email
	s.phone=Phn
	s.userId=u_name
	s.password=pswrd
	s.save()
	print(Name,"\t",Address)
	return redirect('/LogIn')
def login(request):
	return render(request,"loginPage.html")
def loginvalue1(request):
	usrnm=request.POST['u_nm']
	paswrd=request.POST['psword']
	# print("--"*30)
	# print(usrnm)
	# print(paswrd)
	try:
		sign_ob=signup.objects.get(userId=usrnm)
		# print("check")
		# print(sign_ob.userId)
		if((usrnm==sign_ob.userId) and (paswrd==sign_ob.password)):
			# print("check")
			arr=[sign_ob.userId,sign_ob.name,sign_ob.address,sign_ob.email,sign_ob.phone]
			request.session['userinfo']=arr
			return redirect('/')
		else:
			print("hello")
			request.session['error-msg']=2
			return redirect('/Log_in')
	except Exception as e:
		print("world")
		request.session['error-msg']=1
		return redirect('/Signup')
	return redirect('/')

def Signup(request):
	try:
		if request.session['error-msg']==1:
			msg1="please Sign Up first"
			del request.session['error-msg']
	except:
		msg1=''
	return render(request,"signinPage.html",{'msg1':msg1})
def Log_in(request):
	try:
		if request.session['error-msg']==2:
			msg1="Please Enter Correct Details"
			del request.session['error-msg']

	except:
		msg1=''
	return render(request,loginPage.html,{'msg1':msg1})

def logout(request):
	del request.session['userinfo']
	return redirect('/LogIn')


# Payu checkout page
@csrf_exempt
#@login_required(login_url='/login')
def checkout_form(request):
	try:
		if(request.session['userinfo']):
			print("test1")
			single_user=request.user
			print("test2")
			if request.method=='POST':
				print("hello100")
				hash_object=hashlib.sha256(b'randint(0,20)')
				txnid=hash_object.hexdigest()[:20]
				data = {'txnid':txnid,
				'amount': request.session['totalAmount'], 
				'firstname': request.POST['firstname'], 
				'email': request.POST['email'],
				'phone': request.POST['phone'],
				'productinfo':request.POST['productinfo'], 
				'lastname': request.POST['lastname'],
				'address1': request.POST['address1'], 
				'address2': request.POST['address2'],
				'city': request.POST['city'], 
				'state': request.POST['state'],
				'country':request.POST['country'], 
				'zipcode': request.POST['zipcode'], 
				'udf1': '', 
				'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''}
				print("test90")
				payu_data=payu.transaction(**data)

				return render(request,"payu_checkout.html",{'posted':payu_data})
			# print("test3")
			return render(request,"current_datetime.html")

		else:
			print("hello")
			return redirect('/LogIn')
	except Exception as e:
		print("world")
		print (e)
		# return redirect('/LogIn')


@csrf_exempt
def payu_success(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    return JsonResponse(response)



# Payu failure page
@csrf_exempt
def payu_failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    return JsonResponse(response)    

