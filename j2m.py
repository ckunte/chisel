import markdown
from jinja2.nodes import CallBlock
from jinja2.ext import Extension


class MarkdownExtension(Extension):
    tags = {'markdown'}

    def __init__(self, environment):
        super().__init__(environment)
        md = markdown.Markdown(extensions=("smarty", "fenced_code"))
        environment.extend(markdowner=md)
        self._markdowner = md

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(
            ['name:endmarkdown'],
            drop_needle=True
        )
        return CallBlock(
            self.call_method('_markdown_support'),
            [],
            [],
            body
        ).set_lineno(lineno)

    def _markdown_support(self, caller):
        block = caller()
        if '\n' in block:
            block = self._strip_whitespace(block)
        return self._markdowner.convert(block)

    def _strip_whitespace(self, block):
        lines = block.splitlines()
        if len(lines) <= 1:
            return block.strip()

        ws = lines[1][:len(lines[1]) - len(lines[1].lstrip(' \t'))]

        stripped = [
            line[len(ws):] if line.startswith(ws) else line
            for line in lines
        ]

        return '\n'.join(stripped).strip()

