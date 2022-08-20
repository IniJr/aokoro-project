
from flask import Flask, json
import requests
from fetch_and_classify import fetch_and_classify
from datetime import datetime
import sys

headers = {"Content-Type": "application/json", "Authorization": "Token ee778e60b355d4408e72e61e1ca53fda7661bc76"}

def send_sms_reminder(record):
    url = 'https://www.bulksmsnigeria.com/api/v2/sms/create'
    params = {
      'api_token': '21JeCq7hBBFQ1RONcvTSZ3fc0v2xf7qX6G1qIxNLwT6dic19Qonpq38ad8wr',
      'to': record[0],
      'from': 'CHAMPS',
      'body': record[1],
      'gateway': '0',
      'append_sender': '0',
    }
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    response = requests.request('POST', url, headers=headers, params=params)
    return response.json()

def package_message(record):
    file = open('/home/aokoro/flask-apis/aokoro-project/messages.json')
    message = json.load(file)
    first_name = record[0]["first_name"]
    edd = record[0]["edd"]
    reveal_edd = str(" Remember that your EDD is "+str(edd.strftime("%d/%m/%Y"))+".") if edd is not 0 else ""
    prefix = "Dear Mrs "+record[0]["first_name"]
    if record[1] == "anc reminder":
        next_anc_visit = record[0]["next_anc_visit"]
        facility = ""
        text = prefix.strip()+message[record[1]]+next_anc_visit+facility
    else:
        text = prefix.strip()+message[record[1]]+reveal_edd
    suffix = " CHAMPS"
    return text+suffix


api = Flask(__name__)

@api.route('/facilities', methods=['GET'])
def get_facilities():
    data = requests.get("https://kf.kobotoolbox.org/api/v2/assets/aSwAuVXu9fckCrQh9fNgW5/data.json", headers=headers)
    facilities = data.json()
    return json.dumps(facilities)

@api.route('/facilities/count', methods=['GET'])
def get_count():
    data = requests.get("https://kf.kobotoolbox.org/api/v2/assets/aSwAuVXu9fckCrQh9fNgW5/data.json", headers=headers)
    facilities = data.json()
    return str(facilities["count"]+5)


@api.route('/facilities/filtered', methods=['GET'])
def get_filtered():
    data = requests.get("https://kf.kobotoolbox.org/api/v2/assets/aSwAuVXu9fckCrQh9fNgW5/data.json", headers=headers)
    facilities = data.json()
    filtered = []
    for each in facilities["results"]:
        item = {"id": each["PW_card_no"], "age": each["P_age"], "marital_status": each["Marital_status"], "village": each[""], "health_facility": each["Health_Facility_ID"], "distance": each[""], "visit_status": each[""], anc_status: each[""], "i0": each[""], "i1": each[""], "i2": each[""]}
        filtered.append(item)
    return str("")

@api.route('/prototype/registered-pregnant-women', methods=['GET'])
def get_registered_pregnant_women():
    complete_data = []
    #PW ID	Age at first ANC registration	Marital Status	Village	Health Facility	Distance to Health Facility (Km)	Next visit Date	Next visit status	Nex Visit date 2	Recent Visit status	pending visit date	ANC Status	immunization (at birth)	immunization (at six weeks)	immunization (at ten weeks)
    data = requests.get("https://kf.kobotoolbox.org/api/v2/assets/aSwAuVXu9fckCrQh9fNgW5/data.json", headers=headers)
    facilities = data.json()
    for facility in facilities:
        pw_id = ''
        age_at_first_registration = ''
        marital_status = ''
        village = ''
        health_facility = ''
        distance_to_health_facility = ''
        next_visit_date = ''
        next_visit_status = ''
        anc_status = ''
        immunization_at_birth_status = False 
        immunization_at_six_weeks = False
        immunization_at_ten_weeks = False
        row = {
            'pw_id': pw_id,
            'age_at_first_registration': age_at_first_registration,
            'marital_status': marital_status,
            'village': village,
            'health_facility': health_facility,
            'distance_to_health_facility': distance_to_health_facility,
            'next_visit_date': next_visit_date,
            'next_visit_status': next_visit_status,
            'anc_status': anc_status,
            'immunization_at_birth_status': immunization_at_birth_status,
            'immunization_at_six_weeks': immunization_at_six_weeks,
            'immunization_at_ten_weeks': immunization_at_ten_weeks
        }
        complete_data.append(row)
    return json.dumps(complete_data)

