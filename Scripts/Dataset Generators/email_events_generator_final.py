import os
import json
import random
from collections import OrderedDict
from datetime import datetime, timedelta
from faker import Faker

# ------------------------
# Configuration
# ------------------------
output_dir = "C:\\Output"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "email_events.json")

fake = Faker()
TENANT_ID = "d63f3f4b-6e5b-4e10-a8b8-2d7e2a8b5f72"
DOMAIN = "kustoindustries.com"

EMAIL_SUBJECTS = [
    "Re: Invoice #548712 Overdue",
    "Important: Security Update Required",
    "Action Required: Unusual Sign-In Attempt",
    "You Have a New Voicemail",
    "Suspicious Activity Detected on Your Account",
    "Delivery Notification: Package Exception",
    "Office365 Admin Alert: Pending Suspension",
    "Shared Document: Review Requested"
    "New Message from HR: Policy Update",
    "Your Subscription is About to Expire",
    "Urgent: Account Verification Needed",
    "Reminder: Upcoming Meeting",
    "New Login from Unknown Device",
    "Congratulations! You've Won a Gift Card",
    "Your Account Has Been Compromised",
    "Security Alert: Password Change Required",
    "New Login Alert: Verify Your Identity",
    "Action Needed: Update Your Payment Information",
    "Your Invoice is Ready for Review",
    "Important: System Maintenance Scheduled",
    "New Feature Announcement: Check It Out",
    "Your Feedback is Needed: Survey Inside",
    "Reminder: Password Expiration Notice",
    "New Policy Update: Please Read",
    "Your Account Has Been Locked",
    "Important: Data Breach Notification",
    "Action Required: Confirm Your Email Address",
    "New Document Shared with You",
    "Your Account Settings Have Been Updated",
    "Security Alert: Unusual Login Activity",
    "New Message from IT Support: Action Required",
    "Your Subscription Renewal Confirmation"
]

THREAT_TYPE = "Phishing"
THREAT_NAME = "WannaCry Initial Lure"

def generate_email_event(i, start_time, delta):
    event_time = start_time + (i * delta)
    record = OrderedDict()

    record["TenantId"] = TENANT_ID
    record["AttachmentCount"] = random.randint(0, 2)
    record["AuthenticationDetails"] = {"DKIM": "none", "DMARC": "none"}
    record["AdditionalFields"] = {"PhishScore": str(random.randint(85, 99))}
    record["ConfidenceLevel"] = random.randint(80, 100)
    record["Connectors"] = "Exchange Online"
    record["DetectionMethods"] = "Heuristic,MachineLearning"
    record["DeliveryAction"] = "Delivered"
    record["DeliveryLocation"] = random.choice(["Inbox", "Junk"])
    record["EmailDirection"] = "Inbound"
    record["EmailLanguage"] = "en"
    record["EmailAction"] = "Delivered"
    record["EmailActionPolicy"] = "DefaultPolicy"
    record["EmailActionPolicyGuid"] = fake.uuid4()
    record["OrgLevelAction"] = "Notify"
    record["OrgLevelPolicy"] = "OrgPolicy1"
    record["InternetMessageId"] = f"<{fake.uuid4()}@{DOMAIN}>"
    record["NetworkMessageId"] = f"<{fake.uuid4()}@{DOMAIN}>"
    record["RecipientEmailAddress"] = fake.user_name() + "@" + DOMAIN
    record["RecipientObjectId"] = fake.uuid4()
    record["ReportId"] = fake.uuid4()
    record["SenderDisplayName"] = fake.name()
    record["FromEmail"] = fake.user_name() + "@evilcorp.biz"
    record["FromDomain"] = "evilcorp.biz"
    record["SenderObjectId"] = fake.uuid4()
    record["SenderIPv4"] = fake.ipv4_private()
    record["SenderIPv6"] = fake.ipv6()
    record["SenderMailFromAddress"] = "alerts@evilcorp.biz"
    record["SenderMailFromDomain"] = "evilcorp.biz"
    record["EmailSubject"] = random.choice(EMAIL_SUBJECTS)
    record["ThreatTypes"] = THREAT_TYPE
    record["ThreatNames"] = THREAT_NAME
    record["TimeGenerated"] = datetime.utcnow().isoformat()
    record["Timestamp"] = event_time.isoformat()
    record["UrlCount"] = random.randint(1, 3)
    record["UserLevelAction"] = "Clicked"
    record["UserLevelPolicy"] = "Policy1"
    record["BulkComplaintLevel"] = "High"
    record["LatestDeliveryLocation"] = record["DeliveryLocation"]
    record["LatestDeliveryAction"] = record["DeliveryAction"]
    record["SourceSystem"] = ""
    record["Type"] = "EmailEvent"
    record["EmailClusterId"] = fake.uuid4()

    
    record["AdditionalFields"] = json.dumps({
        "PhishScore": "95",
        "campaign": "TANGOFOX_Ransom",
        "stage": "Initial Access",
        "deliveryMethod": "EmailLink",
        "maliciousUrl": "http://evilcorp.biz/download/invoice.html"
    })

    return record

def generate_events(days, events_per_day=1000):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    total_events = days * events_per_day
    delta = timedelta(seconds=((end_time - start_time).total_seconds() / total_events))

    with open(output_file, "w", encoding="utf-8") as f:
        for i in range(total_events):
            f.write(json.dumps(generate_email_event(i, start_time, delta)) + "\n")

    print(f"✅ Generated {total_events} phishing email events in '{output_file}'")

if __name__ == "__main__":
    generate_events(days=1)
