import argparse
import json
import requests
import tempfile
import subprocess

tmp_file = tempfile.gettempdir()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--install", action="store")

args = parser.parse_args()

if args.install:
    inst = args.install
    print(f"Installing {inst}")
    print(f"Requesting {inst} from the server")
    data = json.loads(requests.get(f"http://www.gek0.xyz:4563/deb/{inst}").text)
    try:
        data["error"]
        print(f"Message from server: {data['error']}")
    except KeyError:

        print(f"Building .deb file")
        with open(f"{tmp_file}/{inst}.deb", "wb") as f:
            f.write(bytes(data["file"].encode()))
            f.close()
        print(f"Built {inst}, Installing now.")
        res = subprocess.run(f"sudo dpkg -i {tmp_file}/{inst}.deb", shell=True, stdout=subprocess.PIPE)
        print(res.stdout.decode("utf-8"))
        print("Installation complete")