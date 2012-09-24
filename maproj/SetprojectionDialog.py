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

class SetprojectionDialog(Gtk.Dialog):
    __gtype_name__ = "SetprojectionDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated SetprojectionDialog object.
        """
        builder = get_builder('SetprojectionDialog')
        new_object = builder.get_object('setprojection_dialog')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a SetprojectionDialog object with it in order to
        finish initializing the start of the new SetprojectionDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self)
        
        #Inform user, that s/he has to test the given projection, before adding is possible
        self.ui.label_status.set_text('Please test the syntax to enable adding!')
        #Set some global variables, as they are needed in different functions
        global proj
        proj = ''
        global setted
        setted = False

   
    def on_btn_ok_clicked(self, widget, data=None):
        """The user has elected to save the changes.

        Called before the dialog returns Gtk.ResponseType.OK from run().
        """
        if setted == True:
            #Read the textview and add text to the dictionary
            buff = self.ui.textview1.get_buffer()
            name = t.iterTextview(buff)
            buff2 = self.ui.textview2.get_buffer()
            global proj
            proj = t.iterTextview(buff2)
            #Append the new projection to the file, containing all projections
            #Therefore the file is opened with "a"
            try:
                wobj = open('./data/media/projections.txt', "a")
            except:
                home = os.getenv("HOME")
                wobj = open(home + '/maproj/media/projections.txt', "a")
	        wobj.write(name + ' : ' +proj + '\n')
	        wobj.close()
            
        pass

    def on_btn_cancel_clicked(self, widget, data=None):
        """The user has elected cancel changes.

        Called before the dialog returns Gtk.ResponseType.CANCEL for run()
        """
        pass

    #This is quasi the help
    #---gives an example to see how the syntax should look like---
    def on_mnu_syntax_activate(self, widget, data=None):
        self.ui.label_name.set_text("Mercator")
        self.ui.label_wkt.set_text("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over")
    
    #This button enables the testing of the given projection
    def on_button_test_clicked(self, widget, data=None):
        #get content of textviews
        buff = self.ui.textview1.get_buffer()
        name = t.iterTextview(buff)    
        buff2 = self.ui.textview2.get_buffer() 
        #this is a global variable to call it global ;-) --> defined while initialization     
        global proj
        proj = name = t.iterTextview(buff2)   
        #That is the test - it's just the reprojection and if it doesn't work...the syntax is not right
        #Could be done better...but I only have 3 weeks...and I will do it later 
        try: 
            #just a test but not a good one...should be replaced later
            dict1 = t.readProj('./data/media', 'projections.txt')    
            command = 'ogr2ogr -f \'ESRI Shapefile\' ./data/media/cache/syntaxtest ./data/media/ne_110m_admin_0_countries.shp -t_srs \''+proj+'\' -overwrite -skipfailure'           
        except:
            home = os.getenv("HOME")                
            folder = home + '/maproj/media'
            command = 'ogr2ogr -f \'ESRI Shapefile\' '+folder+'/cache/syntaxtest /usr/share/maproj/media/ne_110m_admin_0_countries.shp -t_srs \''+proj+'\' -overwrite -skipfailure'
        
        tester = os.system(command)        #--> Failure = 256   
        #just do when the test gave 0 --> means everything was done well
        if tester == 256:
            self.ui.label_status.set_text('Sorry...thats not right!')
        elif tester == 0:
            self.ui.label_status.set_text('Yes...thats the right Syntax!')
            global setted
            setted = True
            #the OK-button shows no text after initialiation
            #best would be if it doesn't react also but I don't know how to do that...not now!!!
            self.ui.btn_ok.set_label('Add')
        else:
            self.ui.label_status.set_text('Unknown error!')

if __name__ == "__main__":
    dialog = SetprojectionDialog()
    dialog.show()
    Gtk.main()
