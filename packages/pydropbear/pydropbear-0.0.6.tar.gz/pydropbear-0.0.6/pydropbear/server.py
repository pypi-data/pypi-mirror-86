import ctypes
import os
import signal
from contextlib import contextmanager
from subprocess import check_call

DROPBEAR_PID_PATH = "/tmp/dropbear.pid"
DROPBEAR_BIN = "dropbearmulti"
KEY_PATH = "/tmp/dropbear_{key_type}_key"


def set_pdeathsig(sig=signal.SIGTERM):
    libc = ctypes.CDLL("libc.so.6")

    def func():
        return libc.prctl(1, sig)

    return func


def _get_bin_path():
    root_path = os.path.dirname(os.path.abspath(__file__))
    bin_path = os.path.join(root_path, DROPBEAR_BIN)
    assert os.path.exists(bin_path)
    check_call(["chmod", "+x", bin_path])
    return bin_path


def provide_key(key_type="rsa"):
    key_path = KEY_PATH.format(key_type=key_type)
    if not os.path.exists(key_path):
        check_call([_get_bin_path(), "dropbearkey", "-t", key_type, "-f", key_path])

    return key_path


def start_ssh_server(port=8443, background=False):

    cmd = [
        _get_bin_path(),
        "dropbear",
        "-p",
        str(port),
        "-P",
        DROPBEAR_PID_PATH,
        "-E",  # log to stderr
        "-r",
        provide_key(),
    ]
    if not background:
        cmd.append("-F")  # foreground

    check_call(cmd)


@contextmanager
def ssh_server_context(port=8443):
    start_ssh_server(port=port, background=False)
    yield
