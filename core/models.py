from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime

class Customer(models.Model):
	firstName = models.CharField(_('First Name'),max_length=50)
	lastName = models.CharField(_('Last Name'),max_length=50)
	mobile = models.CharField(_('Mobile Number'),max_length=20,unique=True)
	home = models.CharField(_('Home Phone Number'),max_length=20,null=True,blank=True)
	address = models.CharField(_('Address'),max_length=255,null=True,blank=True)
	note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)
	email = models.EmailField(_('Email'),max_length=255,null=True,blank=True)
	locations = models.ManyToManyField('Location')
	createdTime = models.DateTimeField(_('Created Time'),default=datetime.datetime.now)
	isGymCustomer = models.BooleanField(_('Has Gym Membership'),default=False)

	def __unicode__(self):
	    return self.firstName + " " + self.lastName

	def save(self, **kwargs):
		import datetime

		# Fix the time created and time modified
		if not self.id:
			self.createdTime = datetime.datetime.now() # Edit created timestamp only if it's new entry
		super(Customer,self).save()

	class Meta:
		db_table = 'customers'

class Location(models.Model):
    name = models.CharField(_('Location Name'),max_length=50)
    description = models.CharField(_('Location Description'),max_length=50)
    note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
		db_table = 'locations'

class Employee(models.Model):
    user = models.OneToOneField(User,primary_key=True)
    firstName = models.CharField(_('First Name'),max_length=50)
    lastName = models.CharField(_('Last Name'),max_length=50)
    mobile = models.CharField(_('Mobile Number'),max_length=20)
    home = models.CharField(_('Home Phone Number'),max_length=20,null=True,blank=True)
    address = models.CharField(_('Address'),max_length=255,null=True,blank=True)
    note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)
    locations = models.ManyToManyField('Location')
    createdTime = models.DateTimeField(_('Created Time'),default=datetime.datetime.now)


    def __unicode__(self):
	    return self.firstName + " " + self.lastName

    def save(self, **kwargs):
		import datetime
		# Fix the time created and time modified
		if not self.createdTime:
			self.createdTime = datetime.datetime.now() # Edit created timestamp only if it's new entry
		super(Employee,self).save()

    class Meta:
		db_table = 'employees'

class ProductCategory(models.Model):
    name = models.CharField(_('Category Name'),max_length=50)
    description = models.CharField(_('Category Description'),max_length=50)
    note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
		db_table = 'product_categories'

class ProductBrand(models.Model):
    name = models.CharField(_('Brand Name'),max_length=50)
    description = models.CharField(_('Brand Description'),max_length=50)
    note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
		db_table = 'product_brands'

class ProductType(models.Model):
    name = models.CharField(_('Product Name'),max_length=50)
    description = models.CharField(_('Product Description'),max_length=50)
    note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
		db_table = 'product_types'

class Product(models.Model):
    name = models.CharField(_('Product Name'),max_length=50)
    description = models.CharField(_('Product Description'),max_length=50)
    price = models.DecimalField(_('Product Price'),decimal_places=2,max_digits=9)
    note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)
    quantity = models.IntegerField(_('Quantity'),null=True,blank=True)
    productType = models.ForeignKey('ProductType',null=True,blank=True)
    productCategory = models.ForeignKey('ProductCategory',null=True,blank=True)
    productBrand = models.ForeignKey('ProductBrand',null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
		db_table = 'products'

class Exercise(models.Model):
    name = models.CharField(_('Exercise Name'),max_length=50)
    description = models.CharField(_('Exercise Description'),max_length=50)
    note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
		db_table = 'exercises'

class CustomerDetailAttribute(models.Model):
    name = models.CharField(_('Attribute Name'),max_length=50)
    description = models.CharField(_('Attribute Description'),max_length=50)
    note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
		db_table = 'customer_detail_attributes'

class CustomerDetail(models.Model):
    customer = models.ForeignKey('Customer')
    detailDate = models.DateField(_('Detail Date'))
    exercises = models.ManyToManyField('Exercise',null=True,blank=True,through="ExerciseDetail")
    customerDetailAttributes = models.ManyToManyField('CustomerDetailAttribute',null=True,blank=True,through='AttributeDetail')

    def __unicode__(self):
        return str(self.id)

    class Meta:
		db_table = 'customer_details'

class AttributeDetail(models.Model):
    customerDetailAttribute = models.ForeignKey('CustomerDetailAttribute')
    customerDetail = models.ForeignKey('CustomerDetail')
    amountDone = models.IntegerField(_('Amount'))

    def __unicode__(self):
        return str(self.id)

    class Meta:
		db_table = 'attribute_details'

class ExerciseDetail(models.Model):
    exercise = models.ForeignKey('Exercise')
    customerDetail = models.ForeignKey('CustomerDetail')
    amountDone = models.IntegerField(_('Amount Done'))

    class Meta:
		db_table = 'exercise_details'

class ClassType(models.Model):
    name = models.CharField(_('Class Type Name'),max_length=50)
    description = models.CharField(_('Class Type Description'),max_length=50)
    note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
		db_table = 'class_types'

class Government(models.Model):
    name = models.CharField(_('Government Name'),max_length=50)
    description = models.CharField(_('Government Description'),max_length=50)
    note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
		db_table = 'governments'

class Shipment(models.Model):
    name = models.CharField(_('Shipment Name'),max_length=50)
    description = models.CharField(_('Shipment Description'),max_length=50)
    note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
		db_table = 'shipments'

class Trainer(models.Model):
	firstName = models.CharField(_('First Name'),max_length=50)
	lastName = models.CharField(_('Last Name'),max_length=50)
	mobile = models.CharField(_('Mobile Number'),max_length=20)
	home = models.CharField(_('Home Phone Number'),max_length=20,null=True,blank=True)
	address = models.CharField(_('Address'),max_length=255,null=True,blank=True)
	note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)
	skill = models.ManyToManyField('ClassType')
	salary = models.DecimalField(_('Salary'),default=150,decimal_places=2,max_digits=9)

	def __unicode__(self):
	    return self.firstName + ' ' + self.lastName

	class Meta:
		db_table = 'trainers'

