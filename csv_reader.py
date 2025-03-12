import csv
import re
import subprocess

def extract_repo_name(output):
    matches = re.findall(r'command: \"\$\{PATH}/([^/]+)/run/script\.sh\"', output)
    return " ".join(matches) if matches else ""

def process_csv(file_path):
    updated_rows = []
    
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        rows = list(reader)
        
        for row in rows:
            if row['Summary']:
                try:
                    result = subprocess.run(row['Summary'], shell=True, capture_output=True, text=True)
                    repo_name = extract_repo_name(result.stdout)
                    row['Repo'] = repo_name
                except Exception as e:
                    print(f"Error processing command {row['Summary']}: {e}")
            updated_rows.append(row)
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

if __name__ == "__main__":
    process_csv("data.csv")