@api.route('/notifications/sms/send-reminder-all', methods=['GET'])
def get_reminder_all():
    print(datetime.now()," | Sending reminders to all", file=sys.stderr)
    classifier = fetch_and_classify()
    classified_data = classifier.classify_data("all")
    sms_stream = []
    response_stream = []
    for each in classified_data:
        sms_stream.append([each[0]["phone_number"], package_message(each)])
    for each in sms_stream:
        response_stream.append(send_sms_reminder(each))
    print(datetime.now()," | SMS Stream: ", sms_stream, file=sys.stderr)
    print(datetime.now()," | Response Stream: ", response_stream, file=sys.stderr)
    return json.dumps(response_stream)

@api.route('/notifications/sms/send-reminder-first-visit', methods=['GET'])
def get_reminder_first_visit():
    print(datetime.now()," | Sending reminders to first visits", file=sys.stderr)
    classifier = fetch_and_classify()
    classified_data = classifier.classify_data("first_visit")
    sms_stream = []
    response_stream = []
    for each in classified_data:
        sms_stream.append([each[0]["phone_number"], package_message(each)])
    for each in sms_stream:
        response_stream.append(send_sms_reminder(each))
    print(datetime.now()," | SMS Stream: ", sms_stream, file=sys.stderr)
    print(datetime.now()," | Response Stream: ", response_stream, file=sys.stderr)
    return json.dumps(response_stream)

@api.route('/notifications/sms/send-reminder-second-month', methods=['GET'])
def get_reminder_second_month():
    print(datetime.now()," | Sending reminders to pregnant women in their second month", file=sys.stderr)
    classifier = fetch_and_classify()
    classified_data = classifier.classify_data("second_month")
    sms_stream = []
    response_stream = []
    for each in classified_data:
        sms_stream.append([each[0]["phone_number"], package_message(each)])
    for each in sms_stream:
        response_stream.append(send_sms_reminder(each))
    print(datetime.now()," | SMS Stream: ", sms_stream, file=sys.stderr)
    print(datetime.now()," | Response Stream: ", response_stream, file=sys.stderr)
    return json.dumps(response_stream)

@api.route('/notifications/sms/send-reminder-third-month', methods=['GET'])
def get_reminder_third_month():
    print(datetime.now()," | Sending reminders to pregnant women in their third month", file=sys.stderr)
    classifier = fetch_and_classify()
    classified_data = classifier.classify_data("third_month")
    sms_stream = []
    response_stream = []
    for each in classified_data:
        sms_stream.append([each[0]["phone_number"], package_message(each)])
    for each in sms_stream:
        response_stream.append(send_sms_reminder(each))
    print(datetime.now()," | SMS Stream: ", sms_stream, file=sys.stderr)
    print(datetime.now()," | Response Stream: ", response_stream, file=sys.stderr)
    return json.dumps(response_stream)

@api.route('/notifications/sms/send-reminder-sixth-month', methods=['GET'])
def get_reminder_sixth_month():
    print(datetime.now()," | Sending reminders to pregnant women in their sixth month", file=sys.stderr)
    classifier = fetch_and_classify()
    classified_data = classifier.classify_data("sixth_month")
    sms_stream = []
    response_stream = []
    for each in classified_data:
        sms_stream.append([each[0]["phone_number"], package_message(each)])
    for each in sms_stream:
        response_stream.append(send_sms_reminder(each))
    print(datetime.now()," | SMS Stream: ", sms_stream, file=sys.stderr)
    print(datetime.now()," | Response Stream: ", response_stream, file=sys.stderr)
    return json.dumps(response_stream)

