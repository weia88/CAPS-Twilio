# TODO: Implement parameter that checks different Survey API based on day of week
import json

# Function:
    # Input is an participant id that is compared against survey data from Qualtrics
# identifier should probably be an array so multiple numbers can be passed in...maybe not
def findPID(identifier, ):

    # Access json file pulled from Qualtrics... simplify so it's not a download but rather tempfile??
    with open('MyQualtricsDownload/Daily Diary Morning.json') as fp:
        data = json.load(fp)
    for pid in data['responses']:
        # print(pid.keys())
        # print(pid['values'])
        if 'recipientFirstName' in pid['values']:
            if(identifier == pid['values']['recipientFirstName']):
                print("True " + pid['responseId'])
                #return True #Return true to enter if loop
        else:
            print("welp " + pid['responseId'])
        # print(pid['values']['recipientFirstName'])

if __name__ == '__main__':
    findPID("888")
