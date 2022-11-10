import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from services.common.gi import home_path

chrome_driver = os.path.join(home_path, ".env/chromedriver", "chromedriver")
chrome_options = Options()
chrome_options.add_argument("--headless")


def f_to_c(x):
    return round((x - 32) * 5 / 9)


def fetch():
    url = "https://weather.com/weather/today/l/e4f3028ded4eaa85aa504baa51acd7b6df7932ebc68c9d7aff1c838d1178f42c"
    driver = webdriver.Chrome(service=Service(chrome_driver), options=chrome_options)
    driver.get(url)
    loc_div = driver.find_element(by=By.CLASS_NAME, value="CurrentConditions--header--kbXKR")
    temp_div = driver.find_element(by=By.CLASS_NAME, value="CurrentConditions--tempValue--MHmYY")
    cond_div = driver.find_element(by=By.CLASS_NAME, value="CurrentConditions--phraseValue--mZC_p")
    data_lst = driver.find_elements(by=By.CLASS_NAME, value="WeatherDetailsListItem--wxData--kK35q")
    out_lst = [loc_div.text, temp_div.text, cond_div.text]
    for element in data_lst:
        out_lst.append(element.text)
    driver.close()
    driver.quit()
    return out_lst


def print_info():
    data_lst: list[str] = fetch()
    temperatures = data_lst[3].split(sep="/")
    high_temp = temperatures[0][:-1]
    low_temp = temperatures[1][:-1]
    if high_temp.isnumeric():
        high_temp = f"{f_to_c(int(high_temp))}°C"
    else:
        high_temp = "--"
    if low_temp.isnumeric():
        low_temp = f"{f_to_c(int(low_temp))}°C"
    else:
        low_temp = "--"
    print(f"---")
    print(f"Location: {data_lst[0]}")
    print(f"Current temperature: {f_to_c(int(data_lst[1][:-1]))}°C")
    print(f"High/Low temperature: {high_temp}/{low_temp}")
    print(f"Condition: {data_lst[2]}")
    print(f"Wind: {round(int(data_lst[4][:-3]) * 1.61)} kmh")
    print(f"Humidity: {data_lst[5]}")
    print(f"Moon phase: {data_lst[10]}")


def get_weather_info():
    data_lst: list[str] = fetch()
    temperatures = data_lst[3].split(sep="/")
    high_temp = temperatures[0][:-1]
    low_temp = temperatures[1][:-1]
    if high_temp.isnumeric():
        high_temp = f"{f_to_c(int(high_temp))}°C"
    else:
        high_temp = "--"
    if low_temp.isnumeric():
        low_temp = f"{f_to_c(int(low_temp))}°C"
    else:
        low_temp = "--"
    return {"location": data_lst[0],
            "currentTemperature": f"{f_to_c(int(data_lst[1][:-1]))}°C",
            "highLowTemperature": f"{high_temp}/{low_temp}",
            "condition": data_lst[2],
            "wind": f"{round(int(data_lst[4][:-3]) * 1.61)} kmh",
            "humidity": data_lst[5],
            "moonPhase": data_lst[10], }


if __name__ == "__main__":
    data_list = fetch()
    print(data_list)
    print_info()
