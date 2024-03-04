import requests


def get_report_trading_view():
    '''
        A "Strong Buy" or "Strong Sell" state appears when the signal is 
    above/below the 0.5/-0.5 level. A "Buy" or "Sell" state appears when the 
    signal is above/below the 0.1/-0.1 level.
    The "Neutral" state appears when the signal is between 0.1 and -0.1 inclusively.
    https://www.tradingview.com/script/Jdw7wW2g-Technical-Ratings/#:~:text=A%20%22Strong%20Buy%22%20or%20%22,the%200.1%2F%2D0.1%20level.
    '''

    url = "https://scanner.tradingview.com/india/scan"

    payload = "{\"columns\":[\"name\",\"description\",\"logoid\",\"update_mode\",\"type\",\"typespecs\",\"Recommend.All\",\"exchange\"],\"filter\":[{\"left\":\"is_blacklisted\",\"operation\":\"equal\",\"right\":false}],\"ignore_unknown_fields\":false,\"options\":{\"lang\":\"en\"},\"range\":[0,100],\"sort\":{\"sortBy\":\"Recommend.All\",\"sortOrder\":\"asc\"},\"symbols\":{\"symbolset\":[\"SYML:NSE;NIFTY\"]},\"markets\":[\"india\"],\"filter2\":{\"operator\":\"and\",\"operands\":[{\"operation\":{\"operator\":\"or\",\"operands\":[{\"operation\":{\"operator\":\"and\",\"operands\":[{\"expression\":{\"left\":\"type\",\"operation\":\"equal\",\"right\":\"stock\"}},{\"expression\":{\"left\":\"typespecs\",\"operation\":\"has\",\"right\":[\"common\"]}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"expression\":{\"left\":\"type\",\"operation\":\"equal\",\"right\":\"stock\"}},{\"expression\":{\"left\":\"typespecs\",\"operation\":\"has\",\"right\":[\"preferred\"]}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"expression\":{\"left\":\"type\",\"operation\":\"equal\",\"right\":\"dr\"}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"expression\":{\"left\":\"type\",\"operation\":\"equal\",\"right\":\"fund\"}},{\"expression\":{\"left\":\"typespecs\",\"operation\":\"has_none_of\",\"right\":[\"etf\"]}}]}}]}}]}}"
    headers = {
        'authority': 'scanner.tradingview.com',
        'accept': 'application/json',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'text/plain;charset=UTF-8',
        'origin': 'https://in.tradingview.com',
        'pragma': 'no-cache',
        'referer': 'https://in.tradingview.com/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload, timeout=6000)
    body = response.json()
    report = dict()
    for tick in body['data']:
        value = tick['d'][6]
        symbol = tick['d'][0]
        if value > 0.5:
            flag = 'Strong buy'
        elif value > .1:
            flag = 'Buy'
        elif value > -.1:
            flag = 'Neutral'
        elif value > -0.5:
            flag = 'sell'
        else:
            flag = 'Strong sell'
        report[symbol] = flag
    return report


print(get_report_trading_view())
