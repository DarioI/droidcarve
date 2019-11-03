# This file is part of DroidCarve.
#
# Copyright (C) 2019, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from pygments.lexers import get_lexer_by_name
from pygments.styles.colorful import ColorfulStyle

STYLE = ColorfulStyle


class SourceCodeWindow:

    def __init__(self, file_path, clazz_name):
        self.win = Gtk.Window()
        self.win.set_title(clazz_name)
        f = open(file_path, 'r')
        SOURCE = f.read()
        f.close()
        self.scrolledwin = Gtk.ScrolledWindow()
        self.win.add(self.scrolledwin)
        self.textview = Gtk.TextView()
        self.scrolledwin.add(self.textview)
        buf = Gtk.TextBuffer()

        styles = {}
        for token, value in get_lexer_by_name("smali", stripall=True).get_tokens(SOURCE):
            while not STYLE.styles_token(token) and token.parent:
                token = token.parent
            if token not in styles:
                styles[token] = buf.create_tag()
            start = buf.get_end_iter()
            buf.insert_with_tags(start, value.encode('utf-8'), styles[token])

        for token, tag in styles.iteritems():
            style = STYLE.style_for_token(token)
            if style['bgcolor']:
                tag.set_property('background', '#' + style['bgcolor'])
            if style['color']:
                tag.set_property('foreground', '#' + style['color'])

        self.win.connect("destroy", Gtk.main_quit)

        self.textview.set_buffer(buf)
        self.textview.set_editable(False)

        self.win.resize(800, 500)
        self.win.show_all()

    def run(self):
        Gtk.main()
