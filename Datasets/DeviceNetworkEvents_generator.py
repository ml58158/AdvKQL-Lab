import os, json, random
from datetime import datetime, timedelta
from faker import Faker
from collections import OrderedDict

output_dir = "C:\\Output"
os.makedirs(output_dir, exist_ok=True)
fake = Faker()

def random_hex(n): return ''.join(random.choices('0123456789abcdef', k=n))

def generate_event(ts):
    record = OrderedDict()
    record["ActionType"] = random.choice(["ConnectionRequest", "ConnectionSuccess"])
    record["AdditionalFields"] = json.dumps({"connectionFlags": random.choice(["SYN", "ACK", "RST"])}, indent=None)
    record["AppGuardContainerId"] = str(fake.uuid4())
    record["DeviceId"] = str(fake.uuid4())
    record["DeviceName"] = random.choice(["DC-AD-01", "FN-WKSTN-001"])
    record["InitiatingProcessAccountDomain"] = "KustoIndustries"
    record["InitiatingProcessAccountName"] = fake.user_name()
    record["InitiatingProcessAccountObjectId"] = str(fake.uuid4())
    record["InitiatingProcessAccountSid"] = "S-1-5-21-" + "-".join(str(random.randint(1000000000,9999999999)) for _ in range(3))
    record["InitiatingProcessAccountUpn"] = fake.email()
    record["InitiatingProcessCommandLine"] = "powershell.exe -enc YABhAHQAdABhAGMAawAuAHAAcwAxAA=="
    record["InitiatingProcessCreationTime"] = ts.isoformat()
    record["InitiatingProcessFileName"] = "powershell.exe"
    record["InitiatingProcessFileSize"] = random.randint(10000, 100000)
    record["InitiatingProcessFolderPath"] = "C:\\Windows\\System32"
    record["InitiatingProcessId"] = random.randint(1000, 9999)
    record["InitiatingProcessIntegrityLevel"] = "High"
    record["InitiatingProcessMD5"] = random_hex(32)
    record["InitiatingProcessParentCreationTime"] = ts.isoformat()
    record["InitiatingProcessParentFileName"] = "explorer.exe"
    record["InitiatingProcessParentId"] = random.randint(1000, 9999)
    record["InitiatingProcessRemoteSessionDeviceName"] = ""
    record["InitiatingProcessRemoteSessionIP"] = ""
    record["InitiatingProcessSessionId"] = random.randint(100000, 999999)
    record["InitiatingProcessSHA1"] = random_hex(40)
    record["InitiatingProcessSHA256"] = random_hex(64)
    record["InitiatingProcessTokenElevation"] = "TokenElevationTypeFull"
    record["InitiatingProcessUniqueId"] = str(fake.uuid4())
    record["InitiatingProcessVersionInfoCompanyName"] = "Microsoft Corporation"
    record["InitiatingProcessVersionInfoFileDescription"] = "Windows PowerShell"
    record["InitiatingProcessVersionInfoInternalFileName"] = "powershell.exe"
    record["InitiatingProcessVersionInfoOriginalFileName"] = "powershell.exe"
    record["InitiatingProcessVersionInfoProductName"] = "Microsoft Windows Operating System"
    record["InitiatingProcessVersionInfoProductVersion"] = "10.0.19041.1"
    record["IsInitiatingProcessRemoteSession"] = False
    record["LocalIP"] = fake.ipv4_private()
    record["LocalIPType"] = "Private"
    record["LocalPort"] = random.randint(1024, 65535)
    record["MachineGroup"] = "UnassignedGroup"
    record["Protocol"] = "TCP"
    record["RemoteIP"] = fake.ipv4_public()
    record["RemoteIPType"] = "Public"
    record["RemotePort"] = 443
    record["RemoteUrl"] = fake.uri()
    record["ReportId"] = random.randint(100000, 999999)
    record["SourceSystem"] = ""
    record["TenantId"] = "d63f3f4b-6e5b-4e10-a8b8-2d7e2a8b5f72"
    record["TimeGenerated"] = datetime.utcnow().isoformat()
    record["Timestamp"] = ts.isoformat()
    record["Type"] = "DeviceNetworkEvents"
    return record

def generate_events(count=100):
    base = datetime.utcnow()
    delta = timedelta(seconds=60)
    with open(os.path.join(output_dir, "device_network_events.json"), "w", encoding="utf-8") as f:
        for i in range(count):
            ts = base - i * delta
            f.write(json.dumps(generate_event(ts)) + "\n")

if __name__ == "__main__":
    generate_events()
