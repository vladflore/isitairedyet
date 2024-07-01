from models import Series
from pyweb import pydom


def createElement(
    tag: str, text_content: str = " ", inner_html: str = "", scope: str = ""
):

    element = pydom.create(tag)
    if text_content:
        element._js.textContent = text_content
    if inner_html:
        element.html = inner_html
    if scope:
        element.scope = scope
    return element
