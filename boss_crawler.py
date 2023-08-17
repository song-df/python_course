import csv
import requests
import json
import os
import time

# 读取保存的信息，如果文件不存在则使用默认值
if os.path.isfile('settings.json'):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
else:
    settings = {
        'last_page': 1,
        'output_file': 'Boss-Python.csv',
        'url_template': 'https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=python&city=100010000&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page={page}&pageSize=30'
    }

# 打开文件时选择适当的模式（a：追加）
file_mode = 'a' if os.path.isfile(settings['output_file']) else 'w'

# 打开csv文件
with open(settings['output_file'], encoding='utf8', newline='', mode=file_mode) as file:
    name = ['岗位', '薪资', '经验', '学位', '技能', '公司', '福利待遇', '城市', '区域']
    w = csv.DictWriter(file, name)
    # 如果文件不存在，则写入表头
    if file_mode == 'w':
        w.writeheader()

    # 循环访问从最后一页开始的所有页数
    page = settings['last_page']
    while True:
        url = settings['url_template'].format(page=page)
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58",
            "Cookie": "lastCity=101210100; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1691744292; wd_guid=f732837c-0ad6-4435-9c1d-452f88102aa1; historyState=state; _bl_uid=IelLkl9568scF6v49l0an5hn9nOw; wt2=Dchy0qt8Fy6RDdYCG4EPNH3EsQcMHd1HLSOuRceZuW4zvuYhg0tIFoFyyKiAIltB-NMswJr0PadkggQP6JBG1Wg~~; wbg=0; JSESSIONID=7E503365F3AB32006D52A29500B99CC7; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1692168241; __c=1691744292; __l=l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3Dpython%26city%3D101210100&r=&g=&s=3&friend_source=0&s=3&friend_source=0; __a=88954623.1691744292..1691744292.33.1.33.33; geek_zp_token=V1Q9ogEuH82VdgXdNgzRweISO27zPfxw~~; __zp_stoken__=94edeWGJvPTB0TG9ISXhvLnEXfxgXSgBfOyxsXzVATGQoAhdHczgYJWpmekFyFkE0R1d%2BQAB2NiB0IHUAIA1MJGY6V1ZDAj8bCw9fTxloZXVnMDoGDRpMX1RfXh9XfxF%2FBW5MP31WNFg2YXQ%3D"
        }
        html = requests.get(url, headers=head).text

        # 解析JSON响应
        data = json.loads(html)

        code = data.get('code', -1)  # 获取 code 字段的值，默认为 -1
        if code != 0:
            message = data.get('message', '未知错误')
            print(f"访问第 {page} 页时出错: {message}")
            break

        job_list = data['zpData']['jobList']

        if not job_list:
            break  # 停止循环，没有更多数据

        print(f"正在访问第 {page} 页...")

        for job in job_list:
            jobname = job['jobName']
            salary = job['salaryDesc']
            experience = job['jobExperience']
            degree = job['jobDegree']
            skills = ', '.join(job['skills'])
            company = job['brandName']
            welfare = ', '.join(job['welfareList'])
            city = job['cityName']
            area = job['areaDistrict']

            w.writerow({
                '岗位': jobname,
                '薪资': salary,
                '经验': experience,
                '学位': degree,
                '技能': skills,
                '公司': company,
                '福利待遇': welfare,
                '城市': city,
                '区域': area
            })

        page += 1
        print(f"正在等待 10 秒...")
        time.sleep(10)  # 暂停10秒

# 更新保存的信息
settings['last_page'] = page
with open('settings.json', 'w') as f:
    json.dump(settings, f)
