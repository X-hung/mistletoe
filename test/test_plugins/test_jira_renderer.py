# Copyright 2018 Tile, Inc.  All Rights Reserved.
#
# The MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from unittest import TestCase, mock
from mistletoe.span_token import tokenize_inner
from plugins.jira_renderer import JIRARenderer
import random
import string

class TestJIRARenderer(TestCase):
    def setUp(self):
        self.renderer = JIRARenderer()
        self.renderer.__enter__()
        self.addCleanup(self.renderer.__exit__, None, None, None)

    # @mock.patch('mistletoe.span_token.RawText')
    # def test_parse(self, MockRawText):
    #     tokens = tokenize_inner('text with [[wiki | target]]')
    #     next(tokens)
    #     MockRawText.assert_called_with('text with ')
    #     token = next(tokens)
    #     self.assertIsInstance(token, GithubWiki)
    #     self.assertEqual(token.target, 'target')
    #     next(iter(token.children))
    #     MockRawText.assert_called_with('wiki')

    def genRandomString(self, n, hasWhitespace=False):
        source = string.ascii_letters + string.digits
        if hasWhitespace:
            source = source + ' \t'
        
        result = ''.join(random.SystemRandom().choice(source) for _ in range(n))
        return result

    def textFormatTest(self, inputTemplate, outputTemplate):
        input = self.genRandomString(80, True)
        token = next(tokenize_inner(inputTemplate.format(input)))
        expected = outputTemplate.format(input)
        actual = self.renderer.render(token)
        self.assertEqual(expected, actual)

    def test_render_strong(self):
        self.textFormatTest('**{}**', '*{}*')

    def test_render_emphasis(self):
        self.textFormatTest('*{}*', '_{}_')
        
    def test_render_inline_code(self):
        self.textFormatTest('`{}`', '{{{{{}}}}}')

    def test_render_strikethrough(self):
        self.textFormatTest('-{}-', '-{}-')

    def test_render_image(self):
        token = next(tokenize_inner('![image](foo.jpg)'))
        expected = '!foo.jpg!'
        actual = self.renderer.render(token)
        self.assertEqual(expected, actual)
    
    def test_render_footnote_image(self):
        # token = next(tokenize_inner('![image]\n\n[image]: foo.jpg'))
        # expected = '!foo.jpg!'
        # actual = self.renderer.render(token)
        # self.assertEqual(expected, actual)
        pass

    def test_render_link(self):
        url = 'http://{0}.{1}.{2}'.format(self.genRandomString(5), self.genRandomString(5), self.genRandomString(3))
        body = self.genRandomString(80, True)
        token = next(tokenize_inner('[{body}]({url})'.format(url=url, body=body)))
        expected = '[{body}|{url}]'.format(url=url, body=body)
        actual = self.renderer.render(token)
        self.assertEqual(expected, actual)
    
    def test_render_footnote_link(self):
        pass

    def test_render_auto_link(self):
        url = 'http://{0}.{1}.{2}'.format(self.genRandomString(5), self.genRandomString(5), self.genRandomString(3))
        token = next(tokenize_inner('<{url}>'.format(url=url)))
        expected = '[{url}]'.format(url=url)
        actual = self.renderer.render(token)
        self.assertEqual(expected, actual)
        
    def test_render_escape_sequence(self):
        pass

    def test_render_html_span(self):
        pass

    def test_render_heading(self):
        pass
        
    def test_render_quote(self):
        pass

    def test_render_paragraph(self):
        pass

    def test_render_block_code(self):
        pass

    def test_render_list(self):
        pass

    def test_render_list_item(self):
        pass

    def test_render_inner(self):
        pass

    def test_render_table(self):
        pass

    def test_render_table_row(self):
        pass

    def test_render_table_cell(self):
        pass

    def test_render_separator(self):
        pass

    def test_render_html_block(self):
        pass

    def test_render_document(self):
        pass
    
    


    
    
