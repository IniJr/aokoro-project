import requests
from contextlib import suppress
import datetime
from dateutil.relativedelta import relativedelta

class fetch_and_classify:
    def __init__(self):
        headers = {"Content-Type": "application/json", "Authorization": "Token ee778e60b355d4408e72e61e1ca53fda7661bc76"}
        response = requests.get('https://kf.kobotoolbox.org/api/v2/assets/aUaMWgTyxmZoWM947C7sQg/data.json',headers=headers)
        result = response.json()
        self.appointment_info = result["results"]
        self.data_classifier = []
                    
    # def group_data(self):
    #     grouped_data = []
    #     facility_gps = "4.9499962 8.32166538"
    #     with suppress(KeyError):
    #         for each in self.expectant:
    #             for facility in self.facility:
    #                 if each["selected_HF"] == facility["Name_of_Facility"]:
    #                     facility_gps = facility["GPS_Coordinate"]
    #             grouped_data.append({"pw_card_no": each["PW_card_no"], "gps_pw_home": each["GPS_PW_Home"], "gps_health_facility": facility_gps })
    #     return grouped_data
        
    def classify_data(self, period):
        for each in self.appointment_info:
            with suppress(KeyError):
                date_format = '%Y-%m-%d'
                dtObj = datetime.datetime.strptime(str(datetime.date.today()), date_format)
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                current_time = datetime.datetime.utcnow()
                try:
                    lmp = datetime.datetime.strptime(each["LMP"], date_format)
                except:
                    lmp = 0
                try:
                    edd = datetime.datetime.strptime(each["EDD"], date_format)
                except:
                    edd = 0
                try:
                    next_anc_date = datetime.datetime.strptime(each["next_ANC_date"], date_format)
                    two_months_away = next_anc_date + relativedelta(months=2)
                    three_months_away = next_anc_date + relativedelta(months=3)
                    six_months_away = next_anc_date + relativedelta(months=6)
                    seven_months_away = next_anc_date + relativedelta(months=7)
                    eight_months_away = next_anc_date + relativedelta(months=8)
                    nine_months_away = next_anc_date + relativedelta(months=9)
                except:
                    next_anc_date = 0
                    two_months_away = 0
                    three_months_away = 0
                    six_months_away = 0
                    seven_months_away = 0
                    eight_months_away = 0
                    nine_months_away = 0
                try:
                    end_of_pregnancy_date = datetime.datetime.strptime(each["end_of_pregnancy_date"], date_format) 
                    two_weeks_away = end_of_pregnancy_date + relativedelta(weeks=2)
                    four_weeks_away = end_of_pregnancy_date + relativedelta(months=1)
                except:
                    end_of_pregnancy_date = 0
                    two_weeks_away = 0
                    four_weeks_away = 0
                try:
                    pregnancy_outcome = each["Pregnancy_outcome"]
                except:
                    pregnancy_outcome = 0
                first_name = each["P_Fname"]
                phone_number = each["P_phone_number"]

                if(period == 'all'):
                    self.data_classifier.append([{"first_name": first_name, "phone_number": phone_number, "edd": edd}, "second month"])
                elif(period == 'two_months_away'): 
                    if(tomorrow == two_months_away):
                        self.data_classifier.append([{"first_name": first_name, "phone_number": phone_number, "edd": edd}, "second month"])
                elif(period == 'three_months_away'):
                    if (tomorrow == three_months_away):
                        self.data_classifier.append([{"first_name": first_name, "phone_number": phone_number, "edd": edd}, "third month"])
                elif(period == 'six_months_away'):
                    if(tomorrow == six_months_away):
                        self.data_classifier.append([{"first_name": first_name, "phone_number": phone_number, "edd": edd}, "sixth month"])
                elif(period == 'seven_months_away'):
                    if(tomorrow == seven_months_away):
                        self.data_classifier.append([{"first_name": first_name, "phone_number": phone_number, "edd": edd}, "seventh month"])
                elif(period == 'six_months_away'):
                    if(tomorrow == eight_months_away):
                        self.data_classifier.append([{"first_name": first_name, "phone_number": phone_number, "edd": edd}, "eighth month"])
                elif(period == 'nine_months_away'):
                    if(tomorrow == nine_months_away):
                        self.data_classifier.append([{"first_name": first_name, "phone_number": phone_number, "edd": edd}, "ninth month"])
                elif(period == 'two_weeks_away'):
                    if(tomorrow == two_weeks_away):
                        self.data_classifier.append([{"first_name": first_name, "phone_number": phone_number, "edd": edd, "end_of_pregnancy_date": end_of_pregnancy_date, "pregnancy_outcome": pregnancy_outcome}, "second week"])
                elif(period == 'four_weeks_away'):
                    if(tomorrow == four_weeks_away):
                        self.data_classifier.append([{"first_name": first_name, "phone_number": phone_number, "edd": edd, "end_of_pregnancy_date": end_of_pregnancy_date, "pregnancy_outcome": pregnancy_outcome}, "fourth week"])
                elif(period == 'first_visit'):
                    if(lmp == datetime.date.today()):
                        self.data_classifier.append([{"first_name": first_name, "phone_number": phone_number, "edd": edd, "next_anc_date": next_anc_date}, "first visit"])
                elif(period == 'anc'):
                    if(tomorrow == next_anc_date):
                        self.data_classifier.append([{"first_name": first_name, "phone_number": phone_number, "edd": edd, "next_anc_date": next_anc_date}, "anc reminder"])
                    elif(datetime.date.today() == next_anc_date and current_time.hour < 8):
                        self.data_classifier.append([{"first_name": first_name, "phone_number": phone_number, "edd": edd, "next_anc_date": next_anc_date}, "anc reminder"])
                else:
                    pass
                    # self.data_classifier.append([{"first_name": first_name, "phone_number": phone_number, "edd": edd, "next_anc_date": next_anc_date, "end_of_pregnancy_date": end_of_pregnancy_date, "pregnancy_outcome": pregnancy_outcome}, "no class"])
        return self.data_classifier