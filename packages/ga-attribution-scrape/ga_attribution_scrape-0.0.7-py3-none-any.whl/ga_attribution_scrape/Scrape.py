
from google.auth.transport import requests
import requests
import pandas as pd
import io
from datetime import datetime, date as d, timedelta
import time


class Scrape:

    def __init__(self, configuration):
        self.configuration = configuration

    def goals(self, ga_management_data):
        request_url = self.configuration['ga_attribution_scrape']['request']['url']
        request_headers = self.configuration['ga_attribution_scrape']['request']['headers']
        form_data = self.configuration['ga_attribution_scrape']['request']['form_data']
        backdate = self.configuration['ga_attribution_scrape']['backdate']['backdate']

        # From configuration backdate or not. If not then get yesterday.
        if backdate:
            start_date = self.configuration['ga_attribution_scrape']['backdate']['start_date']
            end_date = self.configuration['ga_attribution_scrape']['backdate']['end_date']
            date_range = []
            for date in pd.date_range(start=start_date, end=end_date):
                date_range.append(date.strftime('%Y%m%d'))
        else:
            yesterday = d.today() - timedelta(days=1)
            date_range = [str(yesterday.strftime('%Y%m%d'))]

            # Loop through each day for each goal for DDA
        print('Getting attribution response for each day for each relevant goal ID')
        ga_attribution_data = pd.DataFrame()
        for date in date_range:
            for row in ga_management_data.id:

                # Filter goals to row goal - we'll use this to manipulate response and final data output
                conversion = ga_management_data[ga_management_data.id == row]

                # Add dates into form data for response
                form_data['_u.date00'] = date
                form_data['_u.date01'] = date

                # Add conversion ID into response
                conversion_id = conversion.id.to_list()[0]
                form_data['_.bfType'] = conversion_id

                # Get raw response data for GA
                raw_response = requests.post(request_url, data=form_data, headers=request_headers).text
                #print(raw_response)
                # Check for http error in response
                while 'The service is temporarily unavailable. Please try again in a few minutes.' in raw_response:
                    print("http error: The service is temporarily unavailable. Please try again in a few minutes.")
                    print("Sleeping for a couple of mins then retry")
                    time.sleep(120)
                    raw_response = requests.post(request_url, data=form_data, headers=request_headers).text

                #print(raw_response)
                time.sleep(1.5)

                # Clean response
                # Cleaning the actual response by removing the unnecessary lines and adding in other variables
                response = pd.read_csv(io.StringIO(raw_response), quotechar='"', skipinitialspace=True,
                                       error_bad_lines=False,
                                       skiprows=5)[:-3]

                # Renaming the columns
                new_column_names = []
                for item in response.columns:
                    x = item.replace(" ", "_")
                    x = x.replace("-", "_")
                    if x[0].isdigit():
                        x = "_" + x
                    new_column_names.append(x.lower())
                response.columns = new_column_names
                response = response[response.columns.drop(list(response.filter(regex='%_change_')))]

                # Change the types to float and removing all special characters
                for item in response.columns:
                    if 'spend' in item or 'data_driven' in item:
                        response[item] = response[item].replace({'£|€|$|>|<|,|\\%': ''}, regex=True)
                        response[item] = response[item].astype(float)

                # Make data into pandas dataframe
                clean_data = pd.DataFrame(response, columns=response.columns)

                # Add in the conversion name and id of goals
                clean_data['conversion_name'] = conversion.name.to_list() * len(clean_data.index)
                clean_data['conversion_id'] = conversion.id.to_list() * len(clean_data.index)

                # Add date into data
                clean_data["date"] = datetime.strptime(date, '%Y%m%d')

                ga_attribution_data = pd.concat([ga_attribution_data, clean_data])
                print(ga_attribution_data)

        return ga_attribution_data

    def ecommerce(self):
        request_url = self.configuration['ga_attribution_scrape']['request']['url']
        request_headers = self.configuration['ga_attribution_scrape']['request']['headers']
        form_data = self.configuration['ga_attribution_scrape']['request']['form_data']
