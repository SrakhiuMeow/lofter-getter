def comments2md(comments_list, hot_list):
    c_md = ''
    hot_md = ''

    hot_md += '\n\n---\n'
    hot_md += '#### 热门评论\n\n'
    for comment in hot_list:
        nickname = comment['publisherBlogInfo']['blogNickName']
        bloghome = 'https://' + comment['publisherBlogInfo']['blogName'] + '.lofter.com'
        if 'quote' not in comment:
            hot_md += f"- [{nickname}]({bloghome}): \n\n\t{comment['content']}\n"
        else:
            quote = comment['quote']
            hot_md += f"- [{nickname}]({bloghome}): \n\n\t```\n\t{quote}\n\t```\n\n\t{comment['content']}\n"

    c_md += '\n\n---\n'
    c_md += '#### 所有评论\n\n'
    c_md += '<details><summary>展开</summary><p>\n\n'

    for comment in comments_list:
        nickname = comment['publisherBlogInfo']['blogNickName']
        bloghome = 'https://' + comment['publisherBlogInfo']['blogName'] + '.lofter.com'
        if "quote" not in comment:
            c_md += f"- [{nickname}]({bloghome}): \n\n\t {comment['content']}\n"
        else:
            quote = comment['quote']
            c_md += f"- [{nickname}]({bloghome}): \n\n\t```\n\t{quote}\n\t```\n\n\t{comment['content']}\n"

        if comment['l2Comments'] > 0:
            # TODO: 还需要再获取一次二级评论，否则只能显示默认展示出来的评论
            ...

            c_md += '\t<details><summary>展开</summary><p>\n\n'
            for l2c in comment['l2Comments']:
                nickname = l2c['publisherBlogInfo']['blogNickName']
                bloghome = 'https://' + l2c['publisherBlogInfo']['blogName'] + '.lofter.com'
                c_md += f"\t- [{nickname}]({bloghome}):  {l2c['content']}\n"
                
            c_md += '\t\n</p></details>\n'

    c_md += '\n</p></details>\n'

    return hot_md + c_md
