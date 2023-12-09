from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from .models import *

def index(request):
    return render(request, "auctions/index.html",{
        "products": Listing.objects.all(),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def desc(request, id):
    pd = Listing.objects.get(pk=id)
    if pd.active == True:
        if request.method == "POST":
            user = request.POST["name"]
            user0 = User.objects.get(username=user)
            product =  Listing.objects.get(pk=id)
            bid = request.POST["bid"]
            if(not Bid.objects.filter(user=user0, product=product).exists()):
                if(int(bid) < int(product.price)):
                    return render(request, "auctions/mess.html", {
                        "message": "Bid amount is low"
                    })
                bids = Bid.objects.filter(product=product).all()
                for i in bids:
                    if int(bid) < int(i.bid):
                        return render(request, "auctions/mess.html", {
                        "message": "Bid amount is lower than other bids"
                    })
                try:
                    bid = Bid.objects.create(user=user0, product=product, bid=bid)
                    bid.save()
                    return  HttpResponseRedirect(reverse("index"))
                except:
                    return render(request, "auctions/mess.html", {
                        "message": "Bid already done."
                    })
            else:
                return render(request, "auctions/mess.html", {
                        "message": "Bid already placed."
                    })
        return render(request, "auctions/desc.html",{
            "product": Listing.objects.get(pk=id),
            "bids": Bid.objects.filter(product=pd).all(),
            "comments": Comment.objects.filter(product=pd).all()
        })
    else:
        bids = Bid.objects.filter(product=pd).all()
        bid = bids.aggregate(Max("bid"))["bid__max"]
        user = Bid.objects.get(product=pd, bid=bid)
        return render(request, "auctions/res.html",{
            "message": user.user.username,
            "product": pd,            
            "comments": Comment.objects.filter(product=pd).all()
        })

def createlisting(request):
    if request.method == "POST":
        user = request.POST["name"]
        user0 = User.objects.get(username=user)
        title0 = request.POST["title"]
        desc0 = request.POST["desc"]
        image0 = request.POST["image"]
        price0 = request.POST["price"]
        categ = request.POST["category"]
        try:
            product = Listing.objects.create(title=title0, image=image0,desc=desc0, price=price0,category=categ, listed_by=user0)
            product.save()
            return  HttpResponseRedirect(reverse("index"))
        except:
            return render(request, "auctions/mess.html", {
                "message": "Product already exists."
            })
    else:
        return render(request, "auctions/create.html")

def category(request):
    s = set()
    products = Listing.objects.all()
    for prod in products:
        s.add(prod.category)
    
    return render(request, "auctions/category.html",{
        "list": s,
    })

def category_desc(request, category):

    return render(request, "auctions/index.html",{
        "products": Listing.objects.filter(category=category).all()
    })
def wishlist(request):
    if request.method == "POST":
        user0 = User.objects.get(username=request.POST['user'])
        product0 = Listing.objects.get(pk = request.POST['id'])
        if(not Wishlist.objects.filter(user=user0, product=product0).exists()):
            try:
                cart = Wishlist.objects.create(user=user0, product=product0)
                cart.save()
                return render(request,"auctions/wishlist.html",{
                    "carts": Wishlist.objects.all()
                })
            except:
                return render(request,"auctions/wishlist.html",{
                    "carts": Wishlist.objects.all()
                })
        else:
            return render(request,"auctions/mess.html",{
                "message": "Already added to wishlist",
            })
    return render(request, "auctions/wishlist.html", {
        "carts": Wishlist.objects.all(),
    })

def deactivate(request):
    if request.method == "POST":
        product = Listing.objects.get(pk = request.POST['id'])
        try:
            product.active = False
            product.save()  
            return render(request, "auctions/mess.html",{
                "message": "Successfully deactivated"
            })
        except:
            return render(request, "auctions/mess.html",{
                "message": "Internal error"
            })
    return render(request, "auctions/mess.html",{
        "message": "Internal error"
    })

def addcomment(request):
    if request.method == "POST":
        user0 = User.objects.get(username=request.POST['name'])
        product0 = Listing.objects.get(pk = request.POST['id'])
        comm = request.POST['comment']
        if( not Comment.objects.filter(user=user0, product=product0).exists()):
            try:
                comment0 = Comment.objects.create(user=user0, product=product0, comment=comm)
                comment0.save()
                return render(request, "auctions/desc.html",{
                    "product": product0,
                    "bids": Bid.objects.filter(product=product0).all(),
                    "comments": Comment.objects.filter(product=product0).all()
                })
            except:
                return render(request, "auctions/mess.html",{
                    "message": "Internal error"
                })
        else:
            return render(request, "auctions/desc.html",{
                "product": product0,
                "bids": Bid.objects.filter(product=product0).all(),
                "comments": Comment.objects.filter(product=product0).all()
            }) 
    return render(request, "auctions/desc.html",{
        "product": product0,
        "bids": Bid.objects.filter(product=product0).all(),
        "comments": Comment.objects.filter(product=product0).all()
    })

def removefromcart(request):
    if request.method == "POST":
        wish = Wishlist.objects.get(pk=request.POST['id'])
        try:
            wish.delete()
            return render(request, "auctions/mess.html",{
                "message": "Removed from cart"
            })
        except:
            return render(request, "auctions/mess.html",{
                "message": "Server Error"
            })
    return render(request, "auctions/wishlist.html",{
        "carts": Wishlist.objects.all(),
    })