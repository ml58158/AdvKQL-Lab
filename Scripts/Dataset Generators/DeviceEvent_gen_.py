
import json
import random
import os
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Constants
TENANT_ID = "d63f3f4b-6e5b-4e10-a8b8-2d7e2a8b5f72"
DOMAIN = "KustoIndustries"
OUTPUT_DIR = "C:\\Output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "device_events.json")

DEVICE_NAME_OPTIONS = [
    "DC-AD-01", "DC-AD-02", "FN-WKSTN-001", "FN-WKSTN-002", "FN-WKSTN-003",
    "HR-LPT-001", "HR-LPT-002", "HR-LPT-003", "HR-LPT-004",
    "SOC-MON-01", "SOC-MON-02", "AVD-POOL-01", "AVD-POOL-02",
    "AD-CTRL-01", "AD-CTRL-02", "WFILE-SRV-01", "EX-SRV-01", "SQLSVR-01",
    "APPSVR-01", "FTPSVR-01", "BAKSVR-01", "HYPVIS-01", "WEBSVR-01",
    "govms01.kustoindustries.net", "govms02.kustoindustries.net", "govms03.kustoindustries.net",
    "govms04.kustoindustries.net", "govms05.kustoindustries.net", "govms06.kustoindustries.net",
    "eidcloudsync01.kustoindustries.net"
]

ACTION_TYPES = [
    "ScheduledTaskCreated", "ScriptContent", "PowerShellCommand", "PasswordChangeAttempt",
    "RemoteDesktopConnection", "ScheduledTaskEnabled", "SecurityGroupCreated",
    "ServiceInstalled", "TamperingAttempt", "UserAccountCreated", "UserAccountModified",
    "WriteToLsassProcessMemory"
]

# Preset realistic command mappings (for process simulation)
COMMAND_MAP = {
    "PowerShellCommand": "powershell.exe -Command \"Invoke-Mimikatz\"",
    "ScheduledTaskCreated": "schtasks.exe /Create /SC DAILY /TN \"WannaCryTask\" /TR \"encryptor.exe\"",
    "WriteToLsassProcessMemory": "mimikatz.exe privilege::debug sekurlsa::logonpasswords",
    "UserAccountCreated": "net user attacker P@ssword123 /add",
    "UserAccountModified": "net user administrator /active:yes",
    "ServiceInstalled": "sc.exe create mssecsvc binpath= \"C:\\malware\\svc.exe\"",
    "ScriptContent": "script.py",
    "PasswordChangeAttempt": "net user admin NewP@ss123",
    "RemoteDesktopConnection": "mstsc /v:192.168.1.5",
    "SecurityGroupCreated": "net localgroup \"Remote Desktop Users\" eviluser /add",
    "ScheduledTaskEnabled": "schtasks /Change /TN \"WannaCryTask\" /ENABLE",
    "TamperingAttempt": "reg delete HKLM\\Software\\Defender /f"
}

