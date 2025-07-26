from django.shortcuts import render, get_object_or_404
import matplotlib.pyplot as plt
import pandas as pd
import urllib, base64, io, folium, joblib, numpy as np
import datetime
from folium.plugins import MarkerCluster
from django.http import HttpResponse
from collections import Counter
from Crimes.models import *
from django.db.models import Q
from Crimes.forms import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create your views here.
def home(request):
    return render(request, 'home.html')

def dashboard(request):
    query = request.GET.get('q', '')
    crimes = CrimeRecord.objects.all()

    if query:
        crimes = crimes.filter(
            Q(crime_type__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'crimes': crimes,
        'query': query,
    }
    return render(request, 'dashboard.html', context)

def detail(request, crime_id):
    crime = get_object_or_404(CrimeRecord, id=crime_id)
    return render(request, 'details.html', {'crime': crime})

def similarity_search(request):
    form = CrimeSimilarityForm(request.GET or None)
    results = []
    
    if form.is_valid():
        # Combine the input features into a single string
        input_text = " ".join([
            form.cleaned_data.get("crime_type", ""),
            form.cleaned_data.get("modus_operandi", ""),
            form.cleaned_data.get("weapon_used", ""),
            form.cleaned_data.get("location", "")
        ])
        
        # Prepare corpus: each crime's features
        crimes = CrimeRecord.objects.all()
        corpus = []
        for crime in crimes:
            text = " ".join([
                crime.crime_type or "",
                crime.modus_operandi or "",
                crime.weapon_used or "",
                crime.location or ""
            ])
            corpus.append(text)

        # Add input to the top of the list
        corpus.insert(0, input_text)

        # Compute TF-IDF similarity
        tfidf = TfidfVectorizer().fit_transform(corpus)
        cosine_sim = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

        # Combine similarity with crimes
        for i, sim in enumerate(cosine_sim):
            if sim > 0:
                results.append((crimes[i], round(sim * 100, 2)))  # (crime, similarity %)

        # Sort by highest similarity
        results.sort(key=lambda x: x[1], reverse=True)

    return render(request, "similarity_search.html", {"form": form, "results": results})

def crime_trends(request):
    crimes = CrimeRecord.objects.all()

    # --- 1. Crimes per Month ---
    months = [crime.date.strftime("%B") for crime in crimes if crime.date]
    month_count = Counter(months)

    plt.figure(figsize=(8, 4))
    plt.bar(month_count.keys(), month_count.values(), color="skyblue")
    plt.title("Crimes by Month")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    monthly_graph = base64.b64encode(image_png).decode("utf-8")

    # --- 2. Crimes by Type ---
    crime_types = [crime.crime_type for crime in crimes if crime.crime_type]
    type_count = Counter(crime_types)

    plt.figure(figsize=(8, 4))
    plt.bar(type_count.keys(), type_count.values(), color="salmon")
    plt.title("Crimes by Type")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    type_graph = base64.b64encode(image_png).decode("utf-8")

    # --- 3. Status Pie Chart ---
    statuses = [crime.case_status for crime in crimes if crime.case_status]
    status_count = Counter(statuses)

    plt.figure(figsize=(4, 4))
    plt.pie(status_count.values(), labels=status_count.keys(), autopct='%1.1f%%')
    plt.title("Case Status Distribution")
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    status_graph = base64.b64encode(image_png).decode("utf-8")

    return render(request, "crime_trends.html", {
        "monthly_graph": monthly_graph,
        "type_graph": type_graph,
        "status_graph": status_graph
    })

def crime_hotspot_map(request):
    map_center = [12.9716, 77.5946]  # Bengaluru coordinates
    crime_map = folium.Map(location=map_center, zoom_start=12)

    marker_cluster = MarkerCluster().add_to(crime_map)

    crimes = CrimeRecord.objects.all()
    for crime in crimes:
        if crime.latitude and crime.longitude:
            folium.Marker(
                location=[crime.latitude, crime.longitude],
                popup=f"<b>{crime.crime_type}</b><br>{crime.location}<br>Status: {crime.case_status}",
                icon=folium.Icon(color="red" if "murder" in crime.crime_type.lower() else "blue")
            ).add_to(marker_cluster)

    map_html = crime_map._repr_html_()

    return render(request, "crime_map.html", {"map_html": map_html})



def heatmap_view(request):
    crimes = CrimeRecord.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    
    heat_data = [[crime.latitude, crime.longitude] for crime in crimes]

    return render(request, 'heatmap.html', {'heat_data': heat_data})


# Load model and encoders once
model = joblib.load('crime_predictor_model.pkl')
le_dict = joblib.load('label_encoders.pkl')
le_target = joblib.load('target_encoder.pkl')

def predict_crime_view(request):
    prediction = None
    confidence = None

    if request.method == 'POST':
        location = request.POST['location']
        modus = request.POST['modus_operandi']
        weapon = request.POST['weapon_used']
        date_str = request.POST['date']

        try:
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            month, day, year = date_obj.month, date_obj.day, date_obj.year
        except ValueError:
            month = day = year = 0

        # Encode inputs
        location_encoded = le_dict['Location'].transform([location])[0] if location in le_dict['Location'].classes_ else 0
        modus_encoded = le_dict['Modus Operandi'].transform([modus])[0] if modus in le_dict['Modus Operandi'].classes_ else 0
        weapon_encoded = le_dict['Weapon Used'].transform([weapon])[0] if weapon in le_dict['Weapon Used'].classes_ else 0

        input_features = np.array([[location_encoded, modus_encoded, weapon_encoded, month, day, year]])

        pred = model.predict(input_features)
        prob = model.predict_proba(input_features)

        prediction = le_target.inverse_transform(pred)[0]
        confidence = round(np.max(prob) * 100, 2)

    return render(request, 'predict_crime.html', {
        'prediction': prediction,
        'confidence': confidence
    })
