
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
## Create your views here.
from django.core.files.storage import FileSystemStorage
#from hfapp.forms import ProfileForm
from hfnapp.models import hfmodel
from hfnapp import face
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url,
        })

    return render(request, 'upload.html')
    

def home(request):
    if request.method == 'POST' :
        image_url = request.POST['image_url']
        image_url.split('/')[1]
        full_img_path = "/home/nivyanth/Hackfest/hfn"+ image_url
        print(full_img_path)
        attendance_map = face.get_attendance_map(full_img_path)

        return render(request, 'home.html', {
            'image_url': image_url,
            'attendance_map' : attendance_map
        })
    return render(request, 'home.html')
