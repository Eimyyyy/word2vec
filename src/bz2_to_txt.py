#将bz2文件转成txt文件
import bz2file
import codecs
import os
import re

def convert_to_plain_text(bz2_path, txt_path):

    with bz2file.open(bz2_path, 'rt', encoding='utf-8') as bz2_file:
        content = bz2_file.read()

    # 移除XML声明
    content = re.sub(r'<\?xml[^>]+\?>', '', content)
    #移除所有XML标签
    content = re.sub(r'<[^>]+>', '', content)
    #移除多余的空行
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    #移除控制字符
    content = ''.join(char for char in content if ord(char) >= 32 or char == '\n' or char == '\t')
    # 使用codecs确保UTF-8编码
    with codecs.open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(content)

    print(f"纯文本文件已保存: {txt_path}")
    print(f"文件大小: {os.path.getsize(txt_path) / (1024 * 1024):.2f} MB")


convert_to_plain_text(
    "zhwiki-20260301-pages-articles-multistream1.xml-p1p187712.bz2",
    "wiki_plain_text.txt"
)
