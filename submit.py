import csv
import json
import requests
import sys
from validate import explain_result

headers = {'content-type': 'application/json'}


def send_json_to_score_server(corrected_file):
    url = 'http://0.0.0.0:5005'
    data = list(csv.DictReader(open(corrected_file, 'rU')))
    response = requests.post(url, data=json.dumps(data), headers=headers)
    # print "Status code: %s" % response.status_code
    if response.status_code == 200:
        result = response.json()
        explain_result(result)
        return result
    else:
        print 'Invalid'
        print response.text
        return None

if __name__ == "__main__":
    file_name = sys.argv[1]
    junk = send_json_to_score_server(file_name)
