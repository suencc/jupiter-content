# -*- coding:utf-8 -*-
import requests

def getlocation(addr, city='广州'):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    try:
        params = {'output': 'json', 'ak': 'cRNPOVMNnk7DC82p9w9qR3sL', 'address': addr, 'city': city }
        r = requests.get(url, params)
        print(r.url)
        if r.status_code == 200 or r.status_code == 304:
            print(r.json()['result']['location'])
            return r.json()['result']['location']
        else:
            print(r.status_code)
            return r.status_code
    except Exception as e:
        print("ERROR:", e)
        return 404
    
START_LNG  = 113.297942
END_LNG = 113.466578
START_LAT = 23.093353
END_LAT = 23.263226
LNG_GRIDS = 20
LAT_GRIDS = 18
LNG_DELTA = round((END_LNG - START_LNG) / LNG_GRIDS, 7)
LAT_DELTA = round((END_LAT - START_LAT) / LAT_GRIDS, 7)

# 不在范围内则返回 -1
# 边界值时会出现随机现象，和python的浮点处理不精确有关
# 只要保证插入和读取都用此函数，不影响分析正确性
# 查表获取ID，太繁琐低效，后续如有需要则改为查表
def get_grid_id(lng, lat):
    column = round((lng - START_LNG),7) // LNG_DELTA + 1
    row = round((END_LAT - lat),7) // LAT_DELTA + 1
    if column < 1 or column > 20: return -1
    if row < 1 or row > 18: return -1
    ret = 'R%dC%d' % (row, column)
    return ret    

# 测试函数    
def test_grid_id():
    # 边界测试
    gridid = get_grid_id(113.29794200,23.26322600)
    print('gridid = %s, right gridid = R1C1' % gridid)    
    gridid = get_grid_id(113.3063738,23.2537886)
    print('gridid = %s, right gridid = R2C2' % gridid)
    gridid = get_grid_id(113.466577,23.093353)
    print('gridid = %s, right gridid = R18C20' % gridid)
    gridid = get_grid_id(113.3485328,23.216039)
    print('gridid = %s, right gridid = R5C7' % gridid)
    gridid = get_grid_id(113.3485328,23.2066016)
    print('gridid = %s, right gridid = R6C7' % gridid)    
    # 一般测试
    gridid = get_grid_id(113.3991237,23.1877267)
    print('gridid = %s, right gridid = R9C13' % gridid) 
    gridid = get_grid_id(113.4581461,23.1782895)
    print('gridid = %s, right gridid = R9C19' % gridid)
    gridid = get_grid_id(113.4328509,23.121666)
    print('gridid = %s, right gridid = R15C17' % gridid)
    gridid = get_grid_id(113.4581461,23.1311023)
    print('gridid = %s, right gridid = R15C19' % gridid)
    gridid = get_grid_id(113.3906919,23.1027901)
    print('gridid = %s, right gridid = R18C12' % gridid)  
if __name__ == '__main__':
    test_grid_id()

