# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Ralf Klammer <milkbread@freenet.de>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('maproj')

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('maproj')

from maproj_lib import Window
from maproj.AboutMaprojDialog import AboutMaprojDialog
from maproj.PreferencesMaprojDialog import PreferencesMaprojDialog

from maproj.ChooseprojectionDialog import ChooseprojectionDialog
from maproj.SetprojectionDialog import SetprojectionDialog
from maproj.OpenDialog import OpenDialog
from maproj.TrynerrorDialog import TrynerrorDialog
from maproj.SetstyleDialog import SetstyleDialog
from maproj.RenderDialog import RenderDialog

import os
import subprocess

from maproj import gdal_functions as gdal
# See maproj_lib.Window.py for more details about how this class works
class MaprojWindow(Window):
    __gtype_name__ = "MaprojWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(MaprojWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutMaprojDialog
        self.PreferencesDialog = PreferencesMaprojDialog

        self.ui.label4.set_text('Please choose or a set a projection!')

        try:
            #just a test but not a good one...should be replaced later
            dict1 = t.readProj('./data/media', 'projections.txt')
            self.ui.image_proj.set_from_file("./data/media/background/default0.png")
        except:
            self.ui.image_proj.set_from_file("/usr/share/maproj/media/background/default0.png")

        # Code for other initialization actions should be added here.
        global dicts    
        dicts = 'a test'
        global filename
        filename = {}
        global image
        image = ''
        global proj
        proj = ''
        global user_xml
        user_xml = ''
        global user_path
        user_path = ''
        global tester
        tester = False
        #self.ui.image_proj.clear()
        
    def on_mnu_choose_activate(self, widget, data=None):
        chooser = ChooseprojectionDialog()
        result = chooser.run()

         #close the dialog, and check whether to proceed        
        chooser.destroy()
        if result != Gtk.ResponseType.OK:
            return        

        if chooser.get_image() != 'None':
            global image
            image = chooser.get_image()
            #print image
            self.ui.image_proj.set_from_file(image)
            global proj
            proj = chooser.get_proj()
            self.ui.entry1.set_text(proj[0])   
            self.ui.entry2.set_text(proj[1])
            self.ui.label4.set_text('Preview of chosen projection!') 
            tester = chooser.get_prob()
           
        else:
            self.ui.label4.set_text('Failure! Please choose a projection!')
            self.ui.image_proj.set_from_file("./data/media/background/error.png")

        

        

    def on_mnu_open_activate(self, widget, data=None):
        opener = OpenDialog()
        result = opener.run()             
        #get the file, the directory and the format as dict
        global filename
        filename = opener.selected_file
        if filename != None:
            self.ui.entry3.set_text(filename['File'])
        
        #close the dialog, and check whether to proceed        
        opener.destroy()
        if result != Gtk.ResponseType.OK:
            return

    def on_mnu_set_activate(self, widget, data=None):
        setter = SetprojectionDialog()
        result = setter.run() 

        #close the dialog, and check whether to proceed        
        setter.destroy()
        if result != Gtk.ResponseType.OK:
            return
                
    def on_mnu_change_activate(self, widget, data=None):
        
        if proj != '':
            if filename != {}:
                folder = 'folder'
                projection = proj[1].split('\n')
                folder = filename['uri']
                reprojected_source = folder +'/reprojected_userfile'
                global reprojected_file
                reprojected_file =  reprojected_source + '/' + filename['File']   
                if folder.find(" ") != -1:
                    help = folder.split(" ")
                    help2 = help[0] + '\ ' + help[1]
                    #print help2
                    folder = help2
                command = 'ogr2ogr -f \'ESRI Shapefile\' '+ reprojected_source + ' ' + folder +'/'+ filename['File'] +' -t_srs \''+projection[0]+' \' -overwrite -skipfailure'
                #print command

                destination = folder +'/'+ filename['File']
                destination = destination.split('.shp')[0] + '.prj'
	            if os.system('find ' + destination) == 0:
                    try:    
                        os.system( command )
                        self.ui.label4.set_text('Shapefile was reprojected and saved in source path!')
                        self.ui.image_proj.set_from_file(image)
                    except:
                        
                        self.ui.image_proj.set_from_file("./data/media/background/error.png")
                else:
                    self.ui.label4.set_text("The chosen shape has no Projection...edit with a GIS")
            else:
                self.ui.label4.set_text('Failure! Please choose a shapefile!')
        else:
            self.ui.label4.set_text('Failure! Please choose a projection!')
            

    def on_mnu_tne_activate(self, widget, data=None):
        tryer = TrynerrorDialog(tester)
        result = tryer.run() 

        #close the dialog, and check whether to proceed        
        tryer.destroy()
        if result != Gtk.ResponseType.OK:
            return

    def on_mnu_setstyle_activate(self, widget, data=None):
        
        if proj != '':
            if filename != {}:
                #fileCache = str(filename['uri'] +'/'+ filename['File'])
                projection = proj[1].split('\n')[0] + ':' +  reprojected_file 
                setter = SetstyleDialog(projection)
                result = setter.run()
                global user_path 
                user_path = setter.get_path()
                global user_xml
                user_xml = setter.get_newStyle()
                #close the dialog, and check whether to proceed        
                setter.destroy()
                if result != Gtk.ResponseType.OK:
                    return
                self.ui.label4.set_text('Stylefile succesfully rewritten...lets go and render a single image!')
                self.ui.image_proj.set_from_file(image)
            else:
                self.ui.label4.set_text('Cannot set a new stylefile! Please set a shapefile!')
                self.ui.image_proj.set_from_file("./data/media/background/error.png")
        else:
            self.ui.label4.set_text('Cannot set a new stylefile! Please choose a projection!')
            self.ui.image_proj.set_from_file("./data/media/background/error.png")
    
    def on_mnu_render_activate(self, widget, data=None):
        if user_path != '':
            projection = proj[1].split('\n')[0]
            sending = projection + ":" + user_path + ":" + user_xml + ":" + reprojected_file
            render = RenderDialog(sending)
            result = render.run() 
            image = render.getResult()           
            #close the dialog, and check whether to proceed        
            render.destroy()
            if result != Gtk.ResponseType.OK:
                return   
            if image != 'None':
                self.ui.label4.set_text('Rendering done!')
                self.ui.image_proj.set_from_file(image)
        else: 
            self.ui.label4.set_text('Cannot render! Please set the stylefile!')
            self.ui.image_proj.set_from_file("./data/media/background/error.png")    


    def on_mnu_test_activate(self, widget, data=None):
        gdal.openOGR()
