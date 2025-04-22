import requests
import random
from gplayapi.protos import checkin_pb2

GOOGLE_LOGIN_URL = "https://android.clients.google.com/auth"
DEVICE_CHECKIN_URL = "https://android.clients.google.com/checkin"
USER_AGENT = "Android-Finsky/24.3.16 (api=3,versionCode=82431600,sdk=31,device=Pixel6,hardware=google,product=oriole)"

def get_random_android_id():
    return ''.join(random.choices('abcdef0123456789', k=16))

def login(email: str, password: str) -> str:
    data = {
        "Email": email,
        "Passwd": password,
        "service": "androidmarket",
        "accountType": "HOSTED_OR_GOOGLE",
        "has_permission": "1",
        "source": "android",
        "androidId": get_random_android_id(),
        "app": "com.android.vending",
        "client_sig": "38918a453d07199354f8b19af05ec6562ced5788",
        "device_country": "us",
        "lang": "en",
        "sdk_version": "31"
    }

    headers = {"User-Agent": "GoogleLoginService/1.3"}

    response = requests.post(GOOGLE_LOGIN_URL, data=data, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Login failed: {response.text}")

    parsed = dict(line.split("=", 1) for line in response.text.strip().split("\n"))
    return parsed["Auth"]

def device_checkin() -> tuple:
    req = checkin_pb2.CheckinRequest()
    req.id = 0
    req.android_id = 0
    req.checkin.build.fingerprint = "google/sdk_gphone64_x86_64/generic_x86_64:11/RSR1/123456:userdebug/dev-keys"
    req.checkin.build.hardware = "ranchu"
    req.locale = "en_US"
    req.version = 3

    headers = {
        "User-Agent": "Android-Checkin/2.0 (generic_x86_64 userdebug RSR1.123456)",
        "Content-Type": "application/x-protobuffer"
    }

    res = requests.post(DEVICE_CHECKIN_URL, headers=headers, data=req.SerializeToString())
    resp = checkin_pb2.CheckinResponse()
    resp.ParseFromString(res.content)
    return resp.android_id, resp.security_token

def get_instagram_download_url(auth_token: str, android_id: str) -> str:
    headers = {
        "Authorization": f"GoogleLogin auth={auth_token}",
        "User-Agent": USER_AGENT,
        "X-DFE-Device-Id": android_id,
        "X-DFE-MCCMNC": "310260",
        "X-DFE-Client-Id": "am-android-google",
        "X-DFE-Logging-Id": "random-id",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    url = "https://android.clients.google.com/fdfe/details?doc=com.instagram.android"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise Exception("Failed to get app details.")

    # TODO: Proto parsing needed here
    raise NotImplementedError("Parsing of the delivery data not yet implemented.")
