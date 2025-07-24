import uuid
import random
from datetime import datetime, timedelta
import pandas as pd

def generate_filemaliciouscontentinfo(num_noise=500, num_malicious=5, base_time_str="2025-10-01T09:00:00Z"):
    base_time = datetime.strptime(base_time_str, "%Y-%m-%dT%H:%M:%SZ")
    noise_time_range = (base_time - timedelta(days=3), base_time + timedelta(days=3))
    malicious_offsets = [0, 2, 4, 6, 6.166]  # hours after base_time

    def random_datetime(start, end):
        return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

    def random_filesize():
        return random.randint(10 * 1024, 100 * 1024 * 1024)

    def random_filename(extension=".docx"):
        names = ["report", "invoice", "timesheet", "data", "summary", "presentation", "log", "scan"]
        return f"{random.choice(names)}_{random.randint(100,999)}{extension}"

    def generate_file_entry(is_malicious=False, offset_hours=None):
        if is_malicious and offset_hours is not None:
            creation_time = base_time + timedelta(hours=offset_hours)
        else:
            creation_time = random_datetime(*noise_time_range)

        file_size = random_filesize()
        folder = random.choice([
            "C:\\Users\\admin\\Documents",
            "C:\\Users\\admin\\Downloads",
            "C:\\Users\\admin\\Desktop",
            "C:\\Users\\admin\\AppData\\Local\\Temp"
        ])
        filename = random_filename(".exe" if is_malicious else random.choice([".docx", ".xlsx", ".pdf", ".exe", ".txt"]))

        if is_malicious:
            detection = random.choice(["CloudML", "Signature", "Heuristic"])
        else:
            detection = random.choice(["None", "Unknown", "Clean", "Heuristic", "CloudML"])

        return {
            "_BilledSize": round(random.uniform(1.5, 5.0), 2),
            "DetectionMethods": detection,
            "DocumentID": str(uuid.uuid4()),
            "FileCreationTime": creation_time.isoformat(),
            "FileName": filename,
            "FileOwnerDisplayName": "Matt Larkin",
            "FileOwnerUpn": "matt.larkin@contoso.com",
            "FileSize": file_size,
            "FolderPath": folder,
            "_IsBillable": "true",
            "LastUpdateTime": (creation_time + timedelta(minutes=random.randint(0, 30))).isoformat()
        }

    noise_entries = [generate_file_entry() for _ in range(num_noise)]
    malicious_entries = [generate_file_entry(is_malicious=True, offset_hours=offset) for offset in malicious_offsets[:num_malicious]]
    all_entries = noise_entries + malicious_entries
    df = pd.DataFrame(all_entries)
    return df

# Main block
if __name__ == "__main__":
    output_path = "FileMaliciousContentInfo.json"
    df = generate_filemaliciouscontentinfo()
    df.to_json(output_path, orient="records", lines=True)
    print(f"✅ File saved as: {output_path}")
