#coding:utf-8
from selenium import webdriver
import time
import pandas as pd

driver = webdriver.Chrome(executable_path=r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver')

mobile_list = pd.read_excel("mobile.xlsx",header=None)
my_list = []
for m in mobile_list[0]:
    single_info = ['', '', '', '', 0, '', '', '', '', '', '', '', '', '', '']
    #m = "Redmi Note5A Prime"
    single_info[0] = m

    input_first = ""
    for eid in range(1,11):
        try:
            driver.get('https://www.baidu.com/s?wd=中关村cell_phone ' + str(m))
            fetch_url = driver.find_element_by_id(str(eid)).find_element_by_class_name("c-showurl")
            fetch_a = driver.find_element_by_id(str(eid)).find_element_by_tag_name('h3').find_element_by_tag_name('a')
            if(("百度知道" not in fetch_url.text) and
                   ("detail.zol.com.cn/cell" in fetch_url.text or "detail.zol.com.cn/tabl" in fetch_url.text)):
                if("detail.zol.com.cn/cell" in fetch_url.text):
                    single_info[2] = "手机"
                else:
                    single_info[2] = "平板电脑"
                driver.get(fetch_url.get_attribute('href'))
                single_info[1] = driver.current_url
                break
        except:
            single_info[1] = ""

    if ("zol" in single_info[1]):
        try:
            single_info[3] = driver.find_element_by_class_name("product-model__name").text
            get_price = driver.find_element_by_class_name("price-type").text
            if("停产" in get_price):
                single_info[5] = "停产"
            elif('概念产品' in get_price):
                single_info[5] = "概念产品"
            elif('即将上市' in get_price):
                single_info[5] = "即将上市"
            elif('万' in get_price):
                single_info[4] = int(float(get_price.split('万')[0]) * 10000)
            else:
                single_info[4] = int(get_price.split('-')[0])

            #修正上市状态
            get_status = driver.find_elements_by_class_name("price-status")
            if (len(get_status) > 0 and "停产" in get_status[0].text):
                single_info[5] = "停产"
            elif(single_info[5] == ""):
                single_info[5] = "正常"

            #上市时间
            get_market = driver.find_elements_by_class_name("section-header-desc")
            if (len(get_market) > 0 and "上市时间" in get_market[0].text):
                single_info[6] = get_market[0].text.split('：')[1]

            get_paras = driver.find_elements_by_class_name("product-param-item")
            if(len(get_paras)>0):
                get_paras = get_paras[0].find_elements_by_tag_name("p")
                #主屏尺寸
                single_info[7] = get_paras[0].text.split('：')[1]
                #主屏分辨率
                single_info[8] = get_paras[1].text.split('：')[1]
                #后置摄像头
                single_info[9] = get_paras[2].text.split('：')[1]
                #前置摄像头
                single_info[10] = get_paras[3].text.split('：')[1]
                #电池容量
                single_info[11] = get_paras[4].text.split('：')[1]
                #电池类型
                single_info[12] = get_paras[5].text.split('：')[1]
                #核心数
                single_info[13] = get_paras[6].text.split('：')[1]
                #内存
                single_info[14] = get_paras[7].text.split('：')[1]
            else:
                if(len(driver.find_elements_by_class_name("t-danshou"))>0):
                    single_info[7] = driver.find_element_by_class_name("t-danshou").find_element_by_class_name("product-link").text
                else:
                    single_info[7] = driver.find_element_by_class_name("t-shuangshou").find_element_by_class_name("product-link").text
                if(len(driver.find_elements_by_class_name("t-fenbianlv-hd"))>0):
                    single_info[8] = driver.find_element_by_class_name("t-fenbianlv-hd").find_element_by_class_name("product-link").text
                elif(len(driver.find_elements_by_class_name("t-fenbianlv-720p"))>0):
                    single_info[8] = driver.find_element_by_class_name("t-fenbianlv-720p").find_element_by_class_name("product-link").text
                if(len(driver.find_elements_by_class_name("t-xiangsu-hd"))==2):
                    single_info[9] = driver.find_elements_by_class_name("t-xiangsu-hd")[0].find_element_by_class_name("product-link").text
                    single_info[10] = driver.find_elements_by_class_name("t-xiangsu-hd")[1].find_element_by_class_name("product-link").text
                elif(len(driver.find_elements_by_class_name("t-xiangsu-hd"))==1):
                    single_info[9] = driver.find_elements_by_class_name("t-xiangsu-hd")[0].find_element_by_class_name("product-link").text
                    single_info[10] = driver.find_elements_by_class_name("t-xiangsu-putong")[0].find_element_by_class_name("product-link").text
                else:
                    single_info[9] = driver.find_elements_by_class_name("t-xiangsu-putong")[0].find_element_by_class_name("product-link").text
                    single_info[10] = driver.find_elements_by_class_name("t-xiangsu-putong")[1].find_element_by_class_name("product-link").text
                if(len(driver.find_elements_by_class_name("t-dianchirongliang-yiban"))>0):
                    single_info[11] = driver.find_element_by_class_name("t-dianchirongliang-yiban").find_element_by_class_name("product-link").text
                else:
                    single_info[11] = driver.find_element_by_class_name("t-dianchirongliang-ruo").find_element_by_class_name("product-link").text
                single_info[14] = driver.find_element_by_class_name("t-ramrongliang-liuchang").find_element_by_class_name("product-link").text
        except:
            single_info[5] = "非售"
    else:
        single_info[5] = "非售"
    my_list.append(single_info)
    print(single_info)
df = pd.DataFrame(my_list,columns=['model', 'website', 'type', 'fullname', 'price', 'status', 'time_to_market',
                                   'size', 'resolution', 'rear_camera', 'front_camera', 'battery_size', 'battery_type', 'CPU', 'memory'])
df.to_csv("mobile.csv")

#main_para = driver.find_element_by_class_name("product-param-item pi-57 clearfix").find_elements_by_tag_name("p")


#driver.maximize_window()
#time.sleep(2)
#driver.find_element_by_xpath("./*//input[@value='百度一下']").click()