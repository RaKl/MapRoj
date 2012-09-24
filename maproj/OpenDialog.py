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
            
class OpenDialog(Gtk.Dialog):
    __gtype_name__ = "OpenDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated OpenDialog object.
        """
        builder = get_builder('OpenDialog')
        new_object = builder.get_object('open_dialog')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a OpenDialog object with it in order to
        finish initializing the start of the new OpenDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self)

	
        self.supported_shape_formats = [".shp"]

        #let the user choose a path with the directory chooser
        response, path = prompts.choose_directory()

        #make certain the user said ok before working
        if response == Gtk.ResponseType.OK:
           #make one list of support formats
           formats = self.supported_shape_formats

           #make a list of the supported media files
           media_files = []
           #iterate through root directory
           for files in glob.glob(path + "/*.shp"):
                for format in formats:
                    if files.endswith(format):
                        #create a URI in a format gstreamer likes
                        file_uri = path
                        fileSplit = files.split(path + "/")
                        #add a dictionary to the list of media files
                        media_files.append({"File":fileSplit[1],"uri":file_uri, "format":format})

           #remove any children in scrolled window
           #for c in self.ui.scrolledwindow1.get_children():
            #   self.ui.scrolledwindow1.remove(c)

           #create the grid with list of dictionaries
           #only show the File column
           global media_grid
           media_grid = DictionaryGrid(media_files, keys=["File"])

           #show the grid, and add it to the scrolled window
           media_grid.show()
           self.ui.box1.pack_end(media_grid, True, True, 0)


    @property
    def selected_file(self):
        media_files = dict()
        rows = media_grid.selected_rows
        if len(rows) < 1:
            return None
        else:
            #media_files["File"] = rows[0]['File'],"uri":rows[1]['File'], "format":rows[2]['File']})
            media_files['File'] = rows[0]['File']
            media_files['uri'] = rows[0]['uri']
            media_files['format'] = rows[0]['format']
            return media_files

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
    dialog = OpenDialog()
    dialog.show()
    Gtk.main()
