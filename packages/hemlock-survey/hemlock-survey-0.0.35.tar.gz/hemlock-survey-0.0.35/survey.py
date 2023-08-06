from hemlock import (
    Branch, Page, Embedded, Blank, Binary, Check, Input, Label, Range, Textarea, 
    Compile as C, Validate as V, route, settings
)
from hemlock.tools import consent_page, completion_page

from flask_login import current_user

@route('/survey')
def start():
    return Branch(
        consent_page(),
        completion_page()
    )