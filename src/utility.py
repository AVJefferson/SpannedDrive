# utility.py
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

from os.path import isdir, exists
from os import mkdir
from gi.repository import Gtk


def error_dialog(parent, detail, message="Error"):
    dialog = Gtk.AlertDialog()

    dialog.set_message(message)
    dialog.set_detail(detail + "\nContact Developer for help.")

    dialog.set_buttons(["OK"])
    dialog.set_default_button(0)

    dialog.set_modal(True)
    dialog.show(parent=parent)


def is_allowed_text(valid, text, emptyallowed=False):
    if not emptyallowed and text == "":
        return False
    elif any(char not in valid for char in text):
        return False

    return True


def shorten(str, l):
    if len(str) > l:
        return str[: l // 2 - 1] + "..." + str[-l // 2 + 1 :]
    else:
        return str


def has_duplicate(lst):
    return len(lst) != len(set(lst))


def get_ui_path_from_filename(f):
    return "/org/avjeferson/SpannedDrive/gtk/" + f.split(".")[-1] + ".ui"
