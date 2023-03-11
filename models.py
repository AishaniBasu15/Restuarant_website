from django.db import models

# Create your models here.
class categories(models.Model):
	name=models.CharField(max_length=100)
	status=models.BooleanField(default=True)
	def __str__(self):
		return self.name
#to  create table named products DB
class product(models.Model):
	pname=models.CharField(max_length=200)
	price=models.CharField(max_length=100)
	s_decr=models.TextField()
	l_descr=models.TextField()
	quantity=models.CharField(max_length=100)
	slug=models.SlugField(primary_key=True)
	active=models.BooleanField(default=True)
	product_category=models.ForeignKey(categories,on_delete=models.CASCADE)

	def __str__(self):
		return self.slug
#to create table named product_image in DB
class product_image(models.Model):
	single_product=models.ForeignKey(product,on_delete=models.CASCADE)
	img=models.ImageField(upload_to='product_image/imgs/',null=True)
	active=models.BooleanField(default=True)

	def __str__(self):
		return self.single_product.pname
class signup(models.Model):
	name=models.CharField(max_length=100)
	address=models.CharField(max_length=400)
	email=models.CharField(max_length=100)
	phone=models.CharField(max_length=20)
	userId=models.CharField(max_length=50,primary_key=True)
	password=models.CharField(max_length=50)

	def __str__(self):
		return self.name
class payu(models.Model):
	Cardnum=models.CharField(max_length=20,primary_key=True)
	Cvv=models.CharField(max_length=3)
	money=models.CharField(max_length=5)
	def __str__(self):
		return self.Cardnum
