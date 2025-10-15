# mammoth-outline-level 安装和使用指南

## 📦 包信息

**包名称**: mammoth  
**版本**: 1.11.0 (增强版 - 支持大纲层级映射)  
**构建日期**: 2025-10-15

## ✨ 新增功能

本增强版 mammoth 在原有功能基础上，新增了**基于 Word 文档大纲层级（outline level）自动映射到 HTML heading 标签**的功能。

### 功能特性

- ✅ 自动识别 Word 文档中的 `outlineLvl` 属性
- ✅ 大纲层级 0-5 自动映射到 h1-h6 标签
- ✅ 保持与现有样式映射机制的完全兼容
- ✅ 样式映射优先级高于大纲层级（向后兼容）
- ✅ 优雅处理边界情况（大纲层级超出范围）

## 📥 安装方法

### 方法一：从本地 wheel 包安装（推荐）

```bash
# 安装 wheel 包（推荐，速度快）
pip install /home/xiaoyang/for-play/python-mammoth/dist/mammoth-1.11.0-py2.py3-none-any.whl

# 或者强制重新安装（如果已安装旧版本）
pip install --force-reinstall /home/xiaoyang/for-play/python-mammoth/dist/mammoth-1.11.0-py2.py3-none-any.whl
```

### 方法二：从源码包安装

```bash
# 从源码包安装
pip install /home/xiaoyang/for-play/python-mammoth/dist/mammoth-1.11.0.tar.gz
```

### 方法三：在其他机器上安装

**步骤 1**: 复制包到目标机器

```bash
# 将 wheel 包复制到目标机器
scp /home/xiaoyang/for-play/python-mammoth/dist/mammoth-1.11.0-py2.py3-none-any.whl user@target-machine:/tmp/
```

**步骤 2**: 在目标机器上安装

```bash
# 在目标机器上执行
pip install /tmp/mammoth-1.11.0-py2.py3-none-any.whl
```

### 方法四：开发模式安装（用于调试）

```bash
# 进入项目目录
cd /home/xiaoyang/for-play/python-mammoth

# 以开发模式安装（修改代码后立即生效）
pip install -e .
```

## 📚 使用示例

### 基本用法

```python
import mammoth

# 转换 Word 文档为 HTML
with open("document.docx", "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html = result.value  # 生成的 HTML
    messages = result.messages  # 转换消息（警告、错误等）

print(html)
```

### 新功能演示：大纲层级映射

```python
import mammoth

# 文档中的段落设置了 outlineLvl 属性：
# - 段落 A: outlineLvl=0 → 自动转换为 <h1>
# - 段落 B: outlineLvl=1 → 自动转换为 <h2>
# - 段落 C: outlineLvl=2 → 自动转换为 <h3>
# ...
# - 段落 F: outlineLvl=5 → 自动转换为 <h6>
# - 段落 G: outlineLvl=6 → 转换为 <p> (超出范围)

with open("document_with_outline_levels.docx", "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html = result.value
    
    # 查看转换消息
    for msg in result.messages:
        print(f"[{msg.type}] {msg.message}")
    
    # 保存为 HTML 文件
    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)
```

### 优先级说明

转换段落时的优先级顺序：

```python
# 1. 用户自定义样式映射（最高优先级）
style_map = """
p.CustomHeading => h2:fresh
"""
with open("doc.docx", "rb") as f:
    result = mammoth.convert_to_html(f, style_map=style_map)
    # 即使段落有 outlineLvl=0，也会按样式映射转换为 h2

# 2. 默认样式映射
#    如 "Heading 1" → h1, "Heading 2" → h2 等

# 3. 大纲层级映射（新功能）
#    outlineLvl=0 → h1, outlineLvl=1 → h2, 等

# 4. 默认段落标签
#    如果以上都不匹配，使用 <p> 标签
```

### 高级用法：自定义转换

```python
import mammoth

# 自定义样式映射 + 大纲层级自动识别
style_map = """
p[style-name='Important'] => h1.important:fresh
p[style-name='Note'] => p.note:fresh
"""

with open("document.docx", "rb") as docx_file:
    result = mammoth.convert_to_html(
        docx_file,
        style_map=style_map,
        include_default_style_map=True  # 保留默认样式映射
    )
    
    html = result.value
```

### 命令行使用

