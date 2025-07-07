import os, json, random
from datetime import datetime, timedelta
from faker import Faker
from collections import OrderedDict

output_dir = "C:\\Output"
os.makedirs(output_dir, exist_ok=True)
fake = Faker()

def generate_event(ts):
    record = OrderedDict()
    record["ActionType"] = random.choice(["RegistryValueSet", "RegistryKeyCreated"])
    record["AppGuardContainerId"] = str(fake.uuid4())
    record["DeviceId"] = str(fake.uuid4())
    record["DeviceName"] = random.choice(["FN-WKSTN-001", "HR-LPT-001"])
    record["InitiatingProcessAccountDomain"] = "KustoIndustries"
    record["InitiatingProcessAccountName"] = fake.user_name()
    record["InitiatingProcessAccountObjectId"] = str(fake.uuid4())
    record["InitiatingProcessAccountSid"] = "S-1-5-21-" + "-".join(str(random.randint(1000000000,9999999999)) for _ in range(3))
    record["InitiatingProcessAccountUpn"] = fake.email()
    record["InitiatingProcessCommandLine"] = "reg add HKCU\Software\Example /v setting /t REG_SZ /d value"
    record["InitiatingProcessCreationTime"] = ts.isoformat()
    record["InitiatingProcessFileName"] = "reg.exe"
    record["InitiatingProcessFileSize"] = 123456
    record["InitiatingProcessFolderPath"] = "C:\\Windows\\System32"
    record["InitiatingProcessId"] = 6789
    record["InitiatingProcessIntegrityLevel"] = "High"
    record["InitiatingProcessMD5"] = ''.join(random.choices('0123456789abcdef', k=32))
    record["InitiatingProcessParentCreationTime"] = ts.isoformat()
    record["InitiatingProcessParentFileName"] = "cmd.exe"
    record["InitiatingProcessParentId"] = 1234
    record["InitiatingProcessRemoteSessionDeviceName"] = ""
    record["InitiatingProcessRemoteSessionIP"] = ""
    record["InitiatingProcessSessionId"] = random.randint(1000, 9999)
    record["InitiatingProcessSHA1"] = ''.join(random.choices('0123456789abcdef', k=40))
    record["InitiatingProcessSHA256"] = ''.join(random.choices('0123456789abcdef', k=64))
    record["InitiatingProcessTokenElevation"] = "TokenElevationTypeFull"
    record["InitiatingProcessUniqueId"] = str(fake.uuid4())
    record["InitiatingProcessVersionInfoCompanyName"] = "Microsoft Corporation"
    record["InitiatingProcessVersionInfoFileDescription"] = "Registry Editor"
    record["InitiatingProcessVersionInfoInternalFileName"] = "reg.exe"
    record["InitiatingProcessVersionInfoOriginalFileName"] = "reg.exe"
    record["InitiatingProcessVersionInfoProductName"] = "Windows OS"
    record["InitiatingProcessVersionInfoProductVersion"] = "10.0.19041.1"
    record["IsInitiatingProcessRemoteSession"] = False
    record["MachineGroup"] = "UnassignedGroup"
    record["PreviousRegistryKey"] = "HKCU\Software\Example"
    record["PreviousRegistryValueData"] = "old_value"
    record["PreviousRegistryValueName"] = "setting"
    record["RegistryKey"] = "HKCU\Software\Example"
    record["RegistryValueData"] = "new_value"
    record["RegistryValueName"] = "setting"
    record["RegistryValueType"] = "REG_SZ"
    record["ReportId"] = random.randint(100000, 999999)
    record["SourceSystem"] = ""
    record["TenantId"] = "d63f3f4b-6e5b-4e10-a8b8-2d7e2a8b5f72"
    record["TimeGenerated"] = ts.isoformat()
    record["Timestamp"] = ts.isoformat()
    record["Type"] = "DeviceRegistryEvents"
    return record

def generate_events(count=100):
    base = datetime.utcnow()
    delta = timedelta(minutes=1)
    with open(os.path.join(output_dir, "device_registry_events.json"), "w", encoding="utf-8") as f:
        for i in range(count):
            ts = base - i * delta
            f.write(json.dumps(generate_event(ts)) + "\n")

if __name__ == "__main__":
    generate_events()
