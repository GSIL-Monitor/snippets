{{ key }} = Column('{{- name -}}', {{ columnType }}
{%- if options -%}
, {{ options -}}
{% endif -%}
)
