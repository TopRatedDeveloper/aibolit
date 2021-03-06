# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from unittest import TestCase
from aibolit.patterns.this_finder.this_finder import ThisFinder


class TestFindThis(TestCase):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    pattern = ThisFinder()

    def test_several(self):
        lines = self.pattern.value(self.cur_dir + '/several.java')
        assert lines == [4, 10, 20]

    def test_simple1(self):
        lines = self.pattern.value(self.cur_dir + '/double_this.java')
        assert lines == [12]

    def test_simple2(self):
        lines = self.pattern.value(self.cur_dir + '/init_block.java')
        assert lines == []

    def test_simple22(self):
        lines = self.pattern.value(self.cur_dir + '/init_static_block.java')
        assert lines == []

    def test_simple3(self):
        lines = self.pattern.value(self.cur_dir + '/autocloseable.java')
        assert lines == [4]

    def test_simple4(self):
        lines = self.pattern.value(self.cur_dir + '/one_line_this.java')
        assert lines == [11]

    def test_simple5(self):
        lines = self.pattern.value(self.cur_dir + '/one_line_usage.java')
        assert lines == [12]

    def test_simple6(self):
        lines = self.pattern.value(self.cur_dir + '/super.java')
        assert lines == []

    def test_simple7(self):
        lines = self.pattern.value(self.cur_dir + '/holy_moly_constructor.java')
        assert lines == []
