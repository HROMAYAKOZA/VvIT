import requests
print("hello-world")
s_city = "Moscow,RU"
appid = "<токен>"
res = requests.get("http://api.openweathermap.org/data/2.5/weather",\
params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
print("Город:",s_city)
print("Скорость ветра и видимость в городе сейчас:")
print("Скорость ветра <",data['wind']['speed'], "м/с > Видимость <",data['visibility'],"метров >")
res2 = requests.get("http://api.openweathermap.org/data/2.5/forecast",\
params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data2 = res2.json()
print("Прогноз скорости ветра и видимости в городе на неделю:")
for i in data2['list']:
    print("Дата <", i['dt_txt'], "> Скорость ветра: <", i['wind']['speed'], "м/с > Видимость <", i['visibility'], " метров >") 