from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import googlemaps
from django.http import JsonResponse
from . import min_route,max_route

gmaps = googlemaps.Client(key='AIzaSyAnxkwgFS9TIQ5sPFbtk1McDbNbVUqv2Vc')
def test(request):
    context = {}
    return render(request, "hello_world.html")

def index(request):
	source = request.GET.get('source')
	dest = request.GET.get('dest') #destination
	max_opt = request.GET.get('max_opt')
	min_opt = request.GET.get('min_opt') #min or max
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
	if max_opt=='true':
		res=max_route.get_max_elevation_gain((lat,lng),(lat1,lng1),float(thres)/100)
	else:
		res=min_route.get_min_elevation_gain((lat,lng),(lat1,lng1),float(thres)/100)
	
	if len(res['new_path'])>2:
		res['new_path'].pop()
		res['new_path'].pop(0)
	#return route information wrapped in json 
	data={'source':[lat,lng],'dest':[lat1,lng1],'new_path':res['new_path'],
	'new_dist': str(res['new_dist']/1000)+" mi", 'new_elevation_gain': str(res['new_elevation_gain']/1000)+" mi"}
	return JsonResponse(data)



