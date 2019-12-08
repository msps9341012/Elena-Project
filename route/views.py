from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import googlemaps
from django.http import JsonResponse


gmaps = googlemaps.Client(key='AIzaSyAnxkwgFS9TIQ5sPFbtk1McDbNbVUqv2Vc')
def test(request):
    context = {}
    return render(request, "hello_world.html")

def index(request):
	source = request.GET.get('source')
	dest = request.GET.get('dest') #destination
	opt = request.GET.get('opt') #min or max
	thres = request.GET.get('thres') #percentage that user wants

	#lat/lng of source..etc
	geocode_result = gmaps.geocode(source)
	lat=geocode_result[0]['geometry']['location']['lat']
	lng=geocode_result[0]['geometry']['location']['lng']

	geocode_result = gmaps.geocode(dest)
	lat1=geocode_result[0]['geometry']['location']['lat']
	lng1=geocode_result[0]['geometry']['location']['lng']
	
	'''
	Call min/max elevation algo
	'''

	#return route information wrapped in json 
	data={'source':[lat,lng],'dest':[lat1,lng1]}

	return JsonResponse(data)



