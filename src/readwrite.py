from time import time
import json
import os
import logging

from .gconstants import SOFTWARE_VERSION, FILECHARACTERISTICSFOLDER

from gi.repository import Gio, GLib


class Location(str):
    basepath = ""

    def __new__(cls, path: str):
        rpath = path
        relative = False

        if rpath is None:
            rpath = ""

        if cls.basepath == "":
            return

        if rpath.startswith(cls.basepath):
            # Can Be Converted To Relative Path
            relative = True
            rpath = path[len(cls.basepath) :]

            if rpath.startswith("/"):
                rpath = rpath[1:]

        elif not rpath.startswith("/"):
            # Is Already Relative Path
            relative = True

        obj = str.__new__(cls, rpath)
        obj.relative = relative
        return obj

    def abs(self):
        if self.relative:
            return self.basepath + super().__str__()
        return super().__str__()


def get_fileclass_properties(classname):
    try:
        # Read the data characteristics from the file
        characteristicspath = FILECHARACTERISTICSFOLDER + classname + ".json"

        byte_array = Gio.resources_lookup_data(
            characteristicspath, Gio.ResourceLookupFlags.NONE
        )
        json_string = byte_array.get_data().decode("utf-8")

        d = json.loads(json_string)
        t = d["datatype"]

        for k in t:
            v = t[k]
            if v["type"] == "str":
                v["type"] = str
            elif v["type"] == "int":
                v["type"] = int
            elif v["type"] == "float":
                v["type"] = float
            elif v["type"] == "bool":
                v["type"] = bool
            elif v["type"] == "list":
                v["type"] = list
            elif v["type"] == "dict":
                v["type"] = dict
            elif v["type"] == "set":
                v["type"] = set
            elif v["type"] == "frozenset":
                v["type"] = frozenset
            elif v["type"] == "complex":
                v["type"] = complex
            elif v["type"] == "location":
                v["type"] = Location
            else:
                v["type"] = None

        return d["version"], d["datatype"], d["extension"], d["autosave"]
    except GLib.Error as e:
        print("Error in get_fileclass_properties", e)
        return "1.0", dict(), "", False


class File:
    autosave = False

    def __repr__(self):
        return self.loc

    def __str__(self):
        return self.loc

    def put(self, k, v):
        self.data[k] = v

    def get(self, k):
        return self.data[k]

    def __init__(self, loc: str):
        self.loc = loc
        if not loc.startswith("/"):
            # Relative Path
            self.loc = Location.basepath + loc
            print("using absolute path", self.loc)
        self.data = dict()
        self.dirty = False
        return

    def valid_file_extension(self):
        return self.loc.endswith(self.extension)

    def read(self):
        with open(self.loc, "r") as f:
            self.data = json.load(f)
            self.data["lastopened"] = time()
            self.dirty = True
        return True

    def write(self, overwrite=False):
        if overwrite:
            with open(self.loc, "w") as f:
                self.data["lastmodified"] = time()
                json.dump(self.data, f, indent=4)
        else:
            if not os.path.exists(self.loc):
                with open(self.loc, "w") as f:
                    self.data["creationtime"] = self.data["lastmodified"] = time()
                    json.dump(self.data, f, indent=4)
            else:
                return False
        self.dirty = False
        return True

    def __del__(self):
        if self.autosave and self.dirty:
            # Unsaved Content in File
            self.write(overwrite=True)


class ConfigurationFile(File):
    version, datatype, extension, autosave = get_fileclass_properties(
        "ConfigurationFile"
    )

    def put(self, k, v):
        if k not in self.datatype:
            # Adding Data without Data Validation
            super().put(k, v)
        else:
            # Attempting Data Conversion
            try:
                super().put(k, self.datatype[k]["type"](v))
            except Exception as e:
                # Data Conversion Failed
                print("Data Conversion Failed in", self, e)

    def get(self, k):
        if k in self.__dict__:
            return self.__dict__[k]
        return super().get(k)

    def __init__(self, loc: str, **kwargs):
        super().__init__(loc)

        iter = list(kwargs.keys()) + list(self.datatype.keys())

        # Setting Default and provided Values in data
        for k in iter:
            self.put(k, kwargs.get(k, self.datatype[k]["def"]))
        return


