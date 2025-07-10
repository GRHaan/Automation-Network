"""
네트워크 자동화를 위한 시스코 'show run' 명령어를 자동으로 백업하는 파이프라인 구축"
"""

from netmiko import ConnectHandler
from datetime import datetime
import os
import sys
import yaml

USERNAME = os.getenv("DEVICE_USERNAME")
PASSWORD = os.getenv("DEVICE_PASSWORD")
SECRET = os.getenv("DEVICE_SECRET")

def load_device(yaml_path='device.yaml'):
    with open(yaml_path, "r") as file:
        return yaml.safe_load(file)
    
def save_to_config (ip, config):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"backup_{ip}_{timestamp}.txt"
    os.makedirs("backups", exist_ok = True)
    filepath = os.path.join("backups", filename)

    with open(filepath, "w") as f:
        f.write(config_text)
    
    print(f"백업 저장 완료: {filepath}")

def backup_device(device):
    print(f"{device['host']}에 연결 중...")

    conn_info = {
        "device_type": device["device_type"],
        "host": device["host"],
        "username": USERNAME,
        "password": PASSWORD,
        "secret": SECRET,
    }

    try:
        net_connect = ConnectHandler(**conn_info)
        net_connect.enable()
        output = net_connect.send_command("show running-config")
        net_connect.disconnect()
        save_to_file(device["host"], output)

    except Exception as e:
        print(f"{device["host"]} 백업 실패: {e}")
        return False
    
    return True

def main():
    devices = load_device()
    success_count = 0

    for device in devices:
        if backup_device(device):
            success_count += 1

    print(f"\n총 {success_count}/{len(devices)}대 백업에 성공했습니다.")

if __name__ == "__main__":
    main()
