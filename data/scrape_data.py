import os
import requests
import json

EMAIL= "vnh8du@virginia.edu"
API_KEY = os.environ["AQS_API_KEY"]

def get_state_code(state_name):
    data = requests.get(f"https://aqs.epa.gov/data/api/list/states?email={EMAIL}&key={API_KEY}").json()['Data']
    for entry in data:
        if entry['value_represented'] == state_name:
            return entry['code']
    raise ValueError(f"Invalid state name: {state_name}")

def get_county_code(state_code, county_name):
    data = requests.get(f"https://aqs.epa.gov/data/api/list/countiesByState?email={EMAIL}&key={API_KEY}&state={state_code}").json()['Data']
    for entry in data:
        if entry['value_represented'] == county_name:
            return entry['code']
    raise ValueError(f"Invalid county name: {county_name}")

def get_site_codes(state_code, county_code):
    data = requests.get(f"https://aqs.epa.gov/data/api/list/sitesByCounty?email={EMAIL}&key={API_KEY}&state={state_code}&county={county_code}").json()
    return [entry['code'] for entry in data['Data']]

def get_all_parameter_codes():
    data = requests.get(f"https://aqs.epa.gov/data/api/list/parametersByClass?email={EMAIL}&key={API_KEY}&pc=ALL").json()
    return [entry['code'] for entry in data['Data']].join(",")

def get_aqi_parameter_codes():
    data = requests.get(f"https://aqs.epa.gov/data/api/list/parametersByClass?email={EMAIL}&key={API_KEY}&pc=AQI POLLUTANTS").json()
    return ",".join([entry['code'] for entry in data['Data']])

def get_site_data(state_code, county_code, site_code, bdate, edate, parameters):
    URL = f"https://aqs.epa.gov/data/api/sampleData/bySite?email={EMAIL}&key={API_KEY}&param={parameters}&bdate={bdate}&edate={edate}&state={state_code}&county={county_code}&site={site_code}"
    return requests.get(URL).json()['Data']

def get_aqi_data(state_code, county_code, site_code, bdate, edate):
    URL = f"https://aqs.epa.gov/data/api/dailyData/bySite?email={EMAIL}&key={API_KEY}&bdate={bdate}&edate={edate}&state={state_code}&county={county_code}&site={site_code}"
    return requests.get(URL).json()['Data']

def get_all_site_data(state_code, county_code, site_codes, bdate, edate, parameters):
    pass

def main():
    state_code = get_state_code("Virginia")
    county_code = get_county_code(state_code, "Albemarle")
    site_code = get_site_codes(state_code, county_code)[0]
    bdate = 20200101
    edate = 20201231
    parameters = get_aqi_parameter_codes()
    print(get_site_data(state_code, county_code, site_code, bdate, edate, parameters))
    
if __name__ == "__main__":
    main()