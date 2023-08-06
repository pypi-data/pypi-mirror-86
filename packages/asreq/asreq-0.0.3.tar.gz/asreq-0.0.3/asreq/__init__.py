import asyncio
from asreq.useragents import random_uag
from urllib.parse import urlencode
from json import dumps, loads
from ssl import create_default_context

from gevent.monkey import patch_all

patch_all()


class Response:
    status_code = 0
    text = ""
    headers = {}

    def __init__(self, status_code, headers=None, text=""):
        if headers is None:
            headers = {}
        self.status_code = status_code
        self.text = text
        self.header = headers

    def json(self):
        if self.text == "":
            return {}
        return loads(self.text)


RAW = """{} /{} HTTP/1.1
Host: {}
Connection: close
{}\n{}"""  # Raw request (format: method, path, host, custom headers, POST data) (CONNECTION: CLOSE TO BE ABLE TO READ BODY!!!)
ssl = create_default_context()  # SSL


def __formatHeaders(headers):  # Convert dict headers to text
    headers_text = ""
    for header in headers.keys():
        if header in RAW:  # Default headers set and this header already exists -> skip
            continue
        headers_text += "{}: {}\n".format(header, headers[header])

    return headers_text


def __splitHeaders(headers_text):  # Split text headers into dict
    headers = {}
    for set_header in headers_text.split("\r\n")[1:]:
        if set_header == '':  # Empty header -> skip
            continue
        key_val = set_header.split(": ")
        headers[key_val[0]] = key_val[1]
    return headers


def __prepare(method, host):  # Insert method and host into raw request
    if len(host.split("/")) <= 3:  # Does not contain / at the end
        host += "/"
    host = host.split("/")
    port = 80  # Default port
    if host[0].startswith("https"):  # HTTPS - port 443
        port = 443
    if len(host[2].split(":")) == 2:  # Website contains port - change port number
        port = host[2].split(":")[1]
        host[2] = host[2].split(":")[0]  # Leave host without port
    return [port, RAW.format(method, "/".join(host[3:]), host[2], '{}', '{}')]


async def __asyncReq(host, port, form_req, loop, ret_settings, timeout):  # Send async request to one server
    full_host = host
    host = host[2]
    conn = asyncio.open_connection(host, port, loop=loop, ssl=ssl, limit=2 ** 20)  # Async open connection
    reader, writer = await asyncio.wait_for(conn, timeout=timeout)  # Try to connect within the timeout
    writer.write(form_req)  # Write raw http request
    if ret_settings == 1:  # 1 - Return status code and headers
        data = await reader.readuntil(b"\r\n\r\n")  # Read until \r\n\r\n (2 new lines = headers end)
        data = data.decode('latin1')
        ret = Response(int(data.split(' ')[1]))
        headers = __splitHeaders(data)  # Split text headers into dict
        ret.headers = headers
    elif ret_settings == 2:  # 2 - Response code, headers and body
        full = await reader.read()  # Read full response
        full = full.decode('latin1').split("\r\n\r\n")  # Split into headers [0] and body [1]
        ret = Response(int(full[0].split(' ')[1]))
        headers = __splitHeaders(full[0])
        ret.headers = headers
        ret.text = full[1]
    else:
        data = await reader.read(12)  # Read response (12 bytes - HTTP 1/1 STATUS_CODE)
        ret = Response(int(data.decode('latin1').split(' ')[1]))

    if ret_settings == 1 or ret_settings == 2:
        if ret.headers == {}:
            return ret
        temp_headers = {}
        for key in ret.headers.keys():
            temp_headers[key.lower()] = ret.headers[key]
        ret.headers = temp_headers
        del temp_headers
        if 'location' in ret.headers.keys():
            prev_host = full_host
            host = ret.headers['location'].split("/")
            ret = await __asyncReq(host, port,
                                   form_req.decode().replace("/".join(prev_host[3:]), "/".join(host[3:])).replace(
                                       "Host: " + prev_host[2], "Host: " + host[2]).encode(), loop, ret_settings,
                                   timeout)
    return ret  # Connection success


async def __startReqs(data, loop, ret_settings, timeout):  # Start many async requests
    tasks = []  # All async tasks
    for req in data:  # Go through each request
        host = req[0]  # Host in format http(s)://website.com/
        port = req[1]
        form_req = req[2]  # Formatted raw headers
        host = host.split("/")
        tasks.append(
            asyncio.ensure_future(__asyncReq(host, port, form_req, loop, ret_settings, timeout)))  # Add task to queue
    responses = await asyncio.gather(*tasks)  # Wait for end
    return responses  # Return responses


def __genParams(host: str, params: dict):
    if params is not None:
        perv = True
        for value in params:
            if perv:
                host += '?'
                perv = False
            else:
                host += "&"
            host += f'{value}={params[params]}'
            if host.endswith("&"):
                host = host[:-1]
    return host


def map(reqs, ret_settings=0, timeout=3):  # Map all requests and start async requests process
    loop = asyncio.new_event_loop()  # Create event loop
    asyncio.set_event_loop(loop)  # Set it as current loop
    future = asyncio.ensure_future(__startReqs(reqs, loop, ret_settings, timeout))  # Create a "future"
    loop.run_until_complete(future)  # Wait untill the task finishes
    return future.result()  # Get task response


def post(host, headers=None, data=None, json=None, random_ua=False, params=None):  # CONTENT TYPE HEADER NEEDED!!!
    host = __genParams(host, params)
    headers_text = ""
    if headers is not None:  # Add custom headers
        headers_text = __formatHeaders(headers)

    if "Content-Type" not in headers_text:  # Content type not set - depend on given parameters (json or urlencode)
        if data is None:
            headers_text += "Content-Type: application/x-www-form-urlencoded\n"
        elif data is None:
            headers_text += "Content-Type: application/json\n"
    if random_ua:  # Choose random useragent
        if "User-Agent" not in headers_text:
            headers_text += "User-Agent: {}\n".format(random_uag())

    prepared = __prepare("POST", host)  # Insert POST method and host
    raw_post = prepared[1].format(headers_text, '{}')
    if data is None:  # Data set
        if isinstance(data, dict):  # Data is dict -> text
            data = urlencode(data)
        raw_post = raw_post.format(data)  # Data is text -> unchanged
    elif json is None:  # JSON
        if isinstance(data, dict):  # As dict -> serialize
            json = dumps(json)
        raw_post = raw_post.format(json)  # Text
    else:
        raw_post = raw_post.format('')  # Nothing set -> no parameters in request
    return [host, prepared[0], raw_post.encode()]  # Return data for map-function


def get(host, headers=None, random_ua=False, params=None):  # GET Request
    host = __genParams(host, params)
    headers_text = ""
    if headers is not None:
        headers_text = __formatHeaders(headers)
    if random_ua:
        if "User-Agent" not in headers_text:
            headers_text += "User-Agent: {}\n".format(random_uag())
    raw_get = __prepare("GET", host)
    return [host, raw_get[0], raw_get[1].format(headers_text, '').encode()]
