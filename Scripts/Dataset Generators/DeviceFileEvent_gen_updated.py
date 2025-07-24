
import os
import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
output_dir = "C:\\Output"
os.makedirs(output_dir, exist_ok=True)

TENANT_ID = "d63f3f4b-6e5b-4e10-a8b8-2d7e2a8b5f72"
DEVICE_NAMES = ["DC-AD-01", "HR-LPT-001", "SOC-MON-02", "SQLSVR-01"]
ACCOUNT_DOMAINS = ["nt authority", "azuread", "kustoindustries"]
ACTION_TYPES = ["FileCreated", "FileDeleted", "FileModified", "FileRead", "FileRenamed"]
FILE_NAMES = ["readme.txt", "payload.exe", "invoice.pdf", "backdoor.ps1"]
FOLDER_PATHS = [
    "C:\\Users\\Public", "C:\\Windows\\Temp", "C:\\ProgramData\\Microsoft",
    "/tmp", "/home/user", "/var/tmp"
]
COMMAND_LINES = [
    "powershell.exe -ExecutionPolicy Bypass -File 'C:\\Scripts\\Deploy.ps1'",
    "cmd.exe /c del C:\\Temp\\malware.exe",
    "python3 /tmp/backdoor.py",
    "sh /tmp/init.sh"
]

def random_sid():
    return "S-1-5-21-" + "-".join(str(random.randint(1000000000, 9999999999)) for _ in range(3))

def random_hex(n):
    return ''.join(random.choices('0123456789abcdef', k=n))

def generate_additional_fields(account_name):
    return json.dumps({
        "InitiatingProcessPosixEffectiveUser": {
            "Name": account_name,
            "Uid": random.choice([0, 1000])
        },
        "InitiatingProcessPosixProcessGroupId": random.randint(1000, 9999),
        "InitiatingProcessPosixSessionId": random.randint(1000, 9999),
        "Campaign": "TANGOFOX_Ransom"
    })

def generate_event(index, start_time, delta):
    event_time = start_time + (index * delta)
    account_name = fake.user_name()
    action = random.choice(ACTION_TYPES)
    folder = random.choice(FOLDER_PATHS)
    filename = random.choice(FILE_NAMES)

    return {
        "TenantId": TENANT_ID,
        "AccountDomain": random.choice(ACCOUNT_DOMAINS),
        "AccountName": account_name,
        "AccountSid": random_sid(),
        "DeviceId": str(fake.uuid4()),
        "DeviceName": random.choice(DEVICE_NAMES),
        "FileName": filename,
        "FolderPath": folder,
        "FileSize": random.randint(2048, 100_000_000),
        "ActionType": action,
        "AdditionalFields": generate_additional_fields(account_name),
        "InitiatingProcessCommandLine": random.choice(COMMAND_LINES),
        "TimeGenerated": event_time.isoformat(),
        "Timestamp": event_time.isoformat(),
        "MD5": random_hex(32),
        "SHA1": random_hex(40),
        "SHA256": random_hex(64),
        "Type": "DeviceFileEvents"
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
    output_file = os.path.join(output_dir, "device_file_events.json")
    generate_events(total, start_time, end_time, output_file)
    print(f"✓ Generated {total} DeviceFileEvents to '{output_file}'")