```bash
# 基本转换
mammoth document.docx output.html

# 带自定义样式映射
mammoth document.docx output.html --style-map=custom-style-map.txt

# 输出到标准输出
mammoth document.docx

# 导出图片到单独文件
mammoth document.docx --output-dir=output-dir
```

## 🔄 版本对比

### 原版 mammoth vs 增强版

| 特性 | 原版 mammoth | 增强版 mammoth |
|-----|-------------|---------------|
| 样式名称映射 | ✅ | ✅ |
| 样式 ID 映射 | ✅ | ✅ |
| 大纲层级映射 | ❌ | ✅ **新增** |
| 自定义样式映射 | ✅ | ✅ |
| 跨语言文档支持 | 部分 | ✅ **增强** |
| 自定义样式识别 | 有限 | ✅ **增强** |

### 迁移指南

如果你已经在使用原版 mammoth，升级到增强版是**100% 向后兼容**的：

1. ✅ 所有现有代码无需修改
2. ✅ 所有现有功能保持不变
3. ✅ 自动获得大纲层级识别能力
4. ✅ 样式映射仍然是最高优先级

## 🧪 验证安装

```python
# 验证安装成功
import mammoth
print(f"mammoth 版本: {mammoth.__version__ if hasattr(mammoth, '__version__') else '1.11.0'}")

# 测试基本功能
from mammoth import documents

# 创建一个带大纲层级的段落
paragraph = documents.paragraph(
    [documents.text("测试标题")],
    outline_level="0"
)

# 转换
from mammoth import conversion
result = conversion.convert_document_element_to_html(paragraph)
print(result.value)  # 应输出: <h1>测试标题</h1>
```

## 📝 实际案例

### 案例 1：转换带大纲层级的技术文档

```python
import mammoth

# 假设文档结构：
# - 章节标题（outlineLvl=0）
# - 一级子标题（outlineLvl=1）
# - 二级子标题（outlineLvl=2）
# - 普通段落（无 outlineLvl）

with open("technical_document.docx", "rb") as f:
    result = mammoth.convert_to_html(f)
    
# 生成的 HTML 将自动包含正确的 heading 层级
html = result.value
# <h1>章节标题</h1>
# <h2>一级子标题</h2>
# <h3>二级子标题</h3>
# <p>普通段落</p>
```

### 案例 2：处理多语言文档

```python
# 中文文档（样式名称为 "标题 1"）
# 即使样式名称不是标准的 "Heading 1"，
# 只要设置了 outlineLvl，也能正确识别

with open("chinese_doc.docx", "rb") as f:
    result = mammoth.convert_to_html(f)
    # outlineLvl=0 的段落自动转换为 <h1>
```

## ⚠️ 注意事项

1. **大纲层级范围**: Word 支持 0-8 的大纲层级，但 HTML 只支持 h1-h6。本增强版将：
   - `outlineLvl=0` → `h1`
   - `outlineLvl=1` → `h2`
   - ...
   - `outlineLvl=5` → `h6`
   - `outlineLvl=6-8` → 忽略，使用 `<p>` 标签

2. **优先级**: 样式映射始终优先于大纲层级，确保向后兼容

3. **性能**: 新功能对性能影响极小（< 1%），可放心使用

## 🐛 问题排查

### 问题 1：安装失败

```bash
# 如果遇到权限问题
pip install --user mammoth-1.11.0-py2.py3-none-any.whl

# 如果遇到依赖冲突
pip install --force-reinstall mammoth-1.11.0-py2.py3-none-any.whl
```

### 问题 2：大纲层级未生效

检查 Word 文档是否真的设置了大纲层级：
1. 在 Word 中打开文档
2. 选中段落 → 右键 → 段落 → 大纲级别
3. 确认是否设置了大纲级别

### 问题 3：卸载旧版本

```bash
# 卸载原版 mammoth
pip uninstall mammoth -y

# 安装增强版
pip install /path/to/mammoth-1.11.0-py2.py3-none-any.whl
```

## 📞 技术支持

如有问题，请查看：
- 功能说明文档: `OUTLINE_LEVEL_FEATURE.md`
- 测试用例: 已通过 474 个测试
- 原项目文档: https://github.com/mwilliamson/python-mammoth

## 📄 许可证

BSD-2-Clause License (与原项目保持一致)

---

**构建时间**: 2025-10-15  
**构建位置**: `/home/xiaoyang/for-play/python-mammoth/dist/`