@api.route('/notifications/sms/send-reminder-seventh-month', methods=['GET'])
def get_reminder_seventh_month():
    print(datetime.now()," | Sending reminders to pregnant women in their seventh month", file=sys.stderr)
    classifier = fetch_and_classify()
    classified_data = classifier.classify_data("seventh_month")
    sms_stream = []
    response_stream = []
    for each in classified_data:
        sms_stream.append([each[0]["phone_number"], package_message(each)])
    for each in sms_stream:
        response_stream.append(send_sms_reminder(each))
    print(datetime.now()," | SMS Stream: ", sms_stream, file=sys.stderr)
    print(datetime.now()," | Response Stream: ", response_stream, file=sys.stderr)
    return json.dumps(response_stream)

@api.route('/notifications/sms/send-reminder-ninth-month', methods=['GET'])
def get_reminder_ninth_month():
    print(datetime.now()," | Sending reminders to pregnant women in their ninth month", file=sys.stderr)
    classifier = fetch_and_classify()
    classified_data = classifier.classify_data("ninth_month")
    sms_stream = []
    response_stream = []
    for each in classified_data:
        sms_stream.append([each[0]["phone_number"], package_message(each)])
    for each in sms_stream:
        response_stream.append(send_sms_reminder(each))
    print(datetime.now()," | SMS Stream: ", sms_stream, file=sys.stderr)
    print(datetime.now()," | Response Stream: ", response_stream, file=sys.stderr)
    return json.dumps(response_stream)

@api.route('/notifications/sms/send-reminder-immunization-second-week', methods=['GET'])
def get_reminder_second_week():
    print(datetime.now()," | Sending reminders to mothers in their second week", file=sys.stderr)
    classifier = fetch_and_classify()
    classified_data = classifier.classify_data("second_week")
    sms_stream = []
    response_stream = []
    for each in classified_data:
        sms_stream.append([each[0]["phone_number"], package_message(each)])
    for each in sms_stream:
        response_stream.append(send_sms_reminder(each))
    print(datetime.now()," | SMS Stream: ", sms_stream, file=sys.stderr)
    print(datetime.now()," | Response Stream: ", response_stream, file=sys.stderr)
    return json.dumps(response_stream)

@api.route('/notifications/sms/send-reminder-immunization-fourth-week', methods=['GET'])
def get_reminder_fourth_week():
    print(datetime.now()," | Sending reminders to mothers in their fourth week", file=sys.stderr)
    classifier = fetch_and_classify()
    classified_data = classifier.classify_data("fourth_week")
    sms_stream = []
    response_stream = []
    for each in classified_data:
        sms_stream.append([each[0]["phone_number"], package_message(each)])
    for each in sms_stream:
        response_stream.append(send_sms_reminder(each))
    print(datetime.now()," | SMS Stream: ", sms_stream, file=sys.stderr)
    print(datetime.now()," | Response Stream: ", response_stream, file=sys.stderr)
    return json.dumps(response_stream)

@api.route('/notifications/sms/send-reminder-anc', methods=['GET'])
def get_reminder_anc():
    print(datetime.now()," | Sending reminders anc reminders", file=sys.stderr)
    classifier = fetch_and_classify()
    classified_data = classifier.classify_data("anc")
    sms_stream = []
    response_stream = []
    for each in classified_data:
        sms_stream.append([each[0]["phone_number"], package_message(each)])
    for each in sms_stream:
        response_stream.append(send_sms_reminder(each))
    print(datetime.now()," | SMS Stream: ", sms_stream, file=sys.stderr)
    print(datetime.now()," | Response Stream: ", response_stream, file=sys.stderr)
    return json.dumps(response_stream)

if __name__ == '__main__':
    from waitress import serve
    serve(api, host="0.0.0.0", port=5000)
    # api.run() 
