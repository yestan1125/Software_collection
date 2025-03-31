import requests
import tkinter as tk
from tkinter import messagebox
from win10toast import ToastNotifier

# 配置你的OpenWeatherMap API Key（直接写在代码里）
API_KEY = "c289989b03ff887fa430783e4b992676"  # 请替换成你自己的API Key

API_URL = "http://api.openweathermap.org/data/2.5/weather"
UPDATE_INTERVAL = 7200000  # 每两小时更新一次

notifier = ToastNotifier()

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",  # 摄氏度
        "lang": "zh_cn"
    }
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"{city}天气：{weather}, 温度：{temp}°C"
    except Exception as e:
        return f"获取天气信息失败: {e}"

def update_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("提示", "请填写城市名称")
        return

    result = get_weather(city)
    weather_label.config(text=result)
    notifier.show_toast("天气提醒", result, duration=10, threaded=True)
    # 添加弹窗通知
    messagebox.showinfo("天气信息", result)
    root.after(UPDATE_INTERVAL, update_weather)

def start_updates():
    update_weather()
    city_entry.config(state="disabled")
    start_button.config(state="disabled")

# 创建UI界面
root = tk.Tk()
root.title("天气推送应用")
root.geometry("400x200")

tk.Label(root, text="请输入城市名称：").pack(pady=5)
city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=5)
city_entry.insert(0, "Beijing")  # 默认示例

start_button = tk.Button(root, text="开始推送天气", command=start_updates)
start_button.pack(pady=10)

weather_label = tk.Label(root, text="等待更新...", font=("Arial", 12))
weather_label.pack(pady=10)

root.mainloop()
