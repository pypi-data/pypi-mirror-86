import ctypes
import os
import signal
from subprocess import Popen, check_call

DROPBEAR_PID_PATH = "/tmp/dropbear.pid"
DROPBEAR_BIN = "dropbearmulti"
RSA_KEY_PATH = "/tmp/dropbear_rsa_key"


def set_pdeathsig(sig=signal.SIGTERM):
    libc = ctypes.CDLL("libc.so.6")

    def func():
        return libc.prctl(1, sig)

    return func


class SSHServer:
    def __init__(self, port=8443):
        root_path = os.path.dirname(os.path.abspath(__file__))
        self.bin_path = os.path.join(root_path, DROPBEAR_BIN)
        assert os.path.exists(self.bin_path)
        self.port = port

    def start(self):
        if os.path.exists(RSA_KEY_PATH):
            os.remove(RSA_KEY_PATH)

        check_call([self.bin_path, "dropbearkey", "-t", "rsa", "-f", RSA_KEY_PATH])

        cmd = [
            self.bin_path,
            "dropbear",
            "-p",
            str(self.port),
            "-P",
            DROPBEAR_PID_PATH,
            "-F",  # foreground
            "-E",  # log to stderr
            "-r",
            RSA_KEY_PATH,
        ]
        self._server = Popen(cmd, preexec_fn=set_pdeathsig(signal.SIGTERM))

    def close(self):
        self._server.kill()

    def __enter__(self):
        self.start()

    def __exit__(self, *args):
        self.close()
