---
layout: post
title: "swagger2 升级到 springdoc"
date: 2025-07-17
tags:
  - springdoc
  - swagger
comments: true
author: deathwhispers
---

# 背景

随着公司技术栈的持续演进，**Spring Boot 2.3.x 升级到 Spring Boot 3.3.x** 成为必然趋势。Spring Boot 3.3 完全基于 Jakarta EE 9+，要求使用 **Jakarta EE 9 的包名（jakarta.*）**，而 **Swagger2（Springfox）** 早已停止维护，**不再兼容 Spring Boot 3.x**。

因此，为了：

- 适配 Spring Boot 3.3.x 及后续版本
- 使用现代化的 API 文档工具
- 提升文档生成效率与维护性
 
我们决定将项目中的 **Swagger2（Springfox）迁移至 SpringDoc OpenAPI**。

# 二、升级的必要性

| 升级点 | 说明 |
|--------|------|
| **Springfox 停止维护** | Springfox Swagger2 最后一次更新在 2020 年，不再支持 Spring Boot 2.6+，更不兼容 Spring Boot 3.x |
| **Spring Boot 3.x 包名变更** | 从 `javax` 变为 `jakarta`，Springfox 无法兼容 |
| **SpringDoc 活跃维护** | SpringDoc OpenAPI 是目前最活跃、兼容性最强的 OpenAPI 工具 |
| **支持 OpenAPI 3.x 规范** | 提供更丰富的文档结构和交互式 UI（Swagger UI + ReDoc） |


## 三、当前痛点分析

在升级过程中，我们遇到的主要痛点如下：

| 痛点 | 描述 |
|------|------|
| **旧代码中大量使用 Springfox 的注解** | 如 `@Api`, `@ApiOperation`, `@ApiModel`, `@ApiModelProperty` 等，SpringDoc 不兼容 |
| **无成熟迁移工具** | Springfox 注解无法自动转换为 SpringDoc 注解 |
| **手动替换效率低、易出错** | 一个项目可能有上百个 Controller 和 Model，手动修改成本高 |
| **缺乏统一的替换规范** | 团队协作时容易出现注解使用不一致的问题 |


## 四、解决方案：脚本化批量替换

为了高效完成 Springfox 到 SpringDoc 的迁移，我们采取了 **正则表达式 + 脚本化替换** 的方式，**自动化批量替换注解**。

### ✅ 1. 替换目标

将 Springfox 的注解类替换为 SpringDoc 的等效类。

| Springfox 注解 | SpringDoc 注解 |
|----------------|----------------|
| `@Api` | `@Tag` |
| `@ApiOperation` | `@Operation` |
| `@ApiModel` | `@Schema` |
| `@ApiModelProperty` | `@Schema` |
| `@ApiParam` | `@Parameter` |

### ✅ 2. 使用脚本进行批量替换（Python 示例）