# TTP mappings
ADDITIONAL_FIELDS_MAP = {
    "ScheduledTaskCreated": {
        "Tactic": "Persistence",
        "Technique": "T1053.005",
        "TaskName": "WannaCryTask",
        "Trigger": "At logon",
        "Command": "tasksche.exe"
    },
    "ScheduledTaskEnabled": {
        "Tactic": "Persistence",
        "Technique": "T1053.005",
        "TaskName": "WannaCryTask",
        "Status": "Enabled"
    },
    "ServiceInstalled": {
        "Tactic": "Persistence",
        "Technique": "T1543.003",
        "ServiceName": "mssecsvc",
        "Path": "C:\\ProgramData\\Service0\\tasksche.exe",
        "Arguments": "/silent /autorun"
    },
    "TamperingAttempt": {
        "Tactic": "Defense Evasion",
        "Technique": "T1112",
        "RegistryKey": "HKLM\\Software\\Policies\\Microsoft\\Windows Defender",
        "Action": "DeleteKey",
        "Tool": "reg.exe"
    },
    "UserAccountCreated": {
        "Tactic": "Persistence",
        "Technique": "T1136.001",
        "Username": "supportsvc",
        "Role": "Administrator",
        "Method": "net user"
    },
    "UserAccountModified": {
        "Tactic": "Privilege Escalation",
        "Technique": "T1098",
        "Username": "admin",
        "FieldChanged": "passwordNeverExpires",
        "NewValue": "true"
    },
    "PasswordChangeAttempt": {
        "Tactic": "Credential Access",
        "Technique": "T1110.004",
        "Username": "admin",
        "Status": "Failed",
        "TargetSystem": "DC-AD-01"
    },
    "RemoteDesktopConnection": {
        "Tactic": "Lateral Movement",
        "Technique": "T1021.001",
        "TargetHost": "HR-LPT-002",
        "Username": "eviladmin",
        "AuthMethod": "Password"
    },
    "WriteToLsassProcessMemory": {
        "Tactic": "Credential Access",
        "Technique": "T1003.001",
        "ProcessName": "lsass.exe",
        "AccessType": "WriteProcessMemory",
        "Tool": "mimikatz.exe"
    },
    "SecurityGroupCreated": {
        "Tactic": "Persistence",
        "Technique": "T1098.002",
        "GroupName": "Remote Desktop Users",
        "Members": ["supportsvc"],
        "Scope": "Local"
    }
}

def random_sid():
    return f"S-1-5-21-{random.randint(1000000000,9999999999)}-{random.randint(1000000000,9999999999)}-{random.randint(1000000000,9999999999)}"

def generate_additional_fields(action_type, account_name):
    fields = ADDITIONAL_FIELDS_MAP.get(action_type, {"Command": COMMAND_MAP.get(action_type, "cmd.exe")})
    fields["Campaign"] = "TANGOFOX_Ransom"
    fields["UserContext"] = f"{account_name}@{DOMAIN}"
    return json.dumps(fields)

def generate_device_event(index, start_time, delta):
    event_time = start_time + (index * delta)
    action_type = random.choice(ACTION_TYPES)
    account_name = fake.user_name()
    return {
        "TenantId": TENANT_ID,
        "TimeGenerated": event_time.isoformat(),
        "DeviceName": random.choice(DEVICE_NAME_OPTIONS),
        "DeviceId": fake.uuid4(),
        "ActionType": action_type,
        "AccountDomain": DOMAIN,
        "AccountName": account_name,
        "AccountSid": random_sid(),
        "FolderPath": f"C:\\Users\\{account_name}\\AppData\\Local\\Temp",
        "FileName": COMMAND_MAP.get(action_type, "unknown.exe").split()[-1].replace('"', ''),
        "InitiatingProcessCommandLine": COMMAND_MAP.get(action_type, "cmd.exe /c whoami"),
        "InitiatingProcessId": random.randint(2000, 9999),
        "InitiatingProcessAccountName": account_name,
        "InitiatingProcessAccountDomain": DOMAIN,
        "InitiatingProcessLogonId": random.randint(10000, 99999),
        "RemoteDeviceName": random.choice(DEVICE_NAME_OPTIONS),
        "RemoteIP": fake.ipv4(),
        "RemotePort": random.randint(1000, 65535),
        "SourceSystem": "Custom",
        "Type": "DeviceEvents",
        "AdditionalFields": generate_additional_fields(action_type, account_name)
    }

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    days = 3
    records_per_day = 1000
    total = days * records_per_day
    start_time = datetime.now() - timedelta(days=days)
    delta = timedelta(seconds=(24 * 60 * 60) / records_per_day)

    with open(OUTPUT_FILE, "w") as f:
        for i in range(total):
            json.dump(generate_device_event(i, start_time, delta), f)
            f.write("\n")

    print(f"[✓] Generated {total} DeviceEvents -> {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
