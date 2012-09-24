#!/usr/bin/env python
import os

import sys
import ogr

def getExtentFromShape(shapefile):
	ds = ogr.Open(shapefile)
        if ds is None:
	        print "Open failed.\n"
	        #sys.exit( 1 )
	else:
		layer = ds.GetLayer(0)
		layer.ResetReading()
                
	return layer.GetExtent()


#ll = (11.987982, 50.368444, 12.584153, 50.679242)
#(897457.4376301226, 951518.7344816582, 5912001.165168648, 5953149.383240214)


def openOGR():
	#Source: That site was very helpfull: http://nullege.com/codes/show/src%40v%40e%40vectorformats-0.1%40vectorformats%40Formats%40OGR.py/85/ogr.Geometry.AddPoint_2D/python
	
	#source = "/media/Speicher/Daten/Testdaten/polygons.shp"
	#source = "/home/ralf/Grunddaten/testdaten/ne_110m_admin_0_countries.shp"
	source = "/media/Speicher/Daten/Testdaten/ne_110m_admin_0_countries.shp"
	#source = "/media/Speicher/Daten/Testdaten/points.shp"
	#source = "/media/Speicher/Daten/Testdaten/points_simple.shp"
	#source = "/media/Speicher/Daten/Testdaten/lines.shp"	
	#source = "/home/ralf/Grunddaten/testdaten/lines.shp"	
	#ds = ogr.Open( "/media/Speicher/Daten/vogtland/points-vgtl-27-01-12.shp")
	ds = ogr.Open(source)
	
	#+++Output+++
	destination = source.split('.')[0] + '_new.shp'
	if os.system('find ' + destination) == 0:
		cache = destination.split('shp')[0]+'*'	
		os.system('rm ' + cache )
		print "Had to delete"
	
	driverName = "ESRI Shapefile"
	drv = ogr.GetDriverByName( driverName )
	dn = drv.CreateDataSource(destination)
	#+++
	
	if ds is None:
	    print "Open failed.\n"
	    #sys.exit( 1 )
	else:

		print "Number of Layers: " + str(ds.GetLayerCount())

		for i in xrange(ds.GetLayerCount()):
			layer = ds.GetLayer(i)
			layer.ResetReading()
			print "Number of Features: " + str(layer.GetFeatureCount())
			#+++Output+++
			test = layer.GetFeature(0)
			test2 = test.GetGeometryRef()
			print 'type: ' + str(test2.GetGeometryType())
			newLayer = dn.CreateLayer( "layer"+str(i), None, test2.GetGeometryType() )			
			#+++
			print layer.GetExtent()
			for index in xrange(layer.GetFeatureCount()):
				
				feature = layer.GetFeature(index)
				geometry = feature.GetGeometryRef()
				geometryN = ogr.Geometry(type=geometry.GetGeometryType() )		#+++		
				f = ogr.Feature(feature_def=newLayer.GetLayerDefn())			#+++
				if geometry.GetGeometryType() == ogr.wkbMultiPolygon:
					#print "MultiPolygon" + str(geometry.GetGeometryCount())
					gpoly = ogr.Geometry(type=ogr.wkbPolygon)		#+++
					for x in xrange(geometry.GetGeometryCount()):
						#print "loop - geometries"
						ring = geometry.GetGeometryRef(x)
						points = badPointExtruder(str(ring))
								#print ring.GetPointCount()
								#points = ring.GetPointCount() ... doesn't work!
						gring = ogr.Geometry(type=ogr.wkbLinearRing)	#+++
						for p in xrange(len(points[0])):
							#print "loop - points"
								#would be better...but doesn't work
								#lon, lat, z = ring.GetPoint(p)
								#gring.AddPoint_2D(lon, lat)							
							#print float(points[0][p])
							gring.AddPoint_2D(float(points[0][p]), float(points[1][p]))	#+++
						gpoly.AddGeometry(gring)			#+++
					geometryN.AddGeometry(gpoly)				#+++
					
				elif geometry.GetGeometryType() == ogr.wkbPolygon:
				#	print "Polygon"									
					ring = geometry.GetGeometryRef(0)
					points = ring.GetPointCount()
					gring = ogr.Geometry(type=ogr.wkbLinearRing)		#+++
					for p in xrange(points):
						lon, lat, z = ring.GetPoint(p)
						gring.AddPoint_2D(lon, lat)			#+++
					geometryN.AddGeometry(gring)				#+++
					
				elif geometry.GetGeometryType() == ogr.wkbPoint:
				#	print "Point"					
					lon, lat, z = geometry.GetPoint()
					geometryN.AddPoint_2D(lon, lat)				#+++
				
				elif geometry.GetGeometryType() == ogr.wkbMultiPoint:
				#	print "Multipoint"
					#points = geometry.GetGeometryCount()
					points = secondBadPointExtruder(str(geometry))					
					for p in xrange(len(points[0])):
						gring = ogr.Geometry(type=ogr.wkbPoint)
				  	        gring.AddPoint_2D(float(points[0][p]), float(points[1][p]))
				        	geometryN.AddGeometry(gring)	
					#	lon, lat, z = geometry.GetPoint(p)
					#	print geometry
					#geometryN.AddPoint_2D(lon, lat)
	

				elif geometry.GetGeometryType() == ogr.wkbLineString:
				#	print "LineString"									
					points = geometry.GetPointCount()
					for p in xrange(points-1):
						lon, lat, z = geometry.GetPoint(p)
						geometryN.AddPoint_2D(lon, lat)			#+++
						
						
				elif geometry.GetGeometryType() == ogr.wkbMultiLineString:
				#	print "MultiLineString"
					for y in xrange(geometry.GetGeometryCount()):
						ring = geometry.GetGeometryRef(y)
						points = ring.GetPointCount()
						gring = ogr.Geometry(type=ogr.wkbLineString)	#+++
						for p in xrange(points):
							lon, lat, z = ring.GetPoint(p)
							gring.AddPoint_2D(lon, lat)		#+++						
						geometryN.AddGeometry(gring)			#+++
				f.SetGeometry(geometryN)					#+++
				newLayer.CreateFeature(f)					#+++

