import os
import time
import requests
import signal
import sys

# 定义信号处理函数
def handle_sigterm(*args):
    print("SIGTERM received, exiting gracefully...")
    sys.exit(0)

# 注册信号处理函数
signal.signal(signal.SIGTERM, handle_sigterm)

# 间隔时间设置为30分钟
interval = 30 * 60

api_urls = os.getenv('API_URLS').split(',')
webhook_url = os.getenv('WEBHOOK_URL')

if not webhook_url:
    raise ValueError("WEBHOOK_URL environment variable is not set.")

while True:
    for api_url in api_urls:
        # 分割URL并提取镜像名（倒数第三个和倒数第二个部分）
        parts = api_url.rstrip('/').split('/')
        if len(parts) >= 2:
            repository_name = f"{parts[-3]}/{parts[-2]}"
        else:
            print(f"URL {api_url} is not valid for extracting the repository name.")
            continue
        
        last_update_time_file = f'/data/last_update_time_{repository_name.replace("/", "_")}.txt'
        
        try:
            with open(last_update_time_file, 'r') as file:
                last_update_time = file.read().strip()
        except FileNotFoundError:
            last_update_time = ""
        
        response = requests.get(api_url)
        data = response.json()
        
        # 请确保这里的逻辑适用于你的API结构
        current_update_time = data['results'][0]['last_updated'] if 'results' in data and data['results'] else None
        
        if current_update_time and current_update_time != last_update_time:
            message = {
                "msgtype": "text",
                "text": {
                    "content": f"镜像 {repository_name} 的latest标签已更新: {current_update_time}"
                }
            }
            requests.post(webhook_url, json=message)
            
            with open(last_update_time_file, 'w') as file:
                file.write(current_update_time)

    time.sleep(interval)

