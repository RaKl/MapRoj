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

from quickly import prompts
import os
from quickly.widgets.dictionary_grid import DictionaryGrid

import glob
from maproj import functions as t

class SetstyleDialog(Gtk.Dialog):
    __gtype_name__ = "SetstyleDialog"

    def __new__(cls, sent):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated SetstyleDialog object.
        """
        global projection 
        projection = sent.split(':')[0]

        global filename
        filename = sent.split(':')[1]

        global stylesheet
        stylesheet = ''
        global new_stylesheet
        new_stylesheet = ''
        global new_stylesheet2
        new_stylesheet2 = ''
        
        builder = get_builder('SetstyleDialog')
        new_object = builder.get_object('setstyle_dialog')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a SetstyleDialog object with it in order to
        finish initializing the start of the new SetstyleDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self)

        global path
        path = ''

        #let the user choose a path with the directory chooser
        response, path = prompts.choose_directory()

        #make certain the user said ok before working
        if response == Gtk.ResponseType.OK:
           
           #make a list of the supported xml files
           dicts = dict()
           counter = 0
           #iterate through root directory
           for files in glob.glob(path + "/*.xml"):
                    if files.endswith('.xml'):
                        #create a URI in a format gstreamer likes
                        file_uri = path
                        fileSplit = files.split(path + "/")                        
                        dicts[str(counter)] = fileSplit[1]    
                        counter = counter + 1               
           keylist = dicts.keys()
           keylist.sort()        
           for key in keylist: 
	           #print key, value
               self.ui.comboboxtext1.append_text(dicts[key])

    def on_comboboxtext1_changed(self, widget, data=None):
        global stylesheet
        stylesheet = self.ui.comboboxtext1.get_active_text()       
        

    def on_button_proj_clicked(self, widget, data=None):        
        #print projection
        if stylesheet != None:
            global new_stylesheet
            if new_stylesheet2 == '': 
                new_stylesheet = '/new_projection_'+ stylesheet
                t.replaceOnlyProjection(path, stylesheet, new_stylesheet, projection)
            else:
                new_stylesheet = '/new_projection_'+ new_stylesheet2.split('/new_source_')[1]
                t.replaceOnlyProjection(path, new_stylesheet2, new_stylesheet, projection) 
            
            self.ui.label3.set_text('Projection changed!')

    def on_button_shape_clicked(self, widget, data=None):
        if stylesheet != None:
            global new_stylesheet2
            if new_stylesheet == '':
                new_stylesheet2 = '/new_source_'+ stylesheet
                t.replaceOnlySource(path, stylesheet, new_stylesheet2, filename)
            else:
                new_stylesheet2 = '/new_source_'+ new_stylesheet.split('/new_projection_')[1]
                print new_stylesheet2
                t.replaceOnlySource(path, new_stylesheet, new_stylesheet2, filename)
            self.ui.label5.set_text('Source changed!')  

 
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

#ath+'/'+new_stylesheet, projection

    def get_path(self):
        if path != '':
            cache = path
            return cache
        else:
            cache = 'None'
            return cache

    def get_newStyle(self):
        if new_stylesheet2 != '':
            cache = new_stylesheet2
            return cache
        elif new_stylesheet != '':
            cache = new_stylesheet
            return cache
        else:
            cache = 'None'
            return cache


if __name__ == "__main__":
    dialog = SetstyleDialog()
    dialog.show()
    Gtk.main()
