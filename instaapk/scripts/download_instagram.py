#!/usr/bin/env python3


from gplayapi.fetch import login, device_checkin, get_instagram_download_url
import requests

email = "your_email@gmail.com"
password = "your_password"

print("[*] Logging in...")
auth_token = login(email, password)

print("[*] Performing check-in...")
android_id, _ = device_checkin()

print("[*] Fetching Instagram APK URL...")
apk_url = get_instagram_download_url(auth_token, str(android_id))

print(f"[*] APK URL: {apk_url}")

print("[*] Downloading APK...")
apk_data = requests.get(apk_url).content
with open("Instagram_Latest.apk", "wb") as f:
    f.write(apk_data)

print("[+] Done! APK saved as Instagram_Latest.apk")
