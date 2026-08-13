import requests
import csv
import io

response = requests.get("http://127.0.0.1:8000/api/events/")
print(response)
print(response.json())

data = response.json()

virt_file = io.StringIO()
fieldnames = ['id', 'time', 'distance', 'direction']
writer = csv.DictWriter(virt_file, fieldnames=fieldnames)

writer.writeheader()
writer.writerows(data)

csv_text = virt_file.getvalue()
print(csv_text)