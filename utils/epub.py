import os
import markdown
from ebooklib import epub

def md_to_epub(md_dir, title, output_dir, author=None):
    # 创建一本新的EPUB书籍
    book = epub.EpubBook()

    # 设置元数据
    book.set_title(title)
    if author:
        book.add_author(author)

    # 将语言设置为简体中文
    book.set_language('zh-CN')

    # 获取目录中的所有.md文件，并按数字顺序排序
    md_files = [f for f in os.listdir(md_dir) if f.endswith('.md')]
    md_files.sort(key=lambda x: int(x.split('-')[0]))

    # 添加书脊和目录
    book.spine = ['nav']
    chapters = []

    # 读取每个Markdown文件并转换为HTML，然后作为章节添加
    for md_file in md_files:
        file_path = os.path.join(md_dir, md_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            md_content = file.read()
            html_content = markdown.markdown(md_content)

            # 为每个Markdown文件创建一个EPUB章节
            chapter_title = md_file.replace('.md', '').split("-")[-1]
            chapter = epub.EpubHtml(title=chapter_title, file_name=f"{chapter_title}.xhtml", lang='zh-CN')
            chapter.content = f"<h1>{chapter_title}</h1>{html_content}"

            book.add_item(chapter)
            chapters.append(chapter)

    # 将章节添加到书脊中
    book.spine += chapters

    # 创建目录
    toc = [(epub.Section('Chapters'), chapters)]
    book.toc = toc

    # 添加导航文件
    book.add_item(epub.EpubNav())

    # 存入EPUB文件
    epub_filename = os.path.join(output_dir, f"{title}.epub")
    epub.write_epub(epub_filename, book)
    print(f"EPUB file created: {epub_filename}")
