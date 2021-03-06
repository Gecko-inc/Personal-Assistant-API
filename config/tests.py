def parse(url: str):
    import requests
    import re
    from datetime import datetime
    if url:
        ck = re.findall("ck\=(\S+)", url)
        print("Getting params:")
        params = (('lang', 'ru'), ('ck', ck),)
        if len(ck):
            print(f"ck={ck}")
            print("Getting numbers: ")
            numbers = re.findall("[\/](\d+)", url)
            print(f"numbers={numbers}")
            print("Making request")
            if len(numbers):
                url = "https://www.gosuslugi.ru/api/covid-cert/v3/cert/check/" + str(numbers[0])
                response = requests.get(url, params=params)
                unformatted_date = re.findall("\"expiredAt\"\:\"([\d+\.]+)\"", response.text)
                if len(unformatted_date):
                    date = datetime.strptime(unformatted_date[0], "%d.%m.%Y")
                    if date and date > datetime.now():
                        return True
    return False


a = "https://www.gosuslugi.ru/covid-cert/verify/9600000013636491?lang=ru&ck=f3843bab3faafdcd68aa186b13557ad2"
print(parse(a))
# parse('https://www.gosuslugi.ru/api/covid-cert/v3/cert/check/9600000013636491')
