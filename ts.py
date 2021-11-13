# header = {
#             'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; TAS-AN00 Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 dzhapp;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:140248;packageName:com.android.dazhihui',
#             }
# def gen_url_news(lnum=379990,rnum=380000):
#     url = lambda id: f'https://detailpage.dzh.com.cn/index.php?service=getNewsContent&id=topkuaixun-{id}&version=&token='
#     # full_urls = [url(i) for i in range(lnum,rnum)]
#     for i in range(lnum,rnum):
#         yield url(i)
# x = gen_url_news()
# # for i in x:
# #     print(i)
# # print(x)
# import requests

# r = requests.get(list(x)[0],headers=header)
# print(type(r.json()["Data"]["Found"]))

class A():
    def f1(self,b):
        b.f4()
    def f2(self,):
        print("f2")

class B():
    def f3(self,a):
        a.f1(self)
    def f4(self,):
        print("f4") 
class C():
    def f3(self,c):
        c.f4()
    def f4(self,):
        print("f4")
a = A()
b = B()
c = C()
a.f1(b)
b.f3(a)
c.f3(c)