from django.shortcuts import render
import requests
from django.http import HttpResponse
from .forms import RacingForm
def home(request):
    # À la soumission du formulaire
    if request.method == 'POST':
        form = RacingForm(request.POST)

        # vérifier le format des données reçu
        if form.is_valid():
            driver = form.cleaned_data['driver']
            race = form.cleaned_data['race']
            constructor = form.cleaned_data['constructor']
            grid = form.cleaned_data['grid']

            # préparation de la requette vers l'api
            api_url = "http://127.0.0.1:7999/predict"
            params = {'grid': grid, 'driver':driver,'race':race,'constructor':constructor}
            
            # récupération de la prédiction de résultat
            response = requests.post(api_url,json=params)
            res = response.json()
            
            # res=[6.000006]
            prediction = round(res[0],1)
            formEmpty = RacingForm()

            # retourner cette valeur sur le front
            return render(request, 'home.html', {'form':formEmpty,'prediction': prediction})
       
    # Affiche le formulaire pour lancer une prédiection
    else:
        formEmpty = RacingForm()
        return render(request, 'home.html', {'form':formEmpty})