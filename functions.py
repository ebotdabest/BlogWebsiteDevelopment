import re

import re

class MarkdownToHTML:
    def __init__(self):
        self.formatters = [
            (r'\[lb\]', r'<br>'),
            (r'\*\*(.*?)\*\*', r'<b>\1</b>'),
            (r'\*(.*?)\*', r'<i>\1</i>'),
            (r'\_\_(.*?)\_\_', r'<under>\1</under>'),
            (r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>'),
            (r'\((.*?)\)\[(.*?)\]', r'<img src="\2" alt="\1">'),  # updated image format
            (r'^#\s(.*?)$', r'<h1>\1</h1>'),
            (r'^##\s(.*?)$', r'<h2>\1</h2>'),
            (r'^###\s(.*?)$', r'<h3>\1</h3>'),
            (r'^####\s(.*?)$', r'<h4>\1</h4>'),
            (r'^#####\s(.*?)$', r'<h5>\1</h5>'),
            (r'^######\s(.*?)$', r'<h6>\1</h6>'),
            (r'^-\s(.*?)$', r'<li>\1</li>'),
            (r'^\[\s\](.*?)$', r'<li>\1</li>'),
        ]

    def parse_list(self, list_text):
        list_lines = list_text.split('\n')
        if len(list_lines) > 1:  # only remove the last item if there are more than one
            list_lines.pop()
        return '\n'.join(list_lines)

    def parse_table(self, table_text, table_classes):
        table_lines = table_text.split('\n')
        if len(table_lines) > 1:  # only remove the last row if there are more than one
            table_lines.pop()
        max_columns = max(len(line.split(',')) for line in table_lines)

        # Add all table classes
        html = f'<table class="{" ".join(table_classes)}">\n'
        for line in table_lines:
            columns = line.split(',')
            columns.extend([''] * (max_columns - len(columns)))  # Pad shorter rows with empty cells
            html += '<tr>' + ''.join(f'<td>{self.format_text(col)}</td>' for col in columns) + '</tr>\n'
        html += '</table>'
        return html

    def format_text(self, text):
        for regex, replacement in self.formatters:
            text = re.sub(regex, replacement, text)
        return text

    def markdown_to_html(self, markdown):
        html = ''
        in_table = False
        in_list = False
        table_text = ''
        list_text = ''
        table_classes = ''

        for line in markdown.split('\n'):
            if '[table:' in line.strip():
                in_table = True
                table_classes = line.strip().split(':')[1].split(']')[0].split(',') # extract table classes
                continue
            if line.strip() == '[/table]':
                in_table = False
                html += self.parse_table(table_text, table_classes)
                table_text = ''
                table_classes = ''
                continue
            if in_table:
                table_text += line + '\n'
                continue

            if '- ' in line or '[ ]' in line:
                in_list = True
                list_text += line + '\n'
                continue
            if in_list:
                in_list = False
                html += self.parse_list(list_text)
                list_text = ''
                continue

            for regex, replacement in self.formatters:
                line = re.sub(regex, replacement, line)
            html += line + '<br>'
        return html
# if __name__ == "__main__":
#     markdown_text = """# Hello, World!
# **This is bold text.**
# *This is italic text.*
# This is a [link](https://www.example.com/).
# This is an image: ![alt text](https://www.example.com/image.jpg)
# - This is an unordered list item.
# [table]
# Column1,Column2,Column3
# Data1,Data2,Data3
# Data4,Data5,Data6
# [/table]
# """
#     converter = MarkdownToHTML()
#     print(converter.markdown_to_html(markdown_text))