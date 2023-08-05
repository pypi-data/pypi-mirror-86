#!/usr/bin/python3
import logging
import sshcontroller

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

HOST_IP = "10.60.16.63"  # an IPv4 or IPv6 address
KEY_PWD = ""
SSH_PWD = ""


def demo_key():
    ssh_controller = sshcontroller.SSHController(
        host=HOST_IP,
        user="olivier",
        key_path=None,  # if omitted, look for keys in SSH agent and in ~/.ssh/
        key_password=None,      # optional
        key_type="rsa",            # rsa (default), dsa, ecdsa or ed25519
        port=22,                   # 22 is the default
    )

    ssh_controller.connect()

    return_code, output = ssh_controller.run(
        command="ip addr show dev etete",
        display=True,          # display output, false by default
        capture_output=True,   # return output, false by default
        shell=True,
        combine_stderr=False,  # combine stderr and stdout, false by default
        timeout=10,            # command timeout in seconds, 600s by default
    )
    logging.info(f"return code: {return_code}, output: {output}")


demo_key()