#For any reason, the functions GetPointCount and GetPoint do not work for multipolygons
#therefore I need this function...it gets all points of the rings of a multipolygon				
def badPointExtruder(geometry):
	subs = geometry.split('((')
	subs = subs[1].split('))')	
	subs = subs[0].split(' ')
	lon = []
	lat = []
	length = len(subs)
	for i in xrange(length):
		if i == 0:
			subs2 = subs[i].split(',')			
			lon.append(subs2[0]+'.'+subs2[1])
			
		elif i == length-1:
			subs2 = subs[i].split(',')
			lat.append(subs2[0]+'.'+subs2[1])
			
		else:
			subs2 = subs[i].split(',')
			lat.append(subs2[0]+'.'+subs2[1])
			lon.append(subs2[2]+'.'+subs2[3])
	coords = []
	coords.append(lon)
	coords.append(lat)
	return coords

#same is true for multipoints
def secondBadPointExtruder(geometry):
	subs = geometry.split('(')
	subs = subs[1].split(')')	
	subs = subs[0].split(' ')
	length = len(subs)
	lon = []
	lat = []
	if length == 2:
		subsLon = subs[0].split(',')
		lon.append(subsLon[0]+'.'+subsLon[1])
		subsLat = subs[1].split(',')
		lat.append(subsLat[0]+'.'+subsLat[1])
	else:
		for i in xrange(length):
			if i == 0:
				subs2 = subs[i].split(',')			
				lon.append(subs2[0]+'.'+subs2[1])
			elif i == length-1:
				subs2 = subs[i].split(',')			
				lat.append(subs2[0]+'.'+subs2[1])
			else:	
				subs2 = subs[i].split(',')
				lat.append(subs2[0]+'.'+subs2[1])
				lon.append(subs2[2]+'.'+subs2[3])
	coords = []
	coords.append(lon)
	coords.append(lat)
	return coords
	


				


