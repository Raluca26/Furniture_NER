import csv
import requests

csv_file_path = './pages.csv'

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    nr_200 = 0
    for index, row in enumerate(csv_reader):
        if index >= 100:
            break  

        url = row[0]  
        try:
            response = requests.get(url)
            status_code = response.status_code
            print(f"URL: {url}, Status Code: {status_code}")
            if status_code == 200:
                nr_200 +=1   # to check total number of urls with response ==200
            else:
                pass
        except requests.exceptions.RequestException as e:
            print(f"URL: {url}, Error: {e}")
    print(nr_200)  
