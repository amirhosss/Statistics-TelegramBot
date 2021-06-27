import requests
import scipy.stats as st
import json

# Fetching from external api
def chart_api(distribution, data, param=0):
    # Set proxy for fetching from api
    # Proxy = {'https': 'http://127.0.0.1:1080'}
    
    url = 'https://quickchart.io/chart/create'

    _param = {'n': [st.norm.pdf(x/10) for x in range(-40, 41)], 
              't': [st.t.pdf(x/10, param) for x in range(-40, 41) if param > 0]}
    _data = {
        'chart': {
            'type': 'line',
            'data': {
                'labels': [x/10 for x in range(-40, 41)],
                'datasets': [{
                    'type': 'line',
                    'label': distribution + ' distribution',
                    'data': _param[distribution],
                    'fill': False,
                    'borderColor': '#347C98',
                    'pointRadius': 2,
                    'pointBorderColor': 'rgb(75, 192, 192)'
                }, {
                    'type': 'bubble',
                    'label': 'Answer',
                    'data': [{'x': round(data[0], 1), 'y': round(data[1], 5), 'r': 5}], 
                    'backgroundColor': '#C21460'

                }]}}, 
        'format': 'png'}

    try:
        message = ['Fetching from api ... \U0001f60a']
        res = requests.post(url, json=_data)
        pic_url = json.loads(res.text)['url']

        response = requests.get(pic_url)
        message.append('Processing image ...')

        return response.content, message

    except Exception as e:
        message.append(f'Raise an exception while fetching : {e} \u1F61E')
        
        return None, message

