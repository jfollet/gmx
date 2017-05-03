import json
from urllib.parse import parse_qs

this_title = ""
this_val = None
this_leq = lambda x, y: False
this_new = lambda: ""

content_template = """
<body>
<h1>{}</h1>
<p>{}</p>
<form method="get" action="/guess/" target="_self">
    <input type=text name=guess>
    <input type=submit value="Guess!">
</form>
<form method="post" action="/reset/" target="_self">
    <input type=submit value="Reset!">
</form>
</body>
"""


def title(environ):
    return content_template.format(this_title, "")


def guess(environ):
    get_variables = parse_qs(environ['QUERY_STRING'])
    the_guess = get_variables['guess'][0]

    if this_leq(this_val, the_guess) and this_leq(the_guess, this_val):
        message = "Correct!"
    elif this_leq(this_val, the_guess):
        message = "Too high!"
    else:
        message = "Too low!"

    return content_template.format(this_title, message)


def reset(environ):
    global this_val
    this_val = this_new()

    return content_template.format(this_title, "Value reset!")


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments, based on the path.
    """

    func_name = path.strip("/").split("/")[0]

    func = {
        "": title,
        "guess": guess,
        "reset": reset,
    }[func_name]

    return func


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func = resolve_path(path)
        body = func(environ)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


def run(title, leq, new):
    global this_leq, this_new, this_val, this_title

    this_title = title
    this_leq = leq
    this_new = new
    this_val = new()

    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
