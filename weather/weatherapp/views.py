from django.shortcuts import render
import requests
import datetime 
from django.contrib import messages

def home(request):
    if 'city' in request.POST:
        city=request.POST['city']
    else:
        city='new york'

    url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=9470f0ed85247bc24a1037b54c2c56b4'
    PARAMS ={'units':'metric'}

    API_KEY='AIzaSyD_VxFS-NS-sO2OOQVH5T4kPXipIv6N3DY'
    SEARCH_ENGINE_ID='36678daaea346428e'

    query=city+"1920x1080"
    page=1
    start=(page-1)*10+1
    searchType='image'
    city_url = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start{start}&searchType={searchType}&imgSize=xlarge'

    image_url = None
    try:
        search_data = requests.get(city_url).json()
        search_items = search_data.get("items")
        if search_items and len(search_items) > 0:
            image_url = search_items[0]['link']
            print("Image URL:", image_url)
        else:
            print("No images found for city.")
    except Exception as e:
        print(f"Image fetch error: {e}")
    try:
        data = requests.get(url, params=PARAMS).json()
        description=data['weather'][0]['description']
        icon=data['weather'][0]['icon']
        temp=data['main']['temp'] 

        day=datetime.date.today()

        return render(request,'weatherapp/index.html',{'description':description,'icon':icon,'temp':temp,'day':day,'city':city,'exception_occurred':False,'image_url':image_url})
    
    except KeyError:
        exception_occurred=True
        messages.error(request,'enter data is not available to API.')
        day=datetime.date.today()
        return render(request,'weatherapp/index.html',{'description':'clear sky','icon':'01d','temp':25,'day':day,'city':'chittoor','exception_occurred':True})
    return render(request,'weatherapp/index.html',{'description':description,'icon':icon,'temp':temp,'day':day,'city':city,'exception_occurred':False})