class RecentsFile(File):
    version, datatype, extension, autosave = get_fileclass_properties("RecentsFile")

    def put(self, k, v):
        if k not in self.datatype:
            # Adding Data without Data Validation
            super().put(k, v)
        else:
            # Attempting Data Conversion
            try:
                super().put(k, self.datatype[k]["type"](v))
            except Exception as e:
                # Data Conversion Failed
                print("Data Conversion Failed in type", self.datatype[k], self, e)

    def get(self, k):
        if k in self.__dict__:
            return self.__dict__[k]
        return super().get(k)

    def __init__(self, loc: str, **kwargs):
        super().__init__(loc)

        iter = list(kwargs.keys()) + list(self.datatype.keys())
        for k in self.datatype.keys():
            self.put(k, self.datatype[k]["def"])

        for k in kwargs:
            self.put(k, **kwargs[k])
        return

    def sort(self, reverse=True):
        super().get("entries").sort(key=lambda x: int(x[0]), reverse=reverse)

    def add(self, val: str, timestamp=time(), setprevious=True, sort=True):
        super().get("entries").append([timestamp, val])

        if sort:
            self.sort(reverse=True)
        if setprevious:
            super().put("previous", (timestamp, val))
        return

    def update(self, val: str, timestamp=time(), sort=True):
        lst = super().get("entries")
        [lst.remove(x) for x in lst if x[1] == val]
        lst.append([timestamp, val])

        if sort:
            self.sort(reverse=True)
        return

    def discard(self, hash_value=False):
        try:
            return super().get("entries").remove(hash_value)
        except:
            print("Hash Value not found in Recents File")
            return False


class DriveFile(File):
    version, datatype, extension, autosave = get_fileclass_properties("DriveFile")

    def put(self, k, v):
        if k not in self.datatype:
            # Adding Data without Data Validation
            super().put(k, v)
        else:
            # Attempting Data Conversion
            try:
                super().put(k, self.datatype[k]["type"](v))
            except Exception as e:
                # Data Conversion Failed
                print("Data Conversion Failed in", self, e)

    def get(self, k):
        if k in self.__dict__:
            return self.__dict__[k]
        return super().get(k)

    def __init__(self, loc: str, **kwargs):
        super().__init__(loc)

        iter = list(kwargs.keys()) + list(self.datatype.keys())

        # Setting Default and provided Values in data
        for k in iter:
            self.put(k, kwargs.get(k, self.datatype[k]["def"]))
        return


class TokenFile(File):
    version, datatype, extension, autosave = get_fileclass_properties("TokenFile")

    def put(self, k, v):
        if k not in self.datatype:
            # Adding Data without Data Validation
            super().put(k, v)
        else:
            # Attempting Data Conversion
            try:
                super().put(k, self.datatype[k]["type"](v))
            except Exception as e:
                # Data Conversion Failed
                print("Data Conversion Failed in", self, e)

    def get(self, k):
        if k in self.__dict__:
            return self.__dict__[k]
        return super().get(k)

    def __init__(self, loc: str, **kwargs):
        super().__init__(loc)

        iter = list(kwargs.keys()) + list(self.datatype.keys())

        # Setting Default and provided Values in data
        for k in iter:
            self.put(k, kwargs.get(k, self.datatype[k]["def"]))
        return


class PartitionFile(File):
    version, datatype, extension, autosave = get_fileclass_properties("PartitionFile")

    def put(self, k, v):
        if k not in self.datatype:
            # Adding Data without Data Validation
            super().put(k, v)
        else:
            # Attempting Data Conversion
            try:
                super().put(k, self.datatype[k]["type"](v))
            except Exception as e:
                # Data Conversion Failed
                print("Data Conversion Failed in", self, e)

    def get(self, k):
        if k in self.__dict__:
            return self.__dict__[k]
        return super().get(k)

    def __init__(self, loc: str, **kwargs):
        super().__init__(loc)

        iter = list(kwargs.keys()) + list(self.datatype.keys())

        # Setting Default and provided Values in data
        for k in iter:
            self.put(k, kwargs.get(k, self.datatype[k]["def"]))
        return
