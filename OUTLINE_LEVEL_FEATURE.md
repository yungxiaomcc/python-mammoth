# 大纲层级映射功能

## 功能概述

这个增强功能为 python-mammoth 添加了基于 Word 文档大纲层级（outline level）的 HTML heading 映射支持。

## 背景

在 Word 文档中，段落可以通过两种方式标记为标题：
1. **样式（Style）**：使用预定义的 Heading 1-6 样式
2. **大纲层级（Outline Level）**：在段落属性中直接设置 `outlineLvl` 属性（值为 0-8）

之前，mammoth 只支持基于样式的映射。现在增加了对大纲层级的支持。

## 工作原理

### 优先级策略

转换段落时，按以下优先级顺序查找映射规则：

1. **用户自定义样式映射**（最高优先级）
   - 如果在 `style_map` 中定义了匹配的规则，使用该规则
   
2. **默认样式映射**
   - 如果段落样式匹配默认映射（如 Heading 1 → h1），使用默认映射
   
3. **大纲层级映射**（新增）
   - 如果段落有 `outlineLvl` 属性，根据层级映射到对应的 heading：
     - `outlineLvl=0` → `<h1>`
     - `outlineLvl=1` → `<h2>`
     - `outlineLvl=2` → `<h3>`
     - `outlineLvl=3` → `<h4>`
     - `outlineLvl=4` → `<h5>`
     - `outlineLvl=5` → `<h6>`
     - `outlineLvl=6-8` → 忽略（使用默认段落标签）
   
4. **默认段落标签**（最低优先级）
   - 如果以上都不匹配，使用 `<p>` 标签

### 映射示例

```xml
<!-- Word 文档 XML -->
<w:p>
  <w:pPr>
    <w:outlineLvl w:val="0"/>
  </w:pPr>
  <w:r>
    <w:t>章节标题</w:t>
  </w:r>
</w:p>
```

转换为：

```html
<h1>章节标题</h1>
```

## 代码修改

### 1. `mammoth/documents.py`
- 在 `Paragraph` 类中添加 `outline_level` 字段
- 更新 `paragraph()` 构造函数支持 `outline_level` 参数

### 2. `mammoth/docx/body_xml.py`
- 在读取段落属性时，读取 `w:outlineLvl` 元素的值
- 将 `outline_level` 传递给 `documents.paragraph()`

### 3. `mammoth/conversion.py`
- 修改 `_find_html_path_for_paragraph()` 方法
- 实现优先级查找逻辑：
  1. 首先尝试样式映射
  2. 然后尝试大纲层级映射
  3. 最后使用默认值

## 测试结果

所有测试均通过：

✓ 大纲层级 0-5 正确映射到 h1-h6  
✓ 没有大纲层级时使用默认 p 标签  
✓ 样式映射优先于大纲层级（保持向后兼容性）  
✓ 超出范围的大纲层级（6-8）被正确忽略  
✓ 所有现有的 61 个转换测试仍然通过（向后兼容）  

## 优势

1. **更准确的语义识别**：大纲层级直接表示文档结构，比样式名称更可靠
2. **支持自定义样式**：用户使用自定义样式名称但设置了正确的大纲层级时，仍能正确转换
3. **向后兼容**：不影响现有功能，样式映射仍然具有最高优先级
4. **跨语言支持**：不依赖样式名称的语言，支持各种语言的 Word 文档

## 使用场景

### 场景 1：标准 Heading 样式
```python
# Word 文档使用标准 Heading 1-6 样式
# 效果：样式映射优先，结果与之前一致
```

### 场景 2：自定义样式 + 大纲层级
```python
# Word 文档使用自定义样式名称（如"章节标题"）
# 但段落设置了 outlineLvl=0
# 效果：自动映射到 <h1>，无需额外配置
```

### 场景 3：混合使用
```python
# 用户自定义样式映射
style_map = "p.Important => h2.important:fresh"

# 效果：
# - p.Important 样式 → <h2 class="important">（样式映射优先）
# - outlineLvl=0 的段落 → <h1>（大纲层级生效）
# - 普通段落 → <p>（默认）
```

## 注意事项

1. **样式映射仍然是最高优先级**：确保向后兼容性
2. **大纲层级 6-8 被忽略**：因为 HTML 只支持 h1-h6
3. **需要 Word 文档正确设置大纲层级**：并非所有文档都设置了这个属性

## 未来改进建议

1. 可以添加配置选项控制优先级顺序
2. 可以支持将大纲层级 6-8 映射到带特殊 class 的 h6
3. 可以添加日志功能，记录使用了哪种映射规则

## 测试

运行测试：

```bash
# 运行大纲层级功能测试
python3 test_outline_level.py

# 运行所有转换测试
PYTHONPATH=/home/xiaoyang/for-play/python-mammoth:$PYTHONPATH \
  python3 -m pytest tests/conversion_tests.py -v
```

## 作者

修改时间：2025-10-15

