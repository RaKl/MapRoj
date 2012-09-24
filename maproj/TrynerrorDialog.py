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

import os
from maproj import functions as t
import glob

class TrynerrorDialog(Gtk.Dialog):
    __gtype_name__ = "TrynerrorDialog"

    def __new__(cls, test):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated TrynerrorDialog object.
        """
        global tester
        tester = test

        builder = get_builder('TrynerrorDialog')
        new_object = builder.get_object('trynerror_dialog')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a TrynerrorDialog object with it in order to
        finish initializing the start of the new TrynerrorDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self)

        #initialize the global variables
        global counter
        counter = 0
        

    def on_button_try_clicked(self, widget, data=None):
        print self.ui.entry1.get_text()

        proj = self.ui.entry1.get_text()
        if proj != '':
            #Reproject Previewdata
            if tester == False:
                command = 'ogr2ogr -f \'ESRI Shapefile\' ./data/media/cache/reprojected'+str(counter)+' ./data/media/ne_110m_admin_0_countries.shp -t_srs \''+proj+'\' -overwrite -skipfailure'
                imagefile = "./data/media/new_world_style_tryNerror.png"
                command2 = 'rm -r ./data/media/cache/reprojected'+str(counter)
            else:
                home = os.getenv("HOME") 
                folder = home + '/maproj/media'
                command = 'ogr2ogr -f \'ESRI Shapefile\' '+folder+'/cache/reprojected'+str(counter)+' /usr/share/maproj/media/ne_110m_admin_0_countries.shp -t_srs \''+proj+'\' -overwrite -skipfailure'
                imagefile = folder + "/new_world_style_tryNerror.png"
                command2 = 'rm -r '+ folder +'/cache/reprojected'+str(counter)
                
            os.system(command)

            #Make XML-file with chosen projection
            stylefile = "world_style_tryNerror.xml"   
            new_stylefile = t.replaceProjection('./data/media',stylefile,proj,counter, tester)
            
            #Render preview
            
            
            try:
              #start rendering
              image = t.run(imagefile, new_stylefile)
              #show rendered preview 
              self.ui.image1.set_from_file(image)
              self.ui.label_feedback.set_text('Yes...that works!')
            except:
              self.ui.image1.clear()
              self.ui.label_feedback.set_text('Oh no...that doesn\'t work!')
            
            #clear cache
            os.system(command2)

                                    
            #increment counter
            global counter
            counter = counter + 1

        else:
            self.ui.label_feedback.set_text('Nothing entered!')



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


if __name__ == "__main__":
    dialog = TrynerrorDialog()
    dialog.show()
    Gtk.main()
