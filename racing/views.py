from django.shortcuts import render
import requests
from django.http import HttpResponse
from .forms import RacingForm
def home(request):
    if request.method == 'POST':
        form = RacingForm(request.POST)
        if form.is_valid():
            driver = form.cleaned_data['driver']
            race = form.cleaned_data['race']
            constructor = form.cleaned_data['constructor']
            grid = form.cleaned_data['grid']
            print('grid ',grid)
            api_url = "http://127.0.0.1:7999/predict"
            params = {'grid': grid, 'driver':driver,'race':race,'constructor':constructor}
            response = requests.post(api_url,json=params)
            res = response.json()
            # res=[6.000006]
            print(res)
            prediction = round(res[0],1)
            formEmpty = RacingForm()

            return render(request, 'home.html', {'form':formEmpty,'prediction': prediction})
       
    else:
        formEmpty = RacingForm()
        return render(request, 'home.html', {'form':formEmpty})