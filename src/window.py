# window.py
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

from .utility import shorten, error_dialog, get_ui_path_from_filename

import time
import os


@Gtk.Template(resource_path=get_ui_path_from_filename(__name__))
class SpannedDriveWindow(Adw.ApplicationWindow):
    __gtype_name__ = "SpannedDriveWindow"

    search = Gtk.Template.Child("search")

    listbox_partitions = Gtk.Template.Child("listbox_partitions")
    button_new_partition = Gtk.Template.Child("button_new_partition")

    box_path = Gtk.Template.Child("box_path")
    label_current_partition = Gtk.Template.Child("label_current_partition")
    flowbox_storage = Gtk.Template.Child("flowbox_storage")
    label_partition_info = Gtk.Template.Child("label_partition_info")
    progress_partition = Gtk.Template.Child("progress_partition")

    listbox_drives = Gtk.Template.Child("listbox_drives")
    box_drive_primary = Gtk.Template.Child("box_drive_primary")
    button_new_drive = Gtk.Template.Child("button_new_drive")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = kwargs["application"]
        self.quitable = (False, "Test")  # Test Addition, defaulted to (True, None)

        # Headerbar
        self.search.connect("search-changed", self.on_search_changed)
        self.search.connect("stop-search", self.on_stop_search)

        # Partitions Pane
        # self.partition_button[i].connect("clicked", self.on_button_partition_clicked)
        self.button_new_partition.connect(
            "clicked", self.on_button_new_partition_clicked
        )

        self.listbox_partitions.remove_all()
        for r in self.app.partitions.get("entries"):
            b = Gtk.Button(
                os.path.basename(r[1][: -len(SbmFile.extension)]).replace("_", " ")
            )

            setattr(b, "loc", r[1])
            setattr(b, "hash", r)

            b.connect("clicked", self.on_button_partition_clicked)
            b.show()

        # Storage Pane
        # self.label_current_partition.set_text("No Partition Selected")
        # l = Gtk.Label()
        # l.set_text("Get Started by Creating/Opening a Partition")
        # l.set_halign(Gtk.Align.CENTER)
        # l.set_valign(Gtk.Align.CENTER)
        # l.set_hexpand(True)
        # l.set_vexpand(True)
        # self.flowbox_storage.append(l)
        # self.label_partition_info.set_text("No Partition Selected")
        # self.progress_partition.set_fraction(0.0)

        # Drives Pane
        self.button_new_drive.connect("clicked", self.on_button_new_drive_clicked)

    def on_search_changed(self, search, text):
        return

    def on_stop_search(self, search):
        return

    def on_button_partition_clicked(self, button):
        return

    def on_button_new_partition_clicked(self, button):
        return

    def on_button_new_drive_clicked(self, button):
        return
