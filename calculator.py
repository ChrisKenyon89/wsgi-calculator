"""
For your homework this week, you'll be creating a wsgi application of
your own.
You'll create an online calculator that can perform several operations.
You'll need to support:
  * Addition
  * Subtractions
  * Multiplication
  * Division
Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.
Consider the following URL/Response body pairs as tests:
```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```
To submit your homework:
  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!
"""


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    # TODO: Fill sum with the correct value, based on the
    # args provided.
    a = args[0]
    b = args[1]    
    summ = int(a) + int(b)
    return str(summ)

# TODO: Add functions for handling more arithmetic operations.

def subtract(*args):
    """subtract two integers"""
    a = args[0]
    b = args[1]
    result = int(a) - int(b)
    return str(result)

def multiply(*args):
    """multiply two integers"""
    c = args[0]
    d = args[1]
    product = int(c)*int(d)
    return str(product) 

def divide(*args):
    """divide two integers"""
    e = args[0]
    f = args[1]
    #if int(f) == 0:
        #return 'Division by 0 is undefined'
    quotient = int(e)/int(f)
    return str(quotient)

def home(*args):
    page = '''
        <html>
        add
        </html>
        '''
    return page
       
        
def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    method = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
        'home': home,
    }
    path = path.strip('/').split('/')
    
    entry = path[0]
    args = path[1:] 
    if entry == 'add':
        selection = 'add'
    elif entry == 'subtract':
        selection = 'subtract'
    elif entry == 'multiply':
        selection = 'multiply'
    elif entry == 'divide':
        selection = 'divide'
    elif entry == '':
        selection = 'home'
    try:
        func = method[selection]
    except KeyError:
        raise NameError
    return func, args

def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        # print(path)
        # print(e)
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Division by zero is undefined</h1>"         
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"       
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
