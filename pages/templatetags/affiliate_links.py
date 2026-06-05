import html
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

A_TAG_RE = re.compile(r"<a\b(?P<attrs>[^>]*)>", re.IGNORECASE | re.DOTALL)
HREF_RE = re.compile(
    r"(?P<prefix>\bhref\s*=\s*)(?P<quote>[\"'])(?P<url>.*?)(?P=quote)",
    re.IGNORECASE | re.DOTALL,
)
TARGET_RE = re.compile(
    r"(?P<prefix>\btarget\s*=\s*)(?P<quote>[\"'])(?P<value>.*?)(?P=quote)",
    re.IGNORECASE | re.DOTALL,
)
REL_RE = re.compile(
    r"(?P<prefix>\brel\s*=\s*)(?P<quote>[\"'])(?P<value>.*?)(?P=quote)",
    re.IGNORECASE | re.DOTALL,
)


def _amazon_hosts():
    return {host.lower() for host in getattr(settings, "AMAZON_MARKETPLACE_HOSTS", ())}


def _associate_tag():
    return getattr(settings, "AMAZON_ASSOCIATE_TAG", "").strip()


def _split_url(url):
    try:
        return urlsplit(html.unescape(str(url)).strip())
    except ValueError:
        return None


def _is_amazon_marketplace_url(url):
    parts = _split_url(url)
    if not parts or parts.scheme not in {"http", "https"}:
        return False
    return parts.netloc.lower() in _amazon_hosts()


def _tagged_amazon_url(url):
    tag = _associate_tag()
    parts = _split_url(url)
    if not tag or not parts or parts.scheme not in {"http", "https"}:
        return str(url)

    if parts.netloc.lower() not in _amazon_hosts():
        return str(url)

    query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if key.lower() != "tag"
    ]
    query.append(("tag", tag))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def _set_target_blank(attrs):
    match = TARGET_RE.search(attrs)
    if match:
        return (
            attrs[: match.start("value")]
            + "_blank"
            + attrs[match.end("value") :]
        )
    return f'{attrs} target="_blank"'


def _merge_rel(attrs):
    required = {"nofollow", "sponsored", "noopener"}
    match = REL_RE.search(attrs)
    if not match:
        return f'{attrs} rel="nofollow sponsored noopener"'

    values = {value for value in match.group("value").split() if value}
    values.update(required)
    rel_value = " ".join(sorted(values))
    return attrs[: match.start("value")] + rel_value + attrs[match.end("value") :]


def _rewrite_anchor(match):
    attrs = match.group("attrs")
    href = HREF_RE.search(attrs)
    if not href:
        return match.group(0)

    original_url = href.group("url")
    if not _is_amazon_marketplace_url(original_url):
        return match.group(0)

    tagged_url = html.escape(_tagged_amazon_url(original_url), quote=True)
    attrs = attrs[: href.start("url")] + tagged_url + attrs[href.end("url") :]
    attrs = _set_target_blank(attrs)
    attrs = _merge_rel(attrs)
    return f"<a{attrs}>"


@register.filter
def amazon_affiliate_url(url):
    return _tagged_amazon_url(url)


@register.filter
def is_amazon_marketplace_url(url):
    return _is_amazon_marketplace_url(url)


@register.filter
def contains_amazon_link(value):
    if not value:
        return False
    return bool(A_TAG_RE.search(str(value))) and any(host in str(value).lower() for host in _amazon_hosts())


@register.filter
def amazon_affiliate_content(value):
    if not value:
        return ""
    return mark_safe(A_TAG_RE.sub(_rewrite_anchor, str(value)))
