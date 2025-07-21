import re

def replace(s, old, new):
    # 批量替换

    if isinstance(old, str):
        return s.replace(old, new)
    elif isinstance(old, list) and isinstance(new, str):
        for o in old:
            s = s.replace(o, new)
        return s
    elif isinstance(old, list) and isinstance(new, list):
        for i, o in enumerate(old):
            s = s.replace(o, new[i])
        return s

def make_valid_filename(filename):
    # 替换非法字符，用于文件名

    filename = replace(filename, '"', '\'')

    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    filename = replace(filename, invalid_chars, '_')

    filename.replace(' ', '')
    
    return filename

def escape_for_url(s):
    # 替换URL中的特殊字符，用于 markdown 链接

    old = ['%', ' ', '#', '&','(', ')', 
           '+', ',', '/', ':', ';', '=', 
           '?', '@', '[', ']']
    new = ['%25', '%20', '%23', '%26', '%28', '%29', 
           '%2B', '%2C', '%2F', '%3A', '%3B', '%3D', 
           '%3F', '%40', '%5B', '%5D']
    s = replace(s, old, new)
    return s

def html2md(content):
    # 将Lofter原生的HTML内容转换为markdown格式

    # 去除多余标签
    pattern = re.compile(r'<p id=".*"  >')
    content = re.sub(pattern, '', content)
    content = content.replace('</p>', '')
    content = content.replace('　　', '')
    content = content.replace(' \n', '\n')
    content = content.replace('&nbsp;', ' ')
    content = content.replace('<br /> ', '')


    # 调整为markdown格式
    pattern = re.compile(r'——*—\n')
    content = re.sub(pattern, '\n---\n\n', content)
    pattern = re.compile(r'(.)\n(.)')
    content = re.sub(pattern, r'\1\n\n\2', content)

    return content
