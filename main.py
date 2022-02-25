import argparse
import json
import requests
import tempfile
import subprocess
import multiprocessing
import math
import base64

def gen_OWNERID():
    ac = int(input("Access code > "))
    x = multiprocessing.cpu_count()
    y = multiprocessing.cpu_count() / 16 
    a = multiprocessing.cpu_count() * 2487^ ac
    z = ((x + y) * 6276 / (9580 ^ a)) * (x + y + a)
    return math.trunc(z * (int(x + y * a) ^ 4953) + ac)

tmp_file = tempfile.gettempdir()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--install", action="store")
parser.add_argument("-b", "--build", action="store")

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

        to_w = base64.b64decode(bytes(data["file"].encode()))

        with open(f"{tmp_file}/{inst}.deb", "wb") as f:
            f.write(to_w)
            f.close()
        print(f"Built {inst}, Installing now.")
        res = subprocess.run(f"sudo dpkg -i {tmp_file}/{inst}.deb", shell=True, stdout=subprocess.PIPE)
        print(res.stdout.decode("utf-8"))
        print("Installation complete")
elif args.build:
    with open(args.build, "rb") as f:
        bin = f.read()
    name = input("Name > ")
    oID = gen_OWNERID()
    data = requests.post(f"http://www.gek0.xyz:4563/deb/{name}", json={"deb": base64.b64encode(bin).decode('ascii'), "ownerID": str(oID), "private": False}).text
    print(data)