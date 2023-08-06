import argparse
from .server import start_ssh_server


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--port", type=int, default=8443)
    arg_parser.add_argument("--bg", type=bool, default=False)
    args = arg_parser.parse_args()

    start_ssh_server(port=args.port, background=args.bg)
