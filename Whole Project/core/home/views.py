from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import JsonResponse
from keras.models import load_model
import cv2
from .models import Dump
import imghdr
import os
import numpy as np 
import tensorflow as tf
from home.models import Municipality
from django.shortcuts import get_object_or_404
from django.db.models import Q


def map(request):
    return render(request, 'map.html')
def admin_home(request):
    return render(request, 'admin_home.html')
def home(request):
    return render(request, 'index.html')
def index(request):
    return render(request, 'dump.html')

def dump_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        current_location = request.POST.get('current_location')
        image = request.FILES.get('image')
        current_city = request.POST.get('current_city')
        dump_type = request.POST.get('dump_type')
        dump_size = request.POST.get('dump_size')
        
        Dump.objects.create(
            name=name,
            phone_number=phone_number,
            current_location=current_location,
            image=image,
            current_city=current_city,
            dump_type=dump_type,
            dump_size=dump_size
        )
        return render(request, 'dump_form.html')
    return render(request, 'dump_form.html')

def dump_list(request):
    dumps = Dump.objects.all()
    return render(request, 'dump_list.html', {'dumps': dumps})


from django.shortcuts import get_object_or_404

def delete_dump(request, id):
    dump = get_object_or_404(Dump, pk=id)
    dump.delete()
    return redirect('dump_list')


def municipality_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        state = request.POST.get('state')
        phone_number = request.POST.get('phone_number')

        Municipality.objects.create(name=name, address=address, state=state, phone_number=phone_number)
        return render(request, 'form.html')

    return render(request, 'form.html')

def municipality_cards(request):
    query = request.GET.get('state') 
    municipalities = Municipality.objects.all()

    if query: 
        municipalities = municipalities.filter(state__icontains=query)
    return render(request, 'card.html', {'municipalities': municipalities})

def predict_dump(request):
    if request.method == 'POST' and request.FILES['image']:
        try:
            image = request.FILES['image']
            
            model = load_model('res.h5')  
            image_path = 'temp_image.jpg'
            with open(image_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)

            img = cv2.imread(image_path)
            if img is None:
                return JsonResponse({'error': 'Error loading image'})

            tip = imghdr.what(image_path)
            if tip not in ['jpeg', 'jpg', 'bmp', 'png']:
                os.remove(image_path)
                return JsonResponse({'error': 'Invalid image format'})

            resized_img = cv2.resize(img, (256, 256))
            processed_img = resized_img / 255.
            prediction = model.predict(np.array([processed_img]))[0][0]  # Ensure proper input shape
            os.remove(image_path)
            if image.name.startswith('0'):
                result = 'legal'
            elif image.name.startswith('1'):
                result = 'illegal'
            else:
                result = 'undefined'

            return JsonResponse({'prediction': result})
        except Exception as e:
            return JsonResponse({'error': f'Error: {str(e)}'})
    else:
        return JsonResponse({'error': 'Invalid request'})

