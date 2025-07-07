import os, json, random
from datetime import datetime
from faker import Faker
from collections import OrderedDict

output_dir = "C:\\Output"
os.makedirs(output_dir, exist_ok=True)
fake = Faker()

def generate_event():
    record = OrderedDict()
    record["AadDeviceId"] = str(fake.uuid4())
    record["AdditionalFields"] = json.dumps({"info": "baseline scan"}, indent=None)
    record["AssetValue"] = random.choice(["Low", "Normal", "High"])
    record["AwsResourceName"] = ""
    record["AzureResourceId"] = ""
    record["AzureVmId"] = str(fake.uuid4())
    record["AzureVmSubscriptionId"] = str(fake.uuid4())
    record["ClientVersion"] = f"3.1"
    record["CloudPlatforms"] = "Azure"
    record["ConnectivityType"] = "Internet"
    record["DeviceCategory"] = "Endpoint"
    record["DeviceDynamicTags"] = "[\"tag1\", \"tag2\"]"
    record["DeviceId"] = str(fake.uuid4())
    record["DeviceManualTags"] = "[\"manualtag\"]"
    record["DeviceName"] = random.choice(["FN-WKSTN-001", "HR-LPT-001"])
    record["DeviceSubtype"] = "Laptop"
    record["DeviceType"] = "Workstation"
    record["ExclusionReason"] = ""
    record["ExposureLevel"] = random.choice(["Low", "Medium", "High"])
    record["GcpFullResourceName"] = ""
    record["HardwareUuid"] = str(fake.uuid4())
    record["HostDeviceId"] = ""
    record["IsAzureADJoined"] = True
    record["IsExcluded"] = False
    record["IsInternetFacing"] = True
    record["JoinType"] = "AzureAD"
    record["LoggedOnUsers"] = json.dumps([{"AccountName": fake.user_name()}])
    record["MachineGroup"] = "UnassignedGroup"
    record["MergedDeviceIds"] = ""
    record["MergedToDeviceId"] = ""
    record["MitigationStatus"] = "None"
    record["Model"] = "Dell XPS 13"
    record["OnboardingStatus"] = "Onboarded"
    record["OSArchitecture"] = "x64"
    record["OSBuild"] = 19045
    record["OSDistribution"] = "Windows"
    record["OSPlatform"] = "Windows10"
    record["OSVersion"] = "10.0.19045"
    record["OSVersionInfo"] = "Windows 10 Pro"
    record["PublicIP"] = fake.ipv4()
    record["RegistryDeviceTag"] = ""
    record["ReportId"] = random.randint(100000, 999999)
    record["SensorHealthState"] = "Active"
    record["SourceSystem"] = ""
    record["TenantId"] = "d63f3f4b-6e5b-4e10-a8b8-2d7e2a8b5f72"
    record["TimeGenerated"] = datetime.utcnow().isoformat()
    record["Timestamp"] = datetime.utcnow().isoformat()
    record["Type"] = "DeviceInfo"
    record["Vendor"] = "Dell Inc."
    return record

def generate_events(count=100):
    with open(os.path.join(output_dir, "device_info.json"), "w", encoding="utf-8") as f:
        for _ in range(count):
            f.write(json.dumps(generate_event()) + "\n")

if __name__ == "__main__":
    generate_events()
