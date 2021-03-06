#!/usr/bin/python3.4
import time
import oauthUP
from rest import REST
import json

class Organization(object):

    def __init__(self):
        self.my_session = REST('my_session')
        access_token = oauthUP.login(
            env='tca',
            username='joeWilsonAdmin@tcaPerformanceTesting.com',
            password='Test1234!',
            encoded_client='YzA1YjNjN2YtMmU4NC00ZjhhLWJmYzEtNzU5YjJlNzBmMGM2OjlEczZaaV82eWJ5UzcyclNsQmpCSGt5QV9jdGVRcjNuZS0wcXBOakVENkk=',
            rest_session=self.my_session
        )
        self.headers = {"Authorization": "bearer " + access_token,'content-type': 'application/json'}

    def get_all_phones(self):
        pageNumber = 1
        allPhones = []
        while True:
            time.sleep(10)
            try:
                phones = self.get_phones(pageNumber)
                phones = json.loads(phones.text)
                if 'entities' in phones:
                    allPhones = allPhones + phones['entities']
                    print("Got page " +  str(pageNumber) + " of phones")
                    pageNumber =  pageNumber + 1
                if pageNumber > phones['pageCount']:
                    print("Got all phones")
                    self.delete_phones(allPhones)
                    break
            except Exception as exception_details:
                print(str(exception_details))
                
    def get_phones(self, pageNumber):
        url = "https://api.inintca.com/"
        url += "api/v2/telephony/providers/edges/phones?pageNumber={0}&pageSize=100".format(pageNumber)
        response = None
        try:
            response = self.my_session.get(url, self.headers)
        except Exception as exception_details:
            print(str(exception_details))

        return response

    def delete_phones(self, phones):
        print("Deleting " + str(len(phones)) + " phones")
        for index in range(0, len(phones)):
            time.sleep(1)
            url = "https://api.inintca.com/"
            url += "api/v2/telephony/providers/edges/phones/{0}".format(phones[index]['id'])
            response = None
            try:
                response = self.my_session.delete(url, self.headers)
            except Exception as exception_details:
                print(str(exception_details))

        return response