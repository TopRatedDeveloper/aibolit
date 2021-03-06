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
from aibolit.patterns.method_chaining.method_chaining import MethodChainFind
from pathlib import Path


class TestMethodChain(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    method_chain_finder = MethodChainFind()

    def test_method_chain(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MethodChain.java'))
        assert len(lines) == 1

    def test_empty_method_chain(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'EmptyMethodChain.java'))
        assert len(lines) == 1

    def test_chain_with_new_object(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MethodChainNewObjectMethods.java'))
        assert len(lines) == 1

    def test_method_chain_in_different_methods(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MethodChainInDifferentMethods.java'))
        assert len(lines) == 2

    def test_chain_in_nested_class(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MethodChainNestedClass.java'))
        assert len(lines) == 1

    def test_chain_in_anonymous_class(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MethodChainAnonymousClass.java'))
        assert len(lines) == 1

    def test_chain_in_anonymous_class_empty(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MethodChainAnonymousClassEmpty.java'))
        assert len(lines) == 0

    def test_several_chains(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MethodChainSeveral.java'))
        assert len(lines) == 3

    def test_chain_without_object_creating(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'WithoutObjectCreating.java'))
        assert len(lines) == 1

    def test_nested_chain_with_this(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'NestedChainWIthThis.java'))
        assert len(lines) == 2

    def test_nested_chain_with_simple_method_invocation(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'NestedChainWithSimpleMethodInvocation.java'))
        assert len(lines) == 2

    def test_nested_chain_complicated_structure(self):
        """
        Several nested structures are checked: nested method chaining
        with nested anonymous classes
        """
        lines = self.method_chain_finder.value(Path(self.dir_path, 'HolyMolyNestedChain.java'))
        assert len(lines) == 3

    def test_smallest_chain(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'SmallestChain.java'))
        assert len(lines) == 1

    def test_fake_chain(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'FakeChain.java'))
        assert len(lines) == 0

    def test_many_chains(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'MachineLearningGetResultsIT.java'))
        assert len(lines) > 300
