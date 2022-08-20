
from fetch_and_classify import fetch_and_classify
import requests
import json

def package_message(record):
    file = open('messages.json')
    message = json.load(file)
    first_name = record[0]["first_name"]
    edd = record[0]["edd"]
    reveal_edd = " Remember that your EDD is "+edd.strftime("%d/%m/%Y")+"." if edd is not 0 else ""
    prefix = "Dear Mrs "+record[0]["first_name"]
    if record[1] == "anc reminder":
        next_anc_visit = record[0]["next_anc_visit"]
        facility = ""
        text = prefix.strip()+message[record[1]]+next_anc_visit+facility
    else:
        text = prefix.strip()+message[record[1]]+reveal_edd
    suffix = " CHAMPS"
    return text+suffix

    
classifier = fetch_and_classify()
classified_data = classifier.classify_data()
sms_stream = []
for each in classified_data:
    sms_stream.append([each[0]["phone_number"], package_message(each)])

for each in sms_stream:
    print(send_sms_reminder(each))
    print(each)
print(classifier.group_data())



    