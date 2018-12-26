# -*- coding: utf-8 -*-
import jinja2

tpl = """
### {{ title }}

create_db ({{ env }})

结果：{{ result }}

{% if failed_tables %}
{%- for t in failed_tables %}
- {{ t }}
{% endfor -%}
{% endif %}
"""

title = '标题'
env = 'production'
result = '失败'
failed_tables = ['table1', 'table2']
# failed_tables = []

ctx = {
    'title': title,
    'env': env,
    'result': result,
    'failed_tables': failed_tables,
}

t = jinja2.Template(tpl)
out = t.render(**ctx)
print(out)
