# main.py
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

import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Gio, Adw
from .utility import error_dialog
from .window import SpanneddriveWindow
from .gconstants import SOFTWARE_VERSION


class SpanneddriveApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="org.avjeferson.SpannedDrive",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.create_action("quit", self.on_quit_action, ["<primary>q"])
        self.create_action("about", self.on_about_action)
        self.create_action("preferences", self.on_preferences_action)

    def do_activate(self):
        """
        Called when the application is activated.
        We raise the application's main window, creating it if necessary.
        """

        win = self.props.active_window
        if not win:
            win = SpanneddriveWindow(application=self)
        win.present()
        # win.set_keep_above(True)

    def on_quit_action(self, widget, _):
        quitable = True
        errorwindow = None
        for window in self.get_windows():
            if not window.quitable[0]:
                quitable = False
                reason = window.quitable[1]
                errorwindow = window
                break

        if quitable:
            self.quit()

        def callback(source, async_res):
            response = source.choose_finish(async_res)

            if response == 0:
                self.quit()
            elif response == 1:
                error_dialog(errorwindow, "This feature is not implemented yet")
                pass

        dialog = Gtk.AlertDialog()

        dialog.set_message("Quit?")
        dialog.set_detail("Are you sure you want to quit?\nReason: " + str(reason))

        dialog.set_buttons(["Quit Now", "Quit After Finish", "Cancel"])
        dialog.set_default_button(2)

        dialog.set_modal(True)
        dialog.choose(errorwindow, None, callback)

    def on_about_action(self, widget, _):
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="Spanned Drive",
            application_icon="org.avjeferson.SpannedDrive",
            developer_name="A V Jefferson",
            version=SOFTWARE_VERSION,
            developers=["A V Jefferson <avjeferson@gmail.com>"],
            copyright="© 2023 A V Jefferson",
            comments="A tool to span a single folder across multiple drives.",
        )
        about.present()

    def on_preferences_action(self, widget, _):
        preferences = Adw.PreferencesWindow(
            transient_for=self.props.active_window,
            application=self,
            title="Preferences",
            modal=True,
        )
        preferences.present()


    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.
        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    app = SpanneddriveApplication()
    return app.run(sys.argv)
