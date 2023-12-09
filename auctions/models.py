from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self) -> str:
        return f"{self.username}: {self.email}"

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    image = models.CharField(max_length=350)
    desc = models.CharField(max_length= 350 , default="This is a really good product")
    price = models.FloatField()
    category = models.CharField(max_length=64, default="Cloth")
    listed_by =  models.ForeignKey(User,on_delete=models.CASCADE, related_name="created")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.listed_by.username} created {self.title} with price {self.price}"


class Bid(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="bid")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} bidded on {self.product.title} of sp {self.product.price} with price {self.bid}"
    
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="commentedon")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="product")
    comment = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.user.username} commented on {self.product.title} as-> {self.comment}"
    

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="addedby")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="productadded")

    def __str__(self) -> str:
        return  f"{self.user.username} added {self.product.title} into the wishlist"