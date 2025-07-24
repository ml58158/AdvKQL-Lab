import os, json, random
from datetime import datetime, timedelta
from faker import Faker
from collections import OrderedDict

output_dir = "C:\\Output"
os.makedirs(output_dir, exist_ok=True)
fake = Faker()

def generate_event(ts):
    record = OrderedDict()
    # Generate realistic AccountUpn based on attack story
    if random.random() < 0.85:
        domain = "kustoindustries.net"
    else:
        domain = random.choice(["phishme.com", "malspam.net", "evilcorp.biz"])
    record["AccountUpn"] = f"{fake.user_name()}@{domain}"

    record["_BilledSize"] = random.randint(1000, 10000)
    record["_IsBillable"] = "True"
    
    record["ActionType"] = random.choice(["Allowed", "Blocked"])
    record["DetectionMethods"] = random.choice(["Heuristic", "MachineLearning"])
    record["IPAddress"] = fake.ipv4_public()
    record["IsClickedThrough"] = random.choice([True, False])
    record["NetworkMessageId"] = f"<356d3ba7-8851-42c4-9846-5126e0ea980a@example.com>"
    record["ReportId"] = str(fake.uuid4())
    record["SourceSystem"] = ""
    record["TenantId"] = "d63f3f4b-6e5b-4e10-a8b8-2d7e2a8b5f72"
    record["ThreatTypes"] = random.choice(["Phish", "Malware", "Spam"])
    record["TimeGenerated"] = ts.isoformat()
    record["Timestamp"] = ts.isoformat()
    record["Type"] = "UrlClickEvents"

    record["AdditionalFields"] = json.dumps({
        "campaign": "TANGOFOX_Ransom",
        "attackStage": "Clickthrough",
        "originalEmailSubject": "Urgent Invoice Request",
        "phishingPage": "http://evilcorp.biz/login"
    })

    record["Url"] = fake.uri()
    record["UrlChain"] = json.dumps([fake.uri(), fake.uri()])
    record["Workload"] = random.choice(["Email", "Office", "Teams"])
    return record

def generate_events(count=100):
    base = datetime.utcnow()
    delta = timedelta(minutes=2)
    with open(os.path.join(output_dir, "url_click_events.json"), "w", encoding="utf-8") as f:
        for i in range(count):
            ts = base - i * delta
            f.write(json.dumps(generate_event(ts)) + "\n")

if __name__ == "__main__":
    generate_events()
