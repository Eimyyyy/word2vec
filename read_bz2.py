#查看bz2中文本数据样式
import bz2file
with bz2file.open('zhwiki-20260301-pages-articles-multistream1.xml-p1p187712.bz2','rt',encoding='utf-8') as f:
    for i,line in enumerate(f,1):
        print(f"第{i}行:{line.strip()}")