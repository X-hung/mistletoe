from unittest import TestCase, mock
from mistletoe.html_renderer import HTMLRenderer


class TestRenderer(TestCase):
    def setUp(self):
        self.renderer = HTMLRenderer()
        self.renderer.render_inner = mock.Mock(return_value='inner')
        self.renderer.__enter__()
        self.addCleanup(self.renderer.__exit__, None, None, None)

    def _test_token(self, token_name, output, children=True, **kwargs):
        render_func = self.renderer.render_map[token_name]
        children = mock.MagicMock() if children else None
        mock_token = mock.Mock(children=children, **kwargs)
        self.assertEqual(render_func(mock_token), output)


class TestHTMLRenderer(TestRenderer):
    def test_strong(self):
        self._test_token('Strong', '<strong>inner</strong>')

    def test_emphasis(self):
        self._test_token('Emphasis', '<em>inner</em>')

    def test_inline_code(self):
        self._test_token('InlineCode', '<code>inner</code>')

    def test_strikethrough(self):
        self._test_token('Strikethrough', '<del>inner</del>')

    def test_image(self):
        output = '<img src="src" title="title" alt="inner">'
        self._test_token('Image', output, src='src', title='title')

    def test_link(self):
        output = '<a href="target">inner</a>'
        self._test_token('Link', output, target='target')

    def test_autolink(self):
        output = '<a href="link">inner</a>'
        self._test_token('AutoLink', output, target='link')

    def test_escape_sequence(self):
        self._test_token('EscapeSequence', 'inner')

    def test_raw_text(self):
        self._test_token('RawText', 'john &amp; jane',
                         children=False, content='john & jane')

    def test_html_span(self):
        self._test_token('HTMLSpan', '<some>text</some>',
                         children=False, content='<some>text</some>')

    def test_heading(self):
        output = '<h3>inner</h3>\n'
        self._test_token('Heading', output, level=3)

    def test_quote(self):
        output = '<blockquote>\ninner</blockquote>\n'
        self._test_token('Quote', output)

    def test_paragraph(self):
        self._test_token('Paragraph', '<p>inner</p>\n')

    def test_block_code(self):
        output = '<pre>\n<code class="lang-sh">\ninner</code>\n</pre>\n'
        self._test_token('BlockCode', output, language='sh')

    def test_block_code_no_language(self):
        output = '<pre>\n<code>\ninner</code>\n</pre>\n'
        self._test_token('BlockCode', output, language='')

    def test_list(self):
        output = '<ul>\ninner</ul>\n'
        self._test_token('List', output, start=None)

    def test_list_item(self):
        output = '<li>inner</li>\n'
        self._test_token('ListItem', output)

    def test_table_with_heading(self):
        func_path = 'mistletoe.html_renderer.HTMLRenderer.render_table_row'
        with mock.patch(func_path, autospec=True) as mock_func:
            mock_func.return_value = 'row'
            output = ('<table>\n'
                        '<thead>\nrow</thead>\n'
                        '<tbody>\ninner</tbody>\n'
                      '</table>\n')
            self._test_token('Table', output, has_header=True)

    def test_table_without_heading(self):
        func_path = 'mistletoe.html_renderer.HTMLRenderer.render_table_row'
        with mock.patch(func_path, autospec=True) as mock_func:
            mock_func.return_value = 'row'
            output = '<table>\n<tbody>\ninner</tbody>\n</table>\n'
            self._test_token('Table', output, has_header=False)

    def test_table_row(self):
        self._test_token('TableRow', '<tr>\n</tr>\n')

    def test_table_cell(self):
        output = '<td align="left">inner</td>\n'
        self._test_token('TableCell', output, align=None)

    def test_separator(self):
        self._test_token('Separator', '<hr>\n', children=False)

    def test_html_block(self):
        content = output = '<h1>hello</h1>\n<p>this is\na paragraph</p>\n'
        self._test_token('HTMLBlock', output,
                         children=False, content=content)

    def test_document(self):
        self._test_token('Document', 'inner', footnotes={})


class TestHTMLRendererFootnotes(TestCase):
    def setUp(self):
        self.renderer = HTMLRenderer()
        self.renderer.__enter__()
        self.addCleanup(self.renderer.__exit__, None, None, None)

    def test_footnote_image(self):
        from mistletoe import Document
        token = Document(['![alt] [foo]\n', '\n', '[foo]: bar "title"\n'])
        output = '<p><img src="bar" title="title" alt="alt">\n</p>\n'
        self.assertEqual(self.renderer.render(token), output)

    def test_footnote_link(self):
        from mistletoe import Document
        token = Document(['[name] [foo]\n', '\n', '[foo]: target\n'])
        output = '<p><a href="target">name</a>\n</p>\n' 
        self.assertEqual(self.renderer.render(token), output)
