import os
import markdown
from fpdf import FPDF
from bs4 import BeautifulSoup

# 去除HTML标签
def strip_html(content):
    return '\n\n'.join(BeautifulSoup(content, "html.parser").stripped_strings)

# 将Markdown转换为文本
def markdown_to_text(md_content):
    html = markdown.markdown(md_content)
    return strip_html(html)

def md_to_pdf(md_dir, title, output_dir):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margin(20)

    # 添加Unicode字体（如果需要，替换为字体文件的路径）
    pdf.add_font('my_font', '', 'fonts/华文中宋.ttf')
    pdf.set_font('my_font', size=12)

    # 获取.md文件列表，并按数字排序
    md_files = [f for f in os.listdir(md_dir) if f.endswith('.md')]
    md_files.sort(key=lambda x: int(os.path.basename(x).split('-')[0]))

    # 遍历每个.md文件，并将其添加到PDF中
    for md_file in md_files:
        # 读取.md文件的内容
        file_path = os.path.join(md_dir, md_file)
        with open(file_path, encoding="utf-8") as file:
            md_content = file.read()

        # 为每个.md文件添加一个新页面
        pdf.add_page()

        # 设置正文字体
        pdf.set_font("my_font", size=12)

        # 将Markdown内容添加到PDF中
        pdf.multi_cell(0, 7, markdown_to_text(md_content))

    # 将PDF保存到输出目录
    output_pdf = os.path.join(output_dir, f"{title}.pdf")
    pdf.output(output_pdf)
    print(f"PDF file created: {output_pdf}")