# This file is part of DroidCarve.
#
# Copyright (C) 2015, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pygtk

pygtk.require('2.0')
import gtk
import pango
from pygments.lexers import get_lexer_by_name
from pygments.styles.colorful import ColorfulStyle

STYLE = ColorfulStyle


class SourceCodeWindow(gtk.Window):

    def __init__(self, file_path, clazz_name):
        super(SourceCodeWindow, self).__init__()
        self.set_title(clazz_name)
        f = file(file_path)
        SOURCE = f.read()
        f.close()
        win = gtk.ScrolledWindow()
        self.add(win)
        self.textview = gtk.TextView()
        win.add(self.textview)
        buf = gtk.TextBuffer()

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
            if style['bold']:
                tag.set_property('weight', pango.WEIGHT_BOLD)
            if style['italic']:
                tag.set_property('style', pango.STYLE_ITALIC)
            if style['underline']:
                tag.set_property('underline', pango.UNDERLINE_SINGLE)

        self.connect('delete-event', lambda *a: gtk.main_quit())

        self.textview.set_buffer(buf)
        self.textview.set_editable(False)
        self.textview.modify_font(pango.FontDescription('consolas'))

        self.resize(800, 500)
        self.show_all()

    def run(self):
        gtk.main()
