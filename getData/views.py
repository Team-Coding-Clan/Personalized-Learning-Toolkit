from django.shortcuts import render
from .forms import Register,Login
from django.db import connection
import sys
from subprocess import run, PIPE
# Create your views here.
'''
def register(request):
    return render(request,"register.html")
'''

def register(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            try:
                form.save()
                return render(request,"register.html",{"msg":"Successfully registered\nWelcome!."})
                #return render()
            except:
                pass
    else:
        form = Register
        print("Registeration unsuccessful")
    return render(request,"register.html",{"form":form})


def login(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']

        cursor = connection.cursor()
        p = cursor.execute("Select * from mydatabase.userdata where username = '" + username + "' and password = '" + password + "'")
        print(p)
        data = cursor.fetchone()
        print(data)
        if (data is None):
            return render(request,'login.html',{'context':'Not a user !'})
        else :
            return render(request,'homepage.html')
    else:
        form = Login()
    return render(request,"login.html",{"form":form})

def home(request):
    return render(request,"homepage.html")

def external(request):
   # input1 = request.POST.get("parameter1")
   # input2 = request.POST.get("parameter2")
    output = run([sys.executable,'C:\\Users\\DELL\\PycharmProjects\\djangoProject3\\dataset1.py'],shell=False,stdout=PIPE)
    print(output)

    return render(request,"recommendation.html",{'data':output.stdout.strip().decode("utf-8")})

def recommend(request):
    return render(request,"recommendation.html")
