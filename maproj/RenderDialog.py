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

from gi.repository import Gtk # pylint: disable=E0611

from maproj_lib.helpers import get_builder

import gettext
from gettext import gettext as _
gettext.textdomain('maproj')

from maproj import functions as t
from maproj import gdal_functions as gdal

class RenderDialog(Gtk.Dialog):
    __gtype_name__ = "RenderDialog"

    def __new__(cls, sent):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated RenderDialog object.
        """
        subs = sent.split(":")

        global projection 
        projection = subs[0]
        global new_stylesheet
        new_stylesheet = subs[2]
        global path
        path = subs[1]
        global shapefile
        shapefile = subs[3]
        global image
        image = ''
        global checkbutton
        checkbutton = False

        builder = get_builder('RenderDialog')
        new_object = builder.get_object('render_dialog')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a RenderDialog object with it in order to
        finish initializing the start of the new RenderDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self)
        self.ui.entry_height.set_text('600')
        self.ui.entry_width.set_text('300')
        self.ui.image1.clear()

    def on_button_render_clicked(self, widget, data=None):
        
        #path = '/home/ralf/Software/Quickly/maproj/data/media'
        #new_stylesheet = '/new_source_world_style.xml'
        #projection = '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
        #shapefile = '/home/ralf/Software/Quickly/testdaten/reprojected_userfile/polygons.shp'

        global image
        image = path+'/user_image.png'
        size = (int(self.ui.entry_height.get_text()),int(self.ui.entry_width.get_text()))        
        
        #print image
        #print path
        #print new_stylesheet
        #print projection
        #print shapefile
        if checkbutton == True:
            extent = gdal.getExtentFromShape(shapefile)
            print extent
            t.complexRun(image, path+'/'+new_stylesheet, extent, size)
            self.ui.image1.set_from_file(image)
            self.ui.entry_lllo.set_text(str(extent[0]))
            self.ui.entry_urlo.set_text(str(extent[1]))
            self.ui.entry_llla.set_text(str(extent[2]))
            self.ui.entry_urla.set_text(str(extent[3]))
            self.ui.label_result.set_text('Saved to: ' + image)
            
        else:
            
            try:
                extent = (float(self.ui.entry_lllo.get_text()), float(self.ui.entry_urlo.get_text()), float(self.ui.entry_llla.get_text()), float(self.ui.entry_urla.get_text()))
                #print extent
                t.complexRun(image, path+'/'+new_stylesheet, extent, size)
                self.ui.image1.set_from_file(image)  
                self.ui.label_result.set_text('Saved to: ' + image)              
            except:
                self.ui.label8.set_text('Emtpty entry or not as float!')
                self.ui.image1.clear()

    def on_btn_ok_clicked(self, widget, data=None):
        """The user has elected to save the changes.

        Called before the dialog returns Gtk.ResponseType.OK from run().
        """
        pass

    def on_btn_cancel_clicked(self, widget, data=None):
        """The user has elected cancel changes.

        Called before the dialog returns Gtk.ResponseType.CANCEL for run()
        """
        pass

    def on_checkbutton1_toggled(self, widget, data=None):
        global checkbutton
        if checkbutton == True:
            checkbutton = False 
        elif checkbutton == False:
            checkbutton = True


    def getResult(self):
        if image != '':
            return image
        else:
            return 'None'
        


if __name__ == "__main__":
    dialog = RenderDialog()
    dialog.show()
    Gtk.main()
