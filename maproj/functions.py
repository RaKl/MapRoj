#!/usr/bin/env python
import mapnik2 as mapnik
import os
import glob

#Function for starting the mapnik-rendering
def run(image, stylesheet):
	#stylesheet = 'world_style.xml'
	#image = 'world_style.png'
	imgx = 600
	imgy = 300
	m = mapnik.Map(imgx, imgy)
	mapnik.load_map(m, stylesheet)
	m.zoom_all() 
	mapnik.render_to_file(m, image)
	#print "rendered image to '%s'" % image
	return image

def complexRun(image, stylesheet, extent, size):
	mapfile = stylesheet
    	map_uri = image
	
	imgx = size[0]
	imgy = size[1]

	m = mapnik.Map(imgx,imgy)
	mapnik.load_map(m,mapfile)
	
	if hasattr(mapnik,'mapnik_version') and mapnik.mapnik_version() >= 800:
		bbox = mapnik.Box2d(extent[0],extent[2],extent[1],extent[3])
	else:
		bbox = mapnik.Envelope(extent[0],extent[2],extent[1],extent[3])
	m.zoom_to_box(bbox)
	im = mapnik.Image(imgx,imgy)
	mapnik.render(m, im)
	view = im.view(0,0,imgx,imgy) # x,y,width,height
	view.save(map_uri,'png')

#I made function to avoid redundant code
#I always need that stuff to read the content of a textview
#---give the buffer and get the content of the textview---
def iterTextview(buff):
        start_iter = buff.get_start_iter()
        end_iter = buff.get_end_iter()
	text = buff.get_text(start_iter, end_iter, True)
        return text
	

#Function to replace the proj4-Projection and the shapefile in a mapnik-stylesheet
#Used for the previews of mapnprojections
def replaceProjection(folder, stylesheet, proj, number, tester):
	if tester == False:
		robj = open(folder + '/' + stylesheet, "r")
	else:
		robj = open('/usr/share/maproj/media' + '/' + stylesheet, "r")
	new_style = folder + '/new_'+stylesheet
	wobj = open(new_style, "w")
	for line in robj: 
		if line.find("srs") != -1:
			sub = line.split("srs")
			sub = sub[1].split("\"")
			new = line
			new = new.replace(sub[1], proj)
			wobj.write(new)
		elif line.find(".shp") != -1:			
			sub = line.split("/reprojected")			
			sub = sub[0]+"/reprojected"+str(number)+sub[1]
			wobj.write(sub)
		else:
			wobj.write(line)		    
	robj.close()
	wobj.close()

	return new_style

#Function to replace only the proj4-Projection in a mapnik-stylesheet
def replaceOnlyProjection(folder, stylesheet, new, proj):
	robj = open(folder + '/' + stylesheet, "r")
	new_style = folder + new
	wobj = open(new_style, "w")
	for line in robj: 
		if line.find("srs") != -1:
			sub = line.split("srs")
			sub = sub[1].split("\"")
			new = line
			new = new.replace(sub[1], proj)
			wobj.write(new)		
		else:
			wobj.write(line)		    
	robj.close()
	wobj.close()

	return new_style

#Function to replace only the source in a mapnik-stylesheet
def replaceOnlySource(folder, stylesheet, new, shape):
	robj = open(folder + '/' + stylesheet, "r")
	new_style = folder + new
	wobj = open(new_style, "w")
	for line in robj: 
		if line.find(".shp") != -1:
			sub = line.split('.shp')
			sub2 = sub[0].split('>')
			new_line = sub2[0] + '>' + shape + sub[1]		
			wobj.write(new_line)
		else:
			wobj.write(line)		    
	robj.close()
	wobj.close()

#Function to write the current list of projections to a txt-file
def writeProj(dicts, folder, filename):
	wobj = open(folder + '/' + filename, "w")
	#sort the dict before writing ... even if it makes no sense ;-)
	keylist = dicts.keys()
        keylist.sort()        
        for key in keylist: 
		wobj.write(key + ' : ' +dicts[key])
		wobj.write('')
	wobj.close()

#Function to read the txt-file containing the current list of projections
def readProj(folder, filename):
	robj = open(folder + '/' + filename, "r")
	dicts = dict()
	for line in robj:
		sub = line.split(' : ')
		if len(sub) == 2:
			#OR is not possible becauso of int and str
			if sub[0] != '':
				dicts[sub[0]] = sub[1]
	robj.close()
	return dicts

def testing(counter):
	 tester = 0
         os.chdir('./data/media/cache/reprojected'+str(counter))
         for files in glob.glob("*.shp"):
         	tester = tester + 1    
		print "Teeeeest"            
         return tester

