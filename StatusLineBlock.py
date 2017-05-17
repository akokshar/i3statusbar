
"""
{
"full_text": "E: 10.0.0.1 (1000 Mbit/s)",
"short_text": "10.0.0.1",
"color": "#00ff00",
"background": "#1c1c1c",
"border": "#ee0000",
"min_width": 300,
"align": "right",
"urgent": false,
"name": "ethernet",
"instance": "eth0",
"separator": true,
"separator_block_width": 9
}
"""

class StatusLineBlock(object):

    def __init__(self, full_text):
        self.attr = {}
        self.full_text = full_text
        
        self.border_top = 0
        self.border_right = 0
        self.border_left = 0
        self.border_bottom = 3

    def __setAttr(self, name, value):
        if value is not None:
            self.attr[name] = value
        else:
            try:
                del self.attr[name]
            except:
                pass

    def __getAttr(self, name):
        #if self.attr.has_key(name):
        if name in self.attr:
            return self.attr[name]
        else:
            return None

    def getAttrs(self):
        return self.attr

    @property
    def full_text(self):
        return self.__getAttr("full_text")

    @full_text.setter
    def full_text(self, value):
        self.__setAttr("full_text", value)

    @property
    def short_text(self):
        return self.__getAttr("short_text")

    @short_text.setter
    def short_text(self, value):
        self.__setAttr("short_text", value)

    @property
    def min_width(self):
        return self.__getAttr("min_width")

    @min_width.setter
    def min_width(self, value):
        self.__setAttr("min_width", value)

    @property
    def align(self):
        return self.__getAttr("align")

    @align.setter
    def align(self, value):
        self.__setAttr("align", value)

    @property
    def separator(self):
        return self.__getAttr("separator")

    @separator.setter
    def separator(self, value):
        self.__setAttr("separator", value)

    @property
    def separator_block_width(self):
        return self.__getAttr("separator_block_width")

    @separator_block_width.setter
    def separator_block_width(self, value):
        self.__setAttr("separator_block_width", value)

    @property
    def color(self):
        return self.__getAttr("color")

    @color.setter
    def color(self, value):
        self.__setAttr("color", value)

    @property
    def name(self):
        return self.__getAttr("name")

    @name.setter
    def name(self, value):
        self.__setAttr("name", value)

    @property
    def instance(self):
        return self.__getAttr("instance")

    @instance.setter
    def instance(self, value):
        self.__setAttr("instance", str(value))

    @property
    def markup(self):
        self.__setAttr("markup", value)

    @markup.setter
    def markup(self, value):
        self.__setAttr("markup", str(value))

    @property
    def border(self):
        return self.__getAttr("border")

    @border.setter
    def border(self, value):
        self.__setAttr("border", value)

    @property
    def border_top(self):
        return self.__getAttr("border_top")

    @border_top.setter
    def border_top(self, value):
        self.__setAttr("border_top", value)

    @property
    def border_right(self):
        return self.__getAttr("border_right")

    @border.setter
    def border_right(self, value):
        self.__setAttr("border_right", value)

    @property
    def border_left(self):
        return self.__getAttr("border_left")

    @border.setter
    def border_left(self, value):
        self.__setAttr("border_left", value)

    @property
    def border_bottom(self):
        return self.__getAttr("border_bottom")

    @border.setter
    def border_bottom(self, value):
        self.__setAttr("border_bottom", value)
