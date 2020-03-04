# Getting Survey Responses via the New Export APIs Sample Code
#***********TODO: Figure out how to access information without needing to download to JSON format
import requests
import zipfile
import json
import io, os
import sys

# Setting user Parameters
def get_survey():
    try:
        apiToken = os.getenv('Q_API_TOKEN')
    except KeyError:
        print("set environment variable APIKEY")
        sys.exit(2)

    surveyId = os.getenv('DDM_SURVEY')
    dataCenter = os.getenv('Q_DATA_CENTER')

    # Setting static parameters
    CheckProgress = 0.0
    progressStatus = "inProgress"
    url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(dataCenter, surveyId)
    headers = {
        "content-type": "application/json",
        "X-API-TOKEN": apiToken,
        }

    # Step 1: Creating Data Export
    data = {
            "format": "json"
            # "useLabels": "False"
           }

    downloadRequestResponse = requests.request("POST", url, json=data, headers=headers)
    print(downloadRequestResponse.json())

    try:
        progressId = downloadRequestResponse.json()["result"]["progressId"]
    except KeyError:
        print(downloadRequestResponse.json())
        sys.exit(2)

    isFile = None

    # Step 2: Checking on Data Export Progress and waiting until export is ready
    while progressStatus != "complete" and progressStatus != "failed" and isFile is None:
        if isFile is None:
           print  ("file not ready")
        else:
           print ("progressStatus=", progressStatus)
        requestCheckUrl = url + progressId
        requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
        try:
           isFile = requestCheckResponse.json()["result"]["fileId"]
        except KeyError:
           1==1
        print(requestCheckResponse.json())
        requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
        print("Download is " + str(requestCheckProgress) + " complete")
        progressStatus = requestCheckResponse.json()["result"]["status"]

    #step 2.1: Check for error
    if progressStatus is "failed":
        raise Exception("export failed")

    fileId = requestCheckResponse.json()["result"]["fileId"]

    # Step 3: Downloading file
    requestDownloadUrl = url + fileId + '/file'
    requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

    # Step 4: Unzipping the file
    zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall("../MyFilesQuatrics")
    print('Complete')

    # Open, read, filter the fileId
    # how to condense so the file doesn't need to be extracted then read --> direct to python3
    # def findPID():
    #     with open('Daily Diary Morning.json') as fp:
    #         data = json.load(fp)
    #     for pid in data:
    #         print user['responses']['values']['recipientFirstName']

    # def progressCheck(pid, date, surveyID): #participant id

def findPID(identifier):
# TODO: Implement parameter that checks different Survey API based on day of week
# Function:
    # Input is an participant id that is compared against survey data from Qualtrics
# identifier should probably be an array so multiple numbers can be passed in...maybe not
    # Access json file pulled from Qualtrics... simplify so it's not a download but rather tempfile??
    with open('../MyFilesQuatrics/Daily Diary Morning.json') as fp:
        data = json.load(fp)
    for r in data['responses']:
        if 'PIN' in r['values']:
            if(identifier == r['values']['PIN']):
                print("True " + r['responseId'])
        else:
            print("welp " + r['responseId'])

def removeFile(fileName):
    # default file name will be /MyFilesQuatrics/Daily Diary Morning/Afternoon
    os.remove('../MyFilesQuatrics/' + fileName)
    print(fileName)

if __name__ == '__main__':
    get_survey()
    # findPID("888")
    # removeFile("test.json") # "Daily Diary Morning/Afternoon"