class Class(models.Model):
    startingTime = models.DateTimeField(_('Starting Time'))
    endingTime = models.DateTimeField(_('Ending Time'))
    trainer = models.ForeignKey('Trainer')
    isTrainerPaid = models.BooleanField(_('Trainer Paid'),default=False)
    amountPaid = models.DecimalField(_('Trainer Paid Amount'),default=0,decimal_places=2,max_digits=9)
    attendees = models.ManyToManyField('Customer')
    type = models.ForeignKey('ClassType')

    def __unicode__(self):
        return str(self.startingTime) + " " + self.type.name + " " + self.trainer.firstName + " " + self.trainer.lastName

    class Meta:
		db_table = 'classes'

class SpaUsage(models.Model):
    startingTime = models.DateTimeField(_('Time Started'))
    endingTime = models.DateTimeField(_('Time Ended'))
    attendees = models.ManyToManyField('Customer')

    def __unicode__(self):
        return "Spa Session"

    class Meta:
		db_table = 'spa_usages'

class MachinesUsage(models.Model):
    startingTime = models.DateTimeField(_('Time Started'))
    endingTime = models.DateTimeField(_('Time Ended'))
    attendees = models.ManyToManyField('Customer')

    def __unicode__(self):
        return "Machine Day"

    class Meta:
		db_table = 'machines_usages'

class Service(models.Model):
    name = models.CharField(_('Service Name'),max_length=50)
    description = models.CharField(_('Service Description'),max_length=50)
    price = models.DecimalField(_('Service Price'),decimal_places=2,max_digits=9)
    note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
		db_table = 'services'

class Package(models.Model):
    name = models.CharField(_('Package Name'),max_length=50)
    description = models.CharField(_('Package Description'),max_length=50)
    price = models.DecimalField(_('Package Price'),decimal_places=2,max_digits=9)
    note = models.CharField(_('Extra Note'),max_length=255,null=True,blank=True)
    services = models.ManyToManyField('Service',through = 'PackageDetail')

    def __unicode__(self):
        return self.name

    class Meta:
		db_table = 'packages'

class PackageDetail(models.Model):
    service = models.ForeignKey('Service')
    package = models.ForeignKey('Package')
    maximumNumberAllowed = models.IntegerField(_('Maximum Number Allowed'))

    def __unicode__(self):
        return str(self.id)

    class Meta:
		db_table = 'package_details'

class Order(models.Model):
    customer = models.ForeignKey('Customer',null=True,blank=True)
    employee = models.ForeignKey('Employee')
    location = models.ForeignKey('Location')
    shipment = models.ForeignKey('Shipment',null=True,blank=True)
    government = models.ForeignKey('Government',null=True,blank=True)
    address = models.CharField(_('Address'),max_length=255,null=True,blank=True)
    price = models.DecimalField(_('Order Price'),decimal_places=2,max_digits=9)
    products = models.ManyToManyField('Product',through='OrderDetail')
    createdTime = models.DateTimeField(_('Created Time'),default=datetime.datetime.now)

    def __unicode__(self):
        return str(self.id)

	def save(self, **kwargs):
		import datetime

		# Fix the time created and time modified
		if not self.id:
			self.createdTime = datetime.datetime.now() # Edit created timestamp only if it's new entry
		super(Order,self).save()

    class Meta:
		db_table = 'orders'

class OrderDetail(models.Model):
    order = models.ForeignKey('Order')
    product = models.ForeignKey('Product')
    price = models.DecimalField(_('Package Price'),decimal_places=2,max_digits=9)
    quantity = models.IntegerField(_('Quantity'))

    def __unicode__(self):
        return str(self.id)

    class Meta:
		db_table = 'orders_details'

class Membership(models.Model):
    customer = models.ForeignKey('Customer')
    employee = models.ForeignKey('Employee',related_name="mebership_creator")
    package = models.ForeignKey('Package')
    price = models.DecimalField(_('Membership Price'),decimal_places=2,max_digits=9)
    createdTime = models.DateTimeField(_('Created Time'),default=datetime.datetime.now)
    endedTime = models.DateTimeField(_('Ended Time'))
    pausedTime = models.DateTimeField(_('Paused Time'), null = True, blank=True)
    daysPaused = models.IntegerField(_('Days Paused'),default=0)
    pauser = models.ForeignKey('Employee',related_name="mebership_pauser",null = True, blank=True)

    def __unicode__(self):
        return str(self.id)

	def save(self, **kwargs):
		import datetime

		# Fix the time created and time modified
		if not self.createdTime:
			self.createdTime = datetime.datetime.now() # Edit created timestamp only if it's new entry
		super(Membership,self).save()

    class Meta:
		db_table = 'memberships'

