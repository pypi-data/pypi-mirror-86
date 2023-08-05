import base64
from subprocess import Popen, PIPE, STDOUT

def decode_string(raw_bytes):
    try:
        return base64.b64decode(raw_bytes).decode("utf-8")
    except:
        return raw_bytes.decode("utf-8")


def decode_protobuf(raw_bytes, proto_dir, decode_msg_type, proto_file):
    decode_mode = '--decode'
    msg_type = decode_msg_type
    if decode_msg_type is None:
        decode_mode = '--decode_raw'
        msg_type = ''

    p = Popen(['protoc', decode_mode, msg_type, '--proto_path', proto_dir, proto_file], stdout=PIPE,
              stdin=PIPE, stderr=STDOUT)
    out = p.communicate(input=raw_bytes)
    if p.returncode != 0:
        return 'invalid protobuf'
    return out[0].decode()
