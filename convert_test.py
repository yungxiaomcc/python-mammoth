#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
转换 test.docx 并显示详细信息
"""

import sys
sys.path.insert(0, '/home/xiaoyang/for-play/python-mammoth')

import mammoth
from mammoth import docx

def analyze_and_convert():
    """分析并转换 test.docx"""
    
    print("=" * 80)
    print("转换 test.docx 文档")
    print("=" * 80)
    print()
    
    # 读取 docx 文档结构
    print("📖 第一步：读取文档并分析段落结构")
    print("-" * 80)
    
    with open("test.docx", "rb") as docx_file:
        document = docx.read(docx_file)
        
        # 遍历所有段落，显示其属性
        paragraph_count = 0
        for element in document.value.children:
            if hasattr(element, 'style_id'):  # 是段落
                paragraph_count += 1
                text_content = ""
                for child in element.children:
                    if hasattr(child, 'children'):  # run
                        for text_elem in child.children:
                            if hasattr(text_elem, 'value'):
                                text_content += text_elem.value
                    elif hasattr(child, 'value'):  # text
                        text_content += child.value
                
                # 截断过长的文本
                if len(text_content) > 60:
                    text_preview = text_content[:60] + "..."
                else:
                    text_preview = text_content
                
                if text_content:  # 只显示非空段落
                    print(f"\n段落 {paragraph_count}:")
                    print(f"  文本: {text_preview}")
                    print(f"  样式ID: {element.style_id}")
                    print(f"  样式名称: {element.style_name}")
                    print(f"  大纲层级: {element.outline_level}")
                    
                    # 预测会转换成什么标签
                    if element.outline_level is not None:
                        try:
                            level = int(element.outline_level)
                            if 0 <= level <= 5:
                                print(f"  ✓ 预期转换: <h{level + 1}> (基于大纲层级)")
                            else:
                                print(f"  ✓ 预期转换: <p> (大纲层级超出范围)")
                        except:
                            print(f"  ✓ 预期转换: <p> (无效的大纲层级)")
                    elif element.style_id or element.style_name:
                        print(f"  ✓ 预期转换: 根据样式映射")
                    else:
                        print(f"  ✓ 预期转换: <p> (普通段落)")
    
    print("\n" + "=" * 80)
    print("📝 第二步：执行转换")
    print("-" * 80)
    
    # 转换文档
    with open("test.docx", "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
    
    # 显示转换结果
    print("\n转换后的 HTML:")
    print("-" * 80)
    print(result.value)
    print("-" * 80)
    
    # 显示消息
    if result.messages:
        print("\n⚠️  转换消息:")
        print("-" * 80)
        for msg in result.messages:
            print(f"  [{msg.type}] {msg.message}")
    else:
        print("\n✓ 没有警告或错误消息")
    
    # 保存 HTML 文件
    with open("test_output.html", "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html>\n")
        f.write("<head>\n")
        f.write("  <meta charset='UTF-8'>\n")
        f.write("  <title>Test Document</title>\n")
        f.write("  <style>\n")
        f.write("    body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 20px; }\n")
        f.write("    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; }\n")
        f.write("    h2 { color: #34495e; border-bottom: 1px solid #95a5a6; }\n")
        f.write("    h3 { color: #34495e; }\n")
        f.write("  </style>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        f.write(result.value)
        f.write("\n</body>\n")
        f.write("</html>\n")
    
    print("\n" + "=" * 80)
    print("✓ 完成！HTML 已保存到 test_output.html")
    print("=" * 80)
    
    # 统计标签使用情况
    import re
    h1_count = len(re.findall(r'<h1[^>]*>', result.value))
    h2_count = len(re.findall(r'<h2[^>]*>', result.value))
    h3_count = len(re.findall(r'<h3[^>]*>', result.value))
    h4_count = len(re.findall(r'<h4[^>]*>', result.value))
    h5_count = len(re.findall(r'<h5[^>]*>', result.value))
    h6_count = len(re.findall(r'<h6[^>]*>', result.value))
    p_count = len(re.findall(r'<p[^>]*>', result.value))
    
    print("\n📊 HTML 标签统计:")
    print("-" * 80)
    if h1_count: print(f"  <h1> 标签: {h1_count}")
    if h2_count: print(f"  <h2> 标签: {h2_count}")
    if h3_count: print(f"  <h3> 标签: {h3_count}")
    if h4_count: print(f"  <h4> 标签: {h4_count}")
    if h5_count: print(f"  <h5> 标签: {h5_count}")
    if h6_count: print(f"  <h6> 标签: {h6_count}")
    if p_count: print(f"  <p> 标签: {p_count}")

if __name__ == "__main__":
    analyze_and_convert()

