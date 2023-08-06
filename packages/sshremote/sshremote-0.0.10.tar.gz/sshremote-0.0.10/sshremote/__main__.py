import re
from argparse import ArgumentParser
from contextlib import contextmanager
from subprocess import check_output

from pydropbear import start_ssh_server
from pyngrok import ngrok


def get_user_name():
    return check_output(["whoami"]).decode().strip()


@contextmanager
def ngrok_context(auth_toke, port):
    ngrok.set_auth_token(args.ngrok_token)
    tunnel = ngrok.connect(args.port, "tcp", options={"bind_tls": True})
    yield tunnel
    ngrok.disconnect(tunnel.public_url)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("ngrok_token", type=str)
    arg_parser.add_argument("--port", type=int, default=8443)
    args = arg_parser.parse_args()

    user_name = get_user_name()

    with ngrok_context(args.ngrok_token, args.port) as tunnel:
        url, port = re.findall(r"//([a-z0-9.]+):(\d+)", tunnel.public_url)[0]
        connection_string = "ssh {}@{} -p {}".format(user_name, url, port)
        print('Type "{}" to connect'.format(connection_string))
        start_ssh_server(port=args.port)
