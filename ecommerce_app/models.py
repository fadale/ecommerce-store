from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Register_models(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile=models.IntegerField()
    address=models.CharField(blank=True,max_length=50,default='Address')
    
    def __str__(self):
        return self.user.username

    

# Model Category
class Category(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

# Model Prand
class Prand(models.Model):
    name=models.CharField(max_length=30)
    icon=models.ImageField(upload_to=f"icon/prand", blank=True )
    def __str__(self):
        return self.name 


# Model Product
class Product(models.Model):
    name = models.CharField(max_length=80)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=None)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to=f"image/pro_", blank=True )
    created_at=models.DateTimeField(auto_now_add=True )
    prand =models.ForeignKey(Prand , on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Attribute_Value(models.Model):
    name = models.CharField(max_length=20)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Attribute_product(models.Model):
    name = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    def __str__(self):
        return  str(self.product)+"," + str(self.attribute)


class Image_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f"image/pro_", blank=True )

    def __str__(self):
        return  str(self.product)+"image" 


class Specification_Product(models.Model):
    title = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title +':'+self.name  


# Create Order Product
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200,null=True,blank=True)


    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return float(total)
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    
class Tags(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name 

class Tag_product(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    tag=models.ForeignKey(Tags, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)  + " : " +str(self.tag ) 



# create Order_Item Model
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True , null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

# Create Shipping Address Model
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    phone = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name =models.CharField(max_length=50)
    email=models.EmailField()
    review=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name  

class Contact(models.Model):
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=models.TextField()
    def __str__(self):
        return self.name

# Create Slider objects
class Slider(models.Model):
    title       = models.CharField(max_length=150)
    sub_title   = models.CharField(max_length=100)
    action_name = models.CharField(max_length=50)
    link        = models.TextField(null=True, blank=True)
    image = models.ImageField(help_text="Size: 600x400",upload_to='image/slider/%Y/%m/%d/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    # Update Image before save to slider
    def save(self):
        super().save()  # saving image first

        img = Image.open(self.image.path) # Open image using self
        if img.height > 420 or img.width > 620:
            new_width  = 600
            new_height = new_width * img.height / img.width 
            new_height = 400
            new_width  = new_height * img.width / img.height
            img = img.resize((int(new_width), int(new_height)), Image.LANCZOS)
            img.save(self.image.path)  # saving image at the same path
        if img.height < 400 or img.width < 600:
            img = img.resize((600,400), Image.LANCZOS)
            img.save(self.image.path)  # saving image at the same path


def tow_days_hence():
    return timezone.now() + timezone.timedelta(hours=48)

class FeaturedProducut(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at=models.DateTimeField(auto_now_add=True )
    xpiration_time=models.DateTimeField(default=tow_days_hence())

    def __str__(self):
        return self.product.name + " , " + str(self.xpiration_time) 
    

class Category_Side(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title=models.CharField(max_length=40)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to=f"image/cat", blank=True )

    def __str__(self):
        return self.category.name +" , " + self.title

class Vertical_Side(models.Model):
    title       = models.CharField(max_length=150)
    sub_title   = models.CharField(max_length=100)
    link        = models.TextField(null=True, blank=True)
    image = models.ImageField(help_text="Size: 250x200",upload_to='image/Vertical_slider')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    # Update Image before save to slider
    def save(self):
        super().save()  # saving image first

        img = Image.open(self.image.path) # Open image using self
        if img.height > 210 or img.width > 260:
            new_width  = 250
            new_height = new_width * img.height / img.width 
            new_height = 200
            new_width  = new_height * img.width / img.height
            img = img.resize((int(new_width), int(new_height)), Image.LANCZOS)
            img.save(self.image.path)  # saving image at the same path
        if img.height < 200 or img.width < 250:
            img = img.resize((250,200), Image.LANCZOS)
            img.save(self.image.path)  # saving image at the same path



class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    
    def _str_(self) -> str:
        return self.product.name 