{% raw %}
```python
import os
import re

# --- 全局配置与常量 ---
PROJECT_ROOT = './src/main'

OLD_SWAGGER_IMPORT_PREFIX = 'import io.swagger.annotations.'
NEW_SWAGGER_IMPORT_PREFIX = 'import io.swagger.v3.oas.annotations.'


# --- 辅助函数：通用正则模式 ---
GENERIC_PAREN_CONTENT_REGEX = r'(?:[^()]|"[^"]*"|\((?:[^()]|"[^"]*")*\))*?'


# --- 主要正则表达式定义 ---
ANNOTATION_REGEX = re.compile(
    r'(?s)(@(?:Api\b|ApiModel\b|ApiOperation\b|ApiParam\b|ApiResponse\b|ApiResponses\b|ApiModelProperty\b|ApiIgnore\b))\s*' # 捕获注解名称 (组1)
    r'(' # 开始捕获组2：匹配整个属性括号块 (包括括号本身)
    r'\(' + GENERIC_PAREN_CONTENT_REGEX + r'\)' # 匹配开括号，中间内容，闭括号
                                          r')?' # 使整个属性块可选 (注解可能没有参数)
)

# --- 修正后的 API_IMPLICIT_PARAM_BLOCK_REGEX 定义 ---
API_IMPLICIT_PARAM_BLOCK_REGEX = re.compile(
    r'(?s)(@(?:ApiImplicitParam\b|ApiImplicitParams\b))\s*' # 捕获注解名称 (组1)
    r'(' # 开始捕获组2：匹配整个属性括号块 (包括括号本身)
    r'(?:' # 非捕获组，用于匹配两种可能的块类型：花括号 {} 或圆括号 ()
    r'\{(?:[^{}]|"[^"]*"|.)*?\}' # 匹配花括号块 { ... } (非贪婪，允许内部引号或任何字符)
    r'|\((?:[^()]|"[^"]*"|.)*?\)' # OR 匹配圆括号块 ( ... ) (非贪婪，允许内部引号或任何字符)
    r')'
    r')' # 结束捕获组2
)

API_IMPLICIT_PARAM_INNER_REGEX = re.compile(
    r'(?s)(@ApiImplicitParam\b)\s*' # 捕获 @ApiImplicitParam 名称 (组1)
    r'(' # 捕获整个参数块 (组2)
    r'\((?:[^()]|"[^"]*"|.)*?\)' # 匹配其参数括号
    r')' # 必须有一个参数块
)


# --- 辅助函数：从注解字符串中提取属性 (key=value) ---
def extract_annotation_attrs(attrs_str):
    attrs = {}
    if not attrs_str:
        return attrs

    if attrs_str.startswith('(') and attrs_str.endswith(')'):
        attrs_str = attrs_str[1:-1] # Correct slicing

    attr_value_pattern = re.compile(
        r'(\w+)\s*=\s*('  # 捕获属性名 (key) 和值 (raw_value)
        r'"(?:[^"\\]|\\.)*"'  # 选项1: 鲁棒地捕获带引号的字符串
        r'|\{.*?\}'          # 选项2: 花括号内容
        r'|\b(?:true|false|\d+(?:\.\d+)?)\b' # 选项3: 布尔值或数字
        r')' # 结束值捕获组
    )

    for match in attr_value_pattern.finditer(attrs_str):
        key = match.group(1).strip()
        raw_value = match.group(2).strip()

        if raw_value.startswith('"') and raw_value.endswith('"'):
            attrs[key] = raw_value
        elif raw_value.startswith('{') and raw_value.endswith('}'):
            attrs[key] = raw_value
        elif raw_value.lower() == 'true' or raw_value.lower() == 'false' or re.fullmatch(r'\d+(?:\.\d+)?', raw_value):
            attrs[key] = raw_value
        else:
            attrs[key] = f'"{raw_value}"'

    return attrs

# --- 辅助函数：将属性字典格式化为字符串 ---
def _format_attrs_string(attrs_dict):
    parts = []
    for key, val in attrs_dict.items():
        parts.append(f"{key} = {val}")
    return ", ".join(parts)


# --- 通用属性处理逻辑 (必须在具体的注解处理器之前定义) ---
def _handle_common_attrs(extracted_attrs, attr_map, attrs_to_remove, final_attrs_dict, new_imports_needed=None, old_annotation_name=""):
    for old_key, new_key in attr_map.items():
        if old_key in extracted_attrs and old_key not in attrs_to_remove:
            val = extracted_attrs[old_key]

            if old_annotation_name == '@ApiResponse' and old_key == 'code':
                final_attrs_dict['responseCode'] = val
            elif new_key == 'schema' and old_annotation_name == '@ApiImplicitParam':
                final_attrs_dict['schema'] = val
            else:
                final_attrs_dict[new_key] = val

            extracted_attrs.pop(old_key)

    # 添加剩余的属性 (如果未被映射或移除，且未被 ignore_unmapped_attrs 忽略)
    # 这里的 logic_ignore_unmapped_attrs_flag 需要从 mapping_config 传递
    for key, val in extracted_attrs.items():
        if key not in attrs_to_remove:
            pass


# --- 注解处理器函数定义 (必须在 ANNOTATION_MAP 之前定义) ---
def _handle_api_model(old_attrs_content, mapping_config):
    new_imports_needed = set()
    extracted_attrs = extract_annotation_attrs(old_attrs_content)
    final_attrs_dict = {}

    # Handle default attribute value (e.g., @ApiModel("MyModel"))
    if not extracted_attrs and old_attrs_content.strip().startswith('(') and old_attrs_content.strip().endswith(')'):
        default_value = old_attrs_content.strip()[1:-1].strip()
        if default_value.startswith('"') and default_value.endswith('"'):
            final_attrs_dict['name'] = default_value
        else:
            final_attrs_dict['name'] = f'"{default_value}"'

    _handle_common_attrs(extracted_attrs, mapping_config['attr_map'], mapping_config.get('attrs_to_remove', []), final_attrs_dict, new_imports_needed, '@ApiModel')

    if not mapping_config.get('ignore_unmapped_attrs', False):
        for key, val in extracted_attrs.items():
            final_attrs_dict[key] = val

    return (f"@Schema({_format_attrs_string(final_attrs_dict)})", new_imports_needed)


def _handle_api(old_attrs_content, mapping_config):
    new_imports_needed = set()
    extracted_attrs = extract_annotation_attrs(old_attrs_content)
    final_attrs_dict = {}
    tag_name_set = False

    if not extracted_attrs and old_attrs_content.strip().startswith('(') and old_attrs_content.strip().endswith(')'):
        default_value = old_attrs_content.strip()[1:-1].strip()
        if default_value.startswith('"') and default_value.endswith('"'):
            final_attrs_dict['name'] = default_value
        else:
            final_attrs_dict['name'] = f'"{default_value}"'
        tag_name_set = True

    special_api_attrs = mapping_config.get('special_api_attrs', {})

    if 'value' in extracted_attrs:
        final_attrs_dict['name'] = extracted_attrs['value']
        tag_name_set = True
        extracted_attrs.pop('value')

    if 'tags' in extracted_attrs:
        if not tag_name_set:
            tags_str = extracted_attrs['tags'].strip('{}').replace('"', '').replace("'", "")
            tags_list = [tag.strip().strip('"').strip("'") for tag in tags_str.split(',') if tag.strip()]
            if tags_list:
                final_attrs_dict['name'] = f"\"{', '.join(tags_list)}\""
                tag_name_set = True
        else:
            print(f"  Warning: @Api for '{old_attrs_content}' has both 'value' and 'tags'. 'value' is used for 'name', 'tags' is ignored. Review manually.")
        extracted_attrs.pop('tags')

    if 'description' in extracted_attrs:
        if not tag_name_set:
            final_attrs_dict['name'] = extracted_attrs['description']
            tag_name_set = True
        else:
            print(f"  Warning: @Api for '{old_attrs_content}' has 'value' or 'tags' (used for 'name') and 'description'. 'description' will be ignored. Review manually if it should be actual description.")
        extracted_attrs.pop('description')

    _handle_common_attrs(extracted_attrs, mapping_config['attr_map'], mapping_config.get('attrs_to_remove', []), final_attrs_dict, new_imports_needed, '@Api')

    if not mapping_config.get('ignore_unmapped_attrs', False):
        for key, val in extracted_attrs.items():
            final_attrs_dict[key] = val

    return (f"@Tag({_format_attrs_string(final_attrs_dict)})", new_imports_needed)


def _handle_api_operation(old_attrs_content, mapping_config):
    new_imports_needed = set()
    extracted_attrs = extract_annotation_attrs(old_attrs_content)
    final_attrs_dict = {}

    if not extracted_attrs and old_attrs_content.strip().startswith('(') and old_attrs_content.strip().endswith(')'):
        default_value = old_attrs_content.strip()[1:-1].strip()
        if default_value.startswith('"') and default_value.endswith('"'):
            final_attrs_dict['summary'] = default_value
        else:
            final_attrs_dict['summary'] = f'"{default_value}"'
    else:
        _handle_common_attrs(extracted_attrs, mapping_config['attr_map'], mapping_config.get('attrs_to_remove', []), final_attrs_dict, new_imports_needed, '@ApiOperation')

    if not mapping_config.get('ignore_unmapped_attrs', False):
        for key, val in extracted_attrs.items():
            final_attrs_dict[key] = val

    return (f"@Operation({_format_attrs_string(final_attrs_dict)})", new_imports_needed)


def _handle_api_responses(old_attrs_content, mapping_config):
    new_imports_needed = set()
    transformed_inner_responses = []

    params_block_str = old_attrs_content.strip()
    if params_block_str.startswith('{') and params_block_str.endswith('}'):
        params_block_str = params_block_str[1:-1].strip()
    elif params_block_str.startswith('(') and params_block_str.endswith(')'):
        params_block_str = params_block_str[1:-1].strip()
        if params_block_str.startswith('{') and params_block_str.endswith('}'):
            params_block_str = params_block_str[1:-1].strip()

    api_response_inner_regex = re.compile(
        r'(?s)(@ApiResponse\b)\s*'
        r'(' # 捕获其整个参数块
        r'\((?:[^()]|"[^"]*"|\((?:[^()]|"[^"]*")*\))*?\)'
        r')'
    )

    for match in api_response_inner_regex.finditer(params_block_str):
        inner_resp_name = match.group(1)
        inner_resp_attrs_content = match.group(2)

        inner_resp_mapping = ANNOTATION_MAP.get(inner_resp_name)
        if inner_resp_mapping:
            transformed_resp_str, inner_imports = build_new_annotation_string(
                inner_resp_name, inner_resp_attrs_content, inner_resp_mapping
            )
            transformed_inner_responses.append(transformed_resp_str)
            new_imports_needed.update(inner_imports)
        else:
            print(f"  Warning: No mapping found for nested {inner_resp_name}. Skipping transformation of: {match.group(0)}")
            transformed_inner_responses.append(match.group(0))

    attrs_string = f"{{ {', '.join(transformed_inner_responses)} }}"
    return (f"@ApiResponses({attrs_string})", new_imports_needed)


def _handle_api_response(old_attrs_content, mapping_config):
    new_imports_needed = set()
    extracted_attrs = extract_annotation_attrs(old_attrs_content)
    final_attrs_dict = {}

    _handle_common_attrs(extracted_attrs, mapping_config['attr_map'], mapping_config.get('attrs_to_remove', []), final_attrs_dict, new_imports_needed, '@ApiResponse')

    if not mapping_config.get('ignore_unmapped_attrs', False):
        for key, val in extracted_attrs.items():
            final_attrs_dict[key] = val

    return (f"@ApiResponse({_format_attrs_string(final_attrs_dict)})", new_imports_needed)


def _handle_api_ignore(old_attrs_content, mapping_config):
    new_imports_needed = set()
    return (f"@Hidden()", new_imports_needed)


def _handle_api_param(old_attrs_content, mapping_config):
    new_imports_needed = set()
    extracted_attrs = extract_annotation_attrs(old_attrs_content)
    final_attrs_dict = {}

    _handle_common_attrs(extracted_attrs, mapping_config['attr_map'], mapping_config.get('attrs_to_remove', []), final_attrs_dict, new_imports_needed, '@ApiParam')

    if not mapping_config.get('ignore_unmapped_attrs', False):
        for key, val in extracted_attrs.items():
            final_attrs_dict[key] = val

    return (f"@Parameter({_format_attrs_string(final_attrs_dict)})", new_imports_needed)


def _handle_api_implicit_param_inner(old_attrs_content, mapping_config):
    new_imports_needed = set()
    extracted_attrs = extract_annotation_attrs(old_attrs_content)
    final_attrs_dict = {}

    if 'dataType' in extracted_attrs:
        data_type = extracted_attrs['dataType'].strip('"')
        if data_type.lower() in ['string', 'integer', 'boolean', 'number', 'array', 'file', 'long', 'double', 'float', 'byte', 'binary', 'date', 'date-time', 'password']:
            final_attrs_dict['schema'] = f"@Schema(type = \"{data_type.lower()}\")"
            new_imports_needed.add('io.swagger.v3.oas.annotations.media.Schema')
        else:
            final_attrs_dict['schema'] = f"{data_type}.class"
        extracted_attrs.pop('dataType')

    _handle_common_attrs(extracted_attrs, mapping_config['attr_map'], mapping_config.get('attrs_to_remove', []), final_attrs_dict, new_imports_needed, '@ApiImplicitParam')

    if not mapping_config.get('ignore_unmapped_attrs', False):
        for key, val in extracted_attrs.items():
            final_attrs_dict[key] = val

    return (f"@Parameter({_format_attrs_string(final_attrs_dict)})", new_imports_needed)


def _handle_api_implicit_params(old_attrs_content, mapping_config):
    new_imports_needed = set()
    new_name = mapping_config['new_name'] # 通常是 '@Parameters'

    # 根据您的要求，直接将 @ApiImplicitParams 替换为 @Parameters()
    # 注意：这将导致内部定义的 @ApiImplicitParam 详情丢失。
    print(f"  Warning: @ApiImplicitParams is simplified to @Parameters(). All inner parameter details will be lost for '{old_attrs_content}'.")

    # 返回 @Parameters() 格式的字符串，不包含任何参数
    return (f"{new_name}()", new_imports_needed)


def _handle_api_model_property(old_attrs_content, mapping_config):
    new_imports_needed = set()
    extracted_attrs = extract_annotation_attrs(old_attrs_content)
    final_attrs_dict = {}

    if not extracted_attrs and old_attrs_content.strip().startswith('(') and old_attrs_content.strip().endswith(')'):
        default_value = old_attrs_content.strip()[1:-1].strip()
        if default_value.startswith('"') and default_value.endswith('"'):
            final_attrs_dict['name'] = default_value
        else:
            final_attrs_dict['name'] = f'"{default_value}"' # 修正：移除了多余的 }

    if 'readOnly' in extracted_attrs: # 正确缩进的 if 块
        val = extracted_attrs['readOnly'].lower().strip('"')
        if val == 'true':
            final_attrs_dict['accessMode'] = 'Schema.AccessMode.READ_ONLY'
        elif val == 'false':
            final_attrs_dict['accessMode'] = 'Schema.AccessMode.READ_WRITE'
        new_imports_needed.add('io.swagger.v3.oas.annotations.media.Schema')
        extracted_attrs.pop('readOnly')

    _handle_common_attrs(extracted_attrs, mapping_config['attr_map'], mapping_config.get('attrs_to_remove', []), final_attrs_dict, new_imports_needed, '@ApiModelProperty')

    if not mapping_config.get('ignore_unmapped_attrs', False):
        for key, val in extracted_attrs.items():
            final_attrs_dict[key] = val

    return (f"@Schema({_format_attrs_string(final_attrs_dict)})", new_imports_needed)


# --- 注解映射表 (必须在所有处理器函数之后定义) ---
# 映射表现在包含处理器函数的引用，以及每个注解的特定配置
ANNOTATION_MAP = {
    '@ApiModel': {'handler': _handle_api_model, 'imports': 'io.swagger.v3.oas.annotations.media.Schema',
                  'attr_map': {'description': 'description', 'value': 'name', 'name': 'description'},
                  'default_attr_target': 'name', 'ignore_unmapped_attrs': True},
    '@Api': {'handler': _handle_api, 'imports': 'io.swagger.v3.oas.annotations.tags.Tag',
             'attr_map': {'value': 'name'}, # Primary mapping for common attrs
             'special_api_attrs': {'tags': 'name', 'description': 'name'}, # Special attrs for @Api, mapped to 'name'
             'default_attr_target': 'name', 'ignore_unmapped_attrs': True},
    '@ApiOperation': {'handler': _handle_api_operation, 'imports': 'io.swagger.v3.oas.annotations.Operation',
                      'attr_map': {'value': 'summary', 'notes': 'description'},
                      'default_attr_target': 'summary', 'ignore_unmapped_attrs': True},
    '@ApiResponses': {'handler': _handle_api_responses, 'imports': 'io.swagger.v3.oas.annotations.responses.ApiResponses',
                      'attr_map': {}, 'default_attr_target': None, 'ignore_unmapped_attrs': True}, # Empty attr_map for common handler
    '@ApiResponse': {'handler': _handle_api_response, 'imports': 'io.swagger.v3.oas.annotations.responses.ApiResponse',
                     'attr_map': {'code': 'responseCode', 'message': 'description'}, 'default_attr_target': None, 'ignore_unmapped_attrs': True},
    '@ApiIgnore': {'handler': _handle_api_ignore, 'imports': 'io.swagger.v3.oas.annotations.Hidden',
                   'attr_map': {}, 'default_attr_target': None, 'ignore_unmapped_attrs': True},
    '@ApiParam': {'handler': _handle_api_param, 'imports': 'io.swagger.v3.oas.annotations.Parameter',
                  'attr_map': {'value': 'description', 'required': 'required', 'example': 'example', 'allowableValues': 'allowableValues'},
                  'default_attr_target': None, 'ignore_unmapped_attrs': True},
    '@ApiImplicitParam': {'handler': _handle_api_implicit_param_inner, 'imports': 'io.swagger.v3.oas.annotations.Parameter',
                          'attr_map': {'name': 'name', 'value': 'description', 'required': 'required', 'example': 'example'},
                          'attrs_to_remove': ['dataType', 'paramType'], 'default_attr_target': None, 'ignore_unmapped_attrs': True},
    '@ApiImplicitParams': {'handler': _handle_api_implicit_params, 'imports': 'io.swagger.v3.oas.annotations.Parameters',
                           'attr_map': {}, 'default_attr_target': None, 'ignore_unmapped_attrs': True},
    '@ApiModelProperty': {'handler': _handle_api_model_property, 'imports': 'io.swagger.v3.oas.annotations.media.Schema',
                          'attr_map': {'value': 'name', 'name': 'description', 'notes': 'description'},
                          'default_attr_target': 'name', 'ignore_unmapped_attrs': True,
                          'attrs_to_remove': ['position', 'readOnly', 'hidden', 'allowableValues']},
}


# --- build_new_annotation_string 调度器 (保持简洁) ---
# 它是所有注解转换的入口点，根据注解名调用对应的处理器函数。
def build_new_annotation_string(old_annotation_name, old_attrs_content, mapping_config):
    handler_func = mapping_config['handler']
    return handler_func(old_attrs_content, mapping_config)


# --- 主要文件处理逻辑 (整合了 Jakarta EE 升级) ---
def process_java_file(filepath):
    print(f"Checking: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        original_lines = f.readlines()

    contains_swagger2_imports = any(line.strip().startswith(OLD_SWAGGER_IMPORT_PREFIX) for line in original_lines)

    package_declaration_line = None
    existing_non_swagger_imports = []

    code_lines_step1 = []
    for line in original_lines:
        current_line_processed = line

        if current_line_processed.strip().startswith('import javax.'):
            current_line_processed = current_line_processed.replace('import javax.', 'import jakarta.')

        if current_line_processed.strip().startswith('package '):
            package_declaration_line = current_line_processed
        elif current_line_processed.strip().startswith(OLD_SWAGGER_IMPORT_PREFIX):
            continue
        elif current_line_processed.strip().startswith('import '):
            existing_non_swagger_imports.append(current_line_processed)
        else:
            code_lines_step1.append(current_line_processed)

    code_lines_step2 = []
    required_new_swagger_imports_general = set()

    if contains_swagger2_imports:
        for line_idx, line in enumerate(code_lines_step1):
            current_line_for_general_swagger = line
            matches = list(ANNOTATION_REGEX.finditer(current_line_for_general_swagger))
            if matches:
                for match in reversed(matches):
                    old_annotation_name = match.group(1)
                    old_attrs_content_full = match.group(2)
                    if old_attrs_content_full is None: old_attrs_content_full = ""

                    mapping_config = ANNOTATION_MAP.get(old_annotation_name)
                    if mapping_config:
                        new_annotation_str, inner_imports = build_new_annotation_string(
                            old_annotation_name, old_attrs_content_full, mapping_config
                        )
                        required_new_swagger_imports_general.update(inner_imports)
                        required_new_swagger_imports_general.add(mapping_config['imports'])

                        current_line_for_general_swagger = current_line_for_general_swagger[:match.start()] + new_annotation_str + current_line_for_general_swagger[match.end():]
            code_lines_step2.append(current_line_for_general_swagger)
    else:
        code_lines_step2 = code_lines_step1

    code_lines_step3 = []
    required_new_swagger_imports_implicit = set()

    if contains_swagger2_imports:
        i = 0
        while i < len(code_lines_step2):
            line = code_lines_step2[i]

            implicit_match = API_IMPLICIT_PARAM_BLOCK_REGEX.search(line)

            if implicit_match:
                old_annotation_name_block = implicit_match.group(1)

                block_start_char = '('
                block_end_char = ')'
                if '@ApiImplicitParams' in old_annotation_name_block:
                    block_start_char = '{'
                    block_end_char = '}'

                current_balance = 0
                block_raw_lines = []

                start_pos_in_line = line.find(block_start_char, implicit_match.start())

                if start_pos_in_line != -1:
                    block_raw_lines.append(line[start_pos_in_line:])
                    for char in line[start_pos_in_line:]:
                        if char == block_start_char: current_balance += 1
                        elif char == block_end_char: current_balance -= 1
                        elif char == '{': current_balance += 1
                        elif char == '}': current_balance -= 1
                        elif char == '[': current_balance += 1
                        elif char == ']': current_balance -= 1

                    block_end_line_idx = i
                    while current_balance > 0 and block_end_line_idx + 1 < len(code_lines_step2):
                        block_end_line_idx += 1
                        next_line = code_lines_step2[block_end_line_idx]
                        block_raw_lines.append(next_line)
                        for char in next_line:
                            if char == block_start_char: current_balance += 1
                            elif char == block_end_char: current_balance -= 1
                            elif char == '{': current_balance += 1
                            elif char == '}': current_balance += 1
                            elif char == '[': current_balance += 1
                            elif char == ']': current_balance += 1

                    if current_balance == 0:
                        full_block_content = "".join(block_raw_lines)

                        mapping_config = ANNOTATION_MAP.get(old_annotation_name_block)
                        if mapping_config:
                            new_annotation_str, inner_imports = build_new_annotation_string(
                                old_annotation_name_block, full_block_content, mapping_config
                            )
                            required_new_swagger_imports_implicit.update(inner_imports)
                            required_new_swagger_imports_implicit.add(mapping_config['imports'])

                            indent = line[:implicit_match.start()]
                            new_annotation_str_indented = "\n".join([indent + s.lstrip() for s in new_annotation_str.splitlines()])

                            code_lines_step3.append(line[:implicit_match.start()] + new_annotation_str_indented + line[start_pos_in_line + len(full_block_content):].lstrip())

                            i = block_end_line_idx + 1
                            continue
                        else:
                            print(f"  Warning: No mapping found for {old_annotation_name_block} in dedicated pass. Keeping original.")
                            code_lines_step3.append(line)
                            i += 1
                            continue
                    else:
                        print(f"  Warning: Unbalanced {block_start_char}{block_end_char} block starting at line {line_idx} in {filepath}. Skipping dedicated processing for this block.")
                        code_lines_step3.extend(code_lines_step2[i:block_end_line_idx+1])
                        i = block_end_line_idx + 1
                        continue
                else:
                    code_lines_step3.append(line)
                    i += 1
                    continue
            else:
                code_lines_step3.append(line)
                i += 1

    else:
        code_lines_step3 = code_lines_step2

        # --- Step 4: 重构文件内容 ---
    final_output_lines = []
    if package_declaration_line:
        final_output_lines.append(package_declaration_line)
        final_output_lines.append('\n')

    for imp_line in sorted(list(set(existing_non_swagger_imports))):
        final_output_lines.append(imp_line)

    all_required_swagger_imports = required_new_swagger_imports_general.union(required_new_swagger_imports_implicit)

    for new_imp_path in sorted(list(all_required_swagger_imports)):
        full_new_imp_line = f"import {new_imp_path};\n"
        if full_new_imp_line not in final_output_lines:
            final_output_lines.append(full_new_imp_line)

    if (package_declaration_line or existing_non_swagger_imports or all_required_swagger_imports) and code_lines_step3 and code_lines_step3[0].strip() != '':
        if final_output_lines and final_output_lines[-1].strip() != '':
            final_output_lines.append('\n')

    final_output_lines.extend(code_lines_step3)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(final_output_lines)
        print(f"  Successfully updated {filepath}")
    except Exception as e:
        print(f"  Error writing to {filepath}: {e}")

# --- 主脚本执行 ---
def main():
    if not os.path.isdir(PROJECT_ROOT):
        print(f"Error: Project root directory '{PROJECT_ROOT}' not found.")
        print("Please adjust PROJECT_ROOT variable in the script.")
        return

    print(f"Starting Swagger and Jakarta EE upgrade in: {PROJECT_ROOT}\n")

    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith('.java'):
                filepath = os.path.join(root, file)
                process_java_file(filepath)

    print("\n---------------------------------------------------------")
    print("Upgrade Complete: Swagger 2 to Swagger 3 & Javax to Jakarta EE.")
    print("重要提示：尽管脚本进行了多方面适配，但仍强烈建议您执行以下操作：")
    print("1. 重新构建您的项目，并解决所有编译错误。")
    print("2. 仔细审查修改过的 Java 文件，特别是：")
    print("   - 包含 @ApiImplicitParam / @ApiImplicitParams 的部分（通常需要手动优化）。")
    print("   - 复杂、多行注解或自定义注解，确保其转换无误。")
    print("   - 检查属性值的引号和格式，特别是那些复杂字符串或自动推断类型的值。")
    print("3. 运行您的API文档（通常是访问 /swagger-ui.html），检查生成的文档是否正确。")
    print("4. 运行您的项目测试，确保功能正常。")
    print("---------------------------------------------------------")

if __name__ == "__main__":
    main()
```
{% endraw %}

