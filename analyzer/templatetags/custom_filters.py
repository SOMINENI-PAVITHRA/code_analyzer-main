from django import template
import re

register = template.Library()


@register.filter
def extract_resource_text(value):
    try:
        # Match [text] with possible spaces
        match = re.search(r"\[\s*(.*?)\s*\]", value)
        return match.group(1) if match else value.split("]")[0].strip(" [-*")
    except:
        return value.split("(")[0].strip()


@register.filter
def extract_resource_url(value):
    try:
        # Match (url) with possible spaces
        match = re.search(r"\(\s*(.*?)\s*\)", value)
        url = match.group(1) if match else value.split(")")[0].split("(")[-1]
        # Ensure valid URL format
        if url.startswith(("http://", "https://")):
            return url
        return f"https://{url}" if "." in url else "#"
    except:
        return "#"
