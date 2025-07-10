"""
한드림넷 스위치 'show running-config' 명령어를 백업하는 스크립트 (Netmiko 사용)
"""

from netmiko import ConnectHandler
from datetime import datetime
import os
import yaml

USERNAME = os.getenv("HANDREAMNET_USERNAME")
PASSWORD = os.getenv("HANDREAMNET_PASSWORD")
SECRET = os.getenv("HANDREAMNET_SECRET")
COMMAND = os.getenv("HANDREAMNET_COMMAND", "show running-config")

def load_device(yaml_path='device_handreamnet.yaml'):
    with open(yaml_path, "r") as file:
        return yaml.safe_load(file)

def save_to_file(device, config_text):
    name = device.get("name", device["host"])
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    folder = "backups/handreamnet"
    os.makedirs(folder, exist_ok=True)
    filename = f"backup_{name}_{timestamp}.txt"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w") as f:
        f.write(config_text)

    print(f"한드림넷 백업 저장 완료: {filepath}")

def backup_device(device):
    print(f"{device['host']}에 연결 중...")

    conn_info = {
        "device_type": "cisco_ios",
        "host": device["host"],
        "username": USERNAME,
        "password": PASSWORD,
        "secret": SECRET,
        "fast_cli": False,
    }

    try:
        net_connect = ConnectHandler(**conn_info)
        net_connect.enable()
        output = net_connect.send_command(COMMAND)
        net_connect.disconnect()
        save_to_file(device, output)

    except Exception as e:
        print(f"{device['host']} 백업 실패: {e}")
        return False

    return True

def main():
    devices = load_device()
    success_count = 0

    for device in devices:
        if backup_device(device):
            success_count += 1

    print(f"\n총 {success_count}/{len(devices)}대 한드림넷 장비 백업에 성공했습니다.")

if __name__ == "__main__":
    main()
