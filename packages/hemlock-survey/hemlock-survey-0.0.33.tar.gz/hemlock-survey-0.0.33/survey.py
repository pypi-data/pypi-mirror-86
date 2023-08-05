from hemlock import (
    Branch, Page, Embedded, Binary, Check, Input, Label, Range, Textarea, 
    Compile as C, Validate as V, route, settings
)

settings['collect_IP'] = False

@route('/survey')
def start():
    return Branch(
        Page(
            Label('Page 1'),
            navigate=middle,
            navigate_worker=True
        ),
        navigate=end,
        navigate_worker=True
    )

def middle(origin):
    delay(origin)
    return Branch()

def end(origin):
    delay(origin)
    return Branch(
        Page(
            Label('Page 6'),
            back=True
        )
    )

def delay(obj=None):
    print('object is', obj)
    import time
    for i in range(3):
        print(i)
        time.sleep(1)