#!/usr/bin/env python
import mapnik2 as mapnik

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
	

#Function to replace the proj4-Projection an a mapnik-stylesheet
def replaceProjection(folder, stylesheet, proj, number):
	robj = open(folder + '/' + stylesheet, "r")
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
			sub = sub[0]+"/cache/reprojected"+str(number)+sub[1]
			wobj.write(sub)
		else:
			wobj.write(line)		    
	robj.close()
	wobj.close()

	return new_style

#Function to make a list out of the proj4-file
def getList(filename):
	robj = open(filename, "r")
        epsg = []
        name = []
        proj = []
        for line in robj: 
	    #split between meta and definition
            if line.find("---") != -1:
                sub = line.split("--- ")
                sub = sub[1].split(" : ")
		#get epsg number
                epsg.append(sub[0].split("EPSG ")[1])
		#get epsg name
                name.append(sub[1])
	    #get epsg proj4-definition
            if line.find("+proj") != -1:
                proj.append(line.split("\n")[0])
        liste = [epsg,name,proj]
	
	return liste

#That was a helping function to convert an existing sql implementes EPSG_list
#to a readable, only Proj4 Data containing file
#1-reads file
#2-writes just the necessary parts to a new file
def makeList(sheet):
	robj = open(sheet, "r")
	new_sheet = "EPSG-proj4-list.txt"
	wobj = open(new_sheet, "w")
	for line in robj: 
		#if it contains text
		if len(line) > 4:
			#to keep the name			
			if line.find("---") != -1:
				wobj.write(line)
			#extract the proj4-Data from the Insert-statement				
			if line.find("+proj") != -1:
				sub = line.split("+proj")
				sub2 = "+proj"+sub[1]
				sub3 = sub2.split("+no_defs")
				proj = sub3[0]+"+no_defs"
				wobj.write(proj+"\n")
	robj.close()
	wobj.close()

	
