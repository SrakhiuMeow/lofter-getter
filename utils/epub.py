import os
import re

import markdown
from ebooklib import epub


def md_to_epub(md_dir, title, output_dir, author=None):
    # 创建一本新的EPUB书籍
    book = epub.EpubBook()

    # 设置元数据
    book.set_identifier(f'collection-{abs(hash(title)) & 0xffffffff:08x}')
    book.set_title(title)
    if author:
        book.add_author(author)

    # 将语言设置为简体中文
    book.set_language('zh-CN')

    # 获取目录中的所有.md文件，并按数字顺序排序
    md_files = [f for f in os.listdir(md_dir) if f.endswith('.md')]

    def _sort_key(name):
        m = re.match(r'^(\d+)-', name)
        return int(m.group(1)) if m else 10**9

    md_files.sort(key=_sort_key)

    chapters = []

    # 读取每个Markdown文件并转换为HTML，然后作为章节添加
    for idx, md_file in enumerate(md_files):
        file_path = os.path.join(md_dir, md_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            md_content = file.read()
            html_content = markdown.markdown(md_content)

            # 显示标题用原文件名；文件名用序号，避免特殊字符导致 EPUB 失败
            chapter_title = md_file.replace('.md', '')
            if '-' in chapter_title:
                chapter_title = chapter_title.split('-', 1)[-1] or chapter_title
            fname = f'chapter_{idx + 1}.xhtml'
            chapter = epub.EpubHtml(title=chapter_title, file_name=fname, lang='zh-CN')
            chapter.content = f"<h1>{chapter_title}</h1>{html_content}"

            book.add_item(chapter)
            chapters.append(chapter)

    if not chapters:
        raise RuntimeError('合集目录下没有可写入 EPUB 的 Markdown')

    # nav 不进 spine，避免部分阅读器打开空白
    book.spine = chapters
    book.toc = tuple(epub.Link(ch.file_name, ch.title, f'ch{i + 1}') for i, ch in enumerate(chapters))
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # 存入EPUB文件
    epub_filename = os.path.join(output_dir, f"{title}.epub")
    try:
        epub.write_epub(epub_filename, book, {'ignore_ncx': False, 'epub3_pages': False})
    except TypeError:
        epub.write_epub(epub_filename, book)
    print(f"EPUB file created: {epub_filename}")
