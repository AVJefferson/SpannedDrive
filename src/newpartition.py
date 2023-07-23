# newpartition.py
#
# Copyright 2023 A V Jefferson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk

import os
import string
import shutil

from .utility import shorten, error_dialog, get_ui_path_from_filename
from .readwrite import Drive, Partition


@Gtk.Template(resource_path=get_ui_path_from_filename(__name__))
class SpannedDriveWindow(Adw.ApplicationWindow):
    __gtype_name__ = "SettingsWindow"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = kwargs["application"]
        self.quitable = (False, "Test")  # Test Addition, defaulted to (True, None)

