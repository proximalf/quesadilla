---
{{ note.yaml }}
---
{% if note.title != "" or note.title is None %}
# {{ note.title }}
{% else %}

{% endif %}

{{ datetime.now().strftime("%A %d %B %Y %H:%M:%S") }}

{{ note.content }}
