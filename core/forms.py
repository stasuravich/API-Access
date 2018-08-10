from django import forms
from django.conf import settings
import requests

class DictionaryForm(forms.Form):
    country = forms.CharField(max_length=5)
    number= forms.CharField(max_length=20)
    def search(self):
        result = {}
        country = self.cleaned_data['country']
        number = self.cleaned_data['number']
        headers = {
            'accept': 'application/json',
            'user_key': 'b1ca07c44d418457d02b85416ae33783',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        base_url = 'https://api.brex.io/'
        post = lambda url, json_data=None: requests.post(base_url+url, headers=headers, json=json_data)
        get = lambda url: requests.get(base_url+url, headers=headers)
        response_1= get('api/v1/company/search/number/'+ country + '/' + number)    #navigate api to get id
        if response_1.json() != []:                                                 #if result exists,
            id=response_1.json()[0]['id']                                           #get the id
            name=response_1.json()[0]['name']                                       #get the name
            response_2= get('api/v1/company/'+ id + '/super/' + country)            #navigate to get other information
            if response_2.status_code == 200:  # SUCCESS
                result = response_2.json()
                result['success'] = True
            else:
                result['success'] = False
                if response_2.status_code == 404:  # NOT FOUND
                    result['message'] = 'No entry found for "%s"' % country
                else:
                    result['message'] = 'The result is not available at the moment. Please try again later.'
        else:
            result['success']=False
            if response_1.status_code == 404:  # NOT FOUND
                result['message'] = 'No entry found for "%s"' % country
            else:
                result['message'] = 'The result is not available at the moment. Please try again later.'
        return result