### ✅ 3. 执行步骤

1. 将脚本保存为 `swagger2_springdoc_replace.py`
2. 修改 `project_dir` 为你的 Java 项目路径
3. 运行脚本：

```bash
python swagger2_springdoc_replace.py
```

### ✅ 4. 后续人工校验

- 检查 `@Tag`、`@Operation` 中的 `name` 和 `summary` 是否为空，需手动填写
- 检查 `@Schema` 注解是否需要添加 `description` 字段
- 检查是否有遗漏的注解或误替换

---

## 五、SpringDoc 配置示例（Spring Boot 3.3）

### 1. 添加依赖（`pom.xml`）

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.2.0</version>
</dependency>
```

### 2. 配置 OpenAPI（`application.yml`）

```yaml
springdoc:
  api-docs:
    enabled: true
    path: /v3/api-docs
  swagger-ui:
    enabled: true
    path: /swagger-ui.html
    tags-sorter: alpha
    operations-sorter: alpha
```

### 3. 启动类无需改动，访问地址：

```
http://localhost:8080/swagger-ui.html
```

---

## 六、总结

| 项目 | 内容 |
|------|------|
| 升级背景 | Spring Boot 2.3 → 3.3，Springfox 不再维护 |
| 升级必要性 | 适配新版本、使用现代化 API 文档工具 |
| 主要痛点 | 旧注解无法兼容、无成熟迁移工具 |
| 解决方案 | 使用正则脚本批量替换 Springfox 注解为 SpringDoc 注解 |
| 推荐实践 | 脚本 + 人工校验，确保文档完整性与准确性 |

> ps: 最终效果只能说差强人意，适配范围不够广，还是有很多情况无法替换，而且对于@ApiImplicitParam的处理一直解决不了，存在一些问题，还是需要再手动处理。
> 不过也能解决绝大部分的问题了，能省点事。
> 
> 希望有大佬能搞个完美的解决方案，这个在升级中还是很有用的。
