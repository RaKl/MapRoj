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

from maproj.SetprojectionDialog import SetprojectionDialog

class ChooseprojectionDialog(Gtk.Dialog):
    __gtype_name__ = "ChooseprojectionDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated ChooseprojectionDialog object.
        """
        builder = get_builder('ChooseprojectionDialog')
        new_object = builder.get_object('chooseprojection_dialog')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a ChooseprojectionDialog object with it in order to
        finish initializing the start of the new ChooseprojectionDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self)
        global tester
        tester = False
        global dict1
        global home
        home = os.getenv("HOME")  
        try:
            dict1 = t.readProj('./data/media', 'projections.txt')  
        except:
            if os.system('find ~/maproj/media/projections.txt') != 0:
                os.system('cp /usr/share/maproj/media/projections.txt ~/maproj/media/projections.txt')
              
            dict1 = t.readProj(home + '/maproj/media', 'projections.txt')
            if os.system('find ~/maproj') == 0:
                os.system('mkdir ~/maproj')
                os.system('mkdir ~/maproj/media')
                os.system('mkdir ~/maproj/media/cache/') 
                os.system('touch ~/maproj/media/new_world_style.xml')     
            tester = True        
        keylist = dict1.keys()
        keylist.sort()        
        for key in keylist: 
	        #print key, value
            self.ui.comboboxtext1.append_text(key)
                    

        #initialize the global variables
        global counter
        counter = 0
        global name
        name = ''
        global imagefile
        imagefile = ''

    def on_button_new_clicked(self, widget, data=None):
        opener = SetprojectionDialog()
        result = opener.run()
        #close the dialog, and check whether to proceed
        opener.destroy()
        if result != Gtk.ResponseType.OK:
            return 

    def on_comboboxtext1_changed(self, widget, data=None):
        #get the chosen projection
        global name
        name = self.ui.comboboxtext1.get_active_text()
        proj = ''       
        proj = dict1[str(name)]
        self.ui.entry2.set_text(dict1[str(self.ui.comboboxtext1.get_active_text())])
        
        if proj != 'None':
            #Reproject Previewdata
            global tester
            if tester == False:
                folder = './data/media'
                command = 'ogr2ogr -f \'ESRI Shapefile\' '+folder+'/cache/reprojected'+str(counter)+' ./data/media/ne_110m_admin_0_countries.shp -t_srs \''+proj+'\' -overwrite -skipfailure'
            else:       #needs another saving place ---this one has no rights to write
                folder = home + '/maproj/media'
                command = 'ogr2ogr -f \'ESRI Shapefile\' '+folder+'/cache/reprojected'+str(counter)+' /usr/share/maproj/media/ne_110m_admin_0_countries.shp -t_srs \''+proj+'\' -overwrite -skipfailure'
            
            os.system(command)   
                            
                            
            #os.system('ogrinfo -al ./data/media/reprojected0/ne_110m_admin_0_countries.shp')
            #self.ui.entry1.set_text("Previewdata was reprojected")
            
            #Make XML-file with chosen projection
            #***
            stylefile = "world_style.xml"   
            new_stylefile = t.replaceProjection(folder,stylefile,proj,counter,tester)
            #self.ui.entry1.set_text("XML was rewritten")

            #Render preview
            global imagefile
            imagefile = folder + "/new_world_style.png"
            #start rendering
            image = t.run(imagefile, new_stylefile)
            #show rendered preview     
            self.ui.image1.set_from_file(image)
            #self.ui.entry1.set_text("Preview was rendered")

            #clear cache
            command2 = 'rm -r '+folder+'/cache/reprojected'+str(counter)
            os.system(command2)
                                    
            #increment counter
            global counter
            counter = counter + 1
#        else:
            #Throw an error out
            #self.ui.entry1.set_text("Please choose projection!")

    def get_proj(self):
        if name != '':
            cache = [name, dict1[name]]
            return cache
        else:
            cache = 'None'
            return cache
    
    def get_image(self):
        if name != '':
            return imagefile
        else:
            return 'None'

    def get_prob(self):
        return tester
    

    def on_btn_ok_clicked(self, widget, data=None):
        """The user has elected to save the changes.

        Called before the dialog returns Gtk.ResponseType.OK from run().
        """
        if tester == False:
            t.writeProj(dict1, './data/media', 'projections.txt')
        else:
            t.writeProj(dict1, home + '/maproj/media', 'projections.txt')

        pass

    def on_btn_cancel_clicked(self, widget, data=None):
        """The user has elected cancel changes.

        Called before the dialog returns Gtk.ResponseType.CANCEL for run()
        """
        
    
        pass


if __name__ == "__main__":
    dialog = ChooseprojectionDialog()
    dialog.show()
    Gtk.main()
