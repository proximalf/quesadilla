---
{{ note.yaml }}
---
{% if note.title != "" or note.title is None %}
# {{ note.title }}
{% else %}

{% endif %}

{{ note.date.as_format("%A %d %B %Y %H:%M:%S") }}

{{ note.content }}
