from django.db import models
from django.utils import timezone
from django.core.ulrresolvers import reverse
import hashlib
from django.core.validators import  *
from django.core.exceptions import ValidationError
import datetime
# Create your models here.

class Restaurant(models.Model):

    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


    TIMING_CHOICES = (
        (MONDAY, 'monday'),
        (TUESDAY, 'tuesday'),
        (WEDNESDAY, 'wednesday'),
        (THURSDAY, 'thursday'),
        (FRIDAY, 'friday'),
        (SATURDAY, 'saturday'),
        (SUNDAY, 'sunday'),
        )
    email = models.EmailField(primery_key=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=150, db_index=True)
    address = models.CharField(max_length=100)
    #phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") #############look into regex
	#phone = models.CharField(validators=[phone_regex],max_length=15,blank=True)
    restaurant_website = models.TextField(validators=[URLValidator()])
    timings = models.IntegerField(choices=TIMING_CHOICES, default=MONDAY)
    other_details = models.TextField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    """
    class Meta:
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'
        ordering = ('restaurant_name',)
        index_together = (('id','slug'),)

    """
    def make_password(self ,password):
            assert password
		    hashedpassword = hashlib.md5(password).hexdigest()
	   	    return hashedpassword

	def check_password(self, password):
		assert password
		hashed = hashlib.md5(password).hexdigest()
		return self.password == hashed

	def set_password(self, password):
		self.password = password

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #   return reverse('restaurant:restaurant_detail', args=[self.id, self.slug])

class Customer(models.Model):
	# userid = models.CharField(primary_key = True,max_length =50)
	password = models.CharField(max_length=100)
	name = models.CharField(max_length=200)
	email = models.EmailField(primary_key = True)

    def make_password(self ,password):
		assert password
		hashedpassword = hashlib.md5(password).hexdigest()
		return hashedpassword

	def check_password(self, password):
		assert password
		hashed = hashlib.md5(password).hexdigest()
		return self.password == hashed

	def set_password(self, password):
		self.password = password

    def __str__(self):
        return self.name

class FoodItem(models.Model):
	resid = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	cuisine = models.CharField(max_length=100)
	COURSE = (
		('s','Starter'),
        ('a','Salat')
		('m','Main Course'),
		('d','Desert')
	)
	course = models.CharField(max_length=1,choices=COURSE)
	price = models.IntegerField()
	availability_time = models.TimeField()
	ordercount = models.IntegerField(default = 0)
    def __str__(self):
        return self.name


class Order(models.Model):
 	customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
 	restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
 	foodlist = models.CharField(max_length = 500,validators=[validate_comma_separated_integer_list],null=True)
 	foodqty = models.CharField(max_length = 500,validators=[validate_comma_separated_integer_list],null=True)
 	amount = models.IntegerField(default = 0)
	ordertime = models.DateTimeField()
	orderdate = models.DateField(auto_now_add=True)

	def calamount(self):
		self.amount = 0
		myl = self.foodlist.split(",")
		qty = self.foodqty.split(",")
		for x,y in zip(myl,qty):
			fitem = FoodItem.objects.get(pk=int(x))
			self.amount = self.amount + fitem.price*int(y)

	def getfooditems(self):
		myl = self.foodlist.split(",")
		items = []
		for x in myl:
			items.append(FoodItem.objects.get(pk=int(x)))
		return items

	def getqty(self):
		myl = self.foodqty.split(",")
		return myl
class Cart(models.Model):
	customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
 	fooditem = models.ForeignKey(FoodItem,on_delete=models.CASCADE)
 	foodqty = models.IntegerField()

"""
class OrderMenu(models.Model):
    order = models.ForeignKey(Order, related_name='menu')
    menu = models.ForeignKey(Menu, related_name='order_menu')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

"""
#####################################################
"""
class Category(models.Model):
    name = models.CharField(max_length=120,db_index=True) #veg, non-veg
    slug = models.SlugField(max_length=120,db_index=True)

    class Meta:
        ordering=('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
"""

"""
class Menu(models.Model):
    category = models.ForeignKey(Category, related_name="menu")
    restaurant = models.ForeignKey(Restaurant, related_name="restaurant_menu")
    name = models.CharField(max_length=120,db_index=True)
    slug = models.SlugField(max_length=120,db_index=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering=('name', )
        index_together = (('id', 'slug'), )
        verbose_name = 'menu'

    def __str__(self):
        return self.name

"""
