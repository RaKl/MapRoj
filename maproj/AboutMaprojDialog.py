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

import logging
logger = logging.getLogger('maproj')

from maproj_lib.AboutDialog import AboutDialog

# See maproj_lib.AboutDialog.py for more details about how this class works.
class AboutMaprojDialog(AboutDialog):
    __gtype_name__ = "AboutMaprojDialog"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the about dialog"""
        super(AboutMaprojDialog, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.
        self.ui.label1.set_text('A simple program for playing with \ncartographic projections, reprojecting shapefiles \nand rendering an image with mapnik! \n NOT finished so far...3 weeks are not enough time for a noobie ;-)\nAdditional functions can be expected...')
        #self.ui.label1.set_justify('GTK_JUSTIFY_RIGHT')

