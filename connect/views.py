from django.shortcuts import render
from .forms import Connect
# Create your views here.

def userConnect(request):
    if request.method == "POST":
        form = Connect(request.POST)
        if form.is_valid():
            try:
                form.save()
                return render(request,"userConnect.html",{"msg":"Connected."})
            except:
                pass
    else:
        form = Connect()
        print("Not connected.")
    return render(request,"userConnect.html",{"form":form})
