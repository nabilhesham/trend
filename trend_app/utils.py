from pytrends.request import TrendReq
import requests
from .models import Trend, TrendName


def save_to_database(trend_name, data, search_type):
    if type(trend_name) == list and type(data) == list and search_type == 'intereset_by_region':
        for trend in trend_name:
            trend_name = TrendName.objects.create(name=trend, search_type=search_type)
            c1=0
            c2=0
            for k, v in data[c1].items():
                if c2 > 50:
                    break
                Trend.objects.create(name=trend_name, region=str(k), interest=v)
                c2=+1
            c1+=1
        return True

    elif search_type == 'get_historical_interest':
        trend = TrendName.objects.create(name=trend_name, search_type=search_type)
        counter=0
        for k, v in data.items():
            if counter > 50:
                break
            Trend.objects.create(name=trend, date=str(k).split(" ")[0], interest=v)
            counter =+ 1
        return True

    return False

def get_data(keyword, trend_type):
    pytrend = TrendReq(hl='en-US', tz=360)

    if trend_type == 'get_historical_interest':
        pytrend.build_payload(kw_list=[keyword], cat=0, timeframe='today 3-m',
            geo='', gprop='')
        data = pytrend.get_historical_interest([keyword])
        data = data.to_dict()[keyword]
        return data

    elif trend_type == 'intereset_by_region':
        all_data = []
        # keywords = [i.lstrip(' ') for i in keyword.split(',') if i.startswith(' ') or i]
        for k in keyword:
            pytrend.build_payload([k])
            data = pytrend.interest_by_region()
            print('########3', data.to_dict()[k])
            all_data.append(data.to_dict()[k])
        return all_data
    return None

def get_from_api(name=None, s_type=None):
    if name and s_type=='get_historical_interest':
        return requests.get('http://127.0.0.1:8000/api/trends/?name={}&type={}'.format(name, s_type)).json()

    elif type(name)==list and s_type=='intereset_by_region':
        all_data = []
        for k in name:
            data = requests.get('http://127.0.0.1:8000/api/trends/?name={}&type={}'.format(k, s_type)).json()
            all_data.append(data)
        return all_data
    else:
        return None