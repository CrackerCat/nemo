#!/usr/bin/env python3
# coding:utf-8
# Build By LandGrey
# Modified by Hancool
import re
import ssl
import socket
import requests
from html.parser import HTMLParser
from requests.adapters import HTTPAdapter

from .taskbase import TaskBase


class WebTitle(TaskBase):
    '''获取网站title的任务
    参数：options
            {
                'target':[{'ip':'xxx','port':[80,443,8080]},...]    #ip和port列表的字典列表格式
            }
    任务结果：
        ip资产表的格式
        [{'ip': '218.19.148.193', 'port': [{'port': 80, 'title': 'xxx'}, {'port': 443, 'title': 'xxx'}]}]
    '''

    def __init__(self):
        super().__init__()
        self.__init_requests()
        self.timeout = 5
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "close",
        }
        self.patterns = (
            '<meta[\s]*http-equiv[\s]*=[\s]*[\'"]refresh[\'"][\s]*content[\s]*=[\s]*[\'"]\d+[\s]*;[\s]*url[\s]*=[\s]*(.*?)[\'"][\s]*/?>',
            'window.location[\s]*=[\s]*[\'"](.*?)[\'"][\s]*;',
            'window.location.href[\s]*=[\s]*[\'"](.*?)[\'"][\s]*;',
            'window.location.replace[\s]*\([\'"](.*?)[\'"]\)[\s]*;',
            'window.navigate[\s]*\([\'"](.*?)[\'"]\)',
            'location.href[\s]*=[\s]*[\'"](.*?)[\'"]',
        )

        self.source = 'portscan'
        self.result_attr_keys = ('title',)

    def __init_requests(self):
        '''对SSL的告警进行忽略
        '''
        try:
            requests.packages.urllib3.disable_warnings()
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

    def __out_format_call(self, url, information):
        '''格式化
        '''
        for char in ('\r', '\n', '\t'):
            information = information.replace(char, "")

        return information

    def __html_decoder(self, html_entries):
        '''html decoder
        '''
        try:
            hp = HTMLParser.HTMLParser()
            return hp.unescape(html_entries)
        except Exception as e:
            return html_entries

    def __match_title(self, content):
        '''正则匹配标题
        '''
        title = re.findall(
            "document\.title[\s]*=[\s]*['\"](.*?)['\"]", content, re.I | re.M | re.S)
        if title and len(title) >= 1:
            return title[0]
        else:
            title = re.findall("<title.*?>(.*?)</title>",
                               content, re.I | re.M | re.S)
            if title and len(title) >= 1:
                return title[0]
            else:
                return False

    def __page_decode(self, url, html_content):
        '''以多种编码方式对页面进行解码尝试
        '''
        raw_content = html_content
        try:
            html_content = raw_content.decode("utf-8")
        except UnicodeError:
            try:
                html_content = raw_content.decode("gbk")
            except UnicodeError:
                try:
                    html_content = raw_content.decode("gb2312")
                except UnicodeError:
                    try:
                        html_content = raw_content.decode("big5")
                    except:
                        # return __out_format_call(url, "DecodeHtmlError")
                        return None
        return html_content

    def __get_title(self, url):
        '''获取title
        '''
        origin = url
        if "://" not in url:
            url = "http://" + url.strip()
        url = url.rstrip("/") + "/"
        # First Try Obtain WebSite Title
        try:
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=1))
            s.mount('https://', HTTPAdapter(max_retries=1))
            req = s.get(url, headers=self.headers, verify=False,
                        allow_redirects=True, timeout=self.timeout)
            html_content = req.content
            req.close()
        except requests.ConnectionError:
            return None
            # return out_format_call(origin, "ConnectError")
        except requests.Timeout:
            return None
            # return out_format_call(origin, "RequestTimeout")
        except socket.timeout:
            return None
            # return out_format_call(origin, "SocketTimeout")
        except requests.RequestException:
            return None
            # return out_format_call(origin, "RequestException")
        except Exception as e:
            return None
            # return out_format_call(origin, "OtherException")
        html_content = self.__page_decode(url, html_content)
        if html_content:
            title = self.__match_title(html_content)
        else:
            # exit(0)
            return None
        try:
            if title:
                if re.findall("\$#\d{3,};", title):
                    title = self.__html_decoder(title)
                return self.__out_format_call(origin, title)
        except Exception as e:
            # return self.__out_format_call(origin, "FirstTitleError")
            return None
        # Find Jump URL
        for pattern in self.patterns:
            jump = re.findall(pattern, html_content, re.I | re.M)
            if len(jump) == 1:
                if "://" in jump[0]:
                    url = jump[0]
                else:
                    url += jump[0]
                break
        # Second Try Obtain WebSite Title
        try:
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=1))
            s.mount('https://', HTTPAdapter(max_retries=1))
            req = s.get(url, headers=self.headers,
                        verify=False, timeout=self.timeout)
            html_content = req.content
            req.close()
        except requests.ConnectionError:
            return None
            # return out_format_call(origin, "ConnectError")
        except requests.Timeout:
            return None
            # return out_format_call(origin, "RequestTimeout")
        except socket.timeout:
            return None
            # return out_format_call(origin, "SocketTimeout")
        except requests.RequestException:
            return None
            # return out_format_call(origin, "RequestException")
        except Exception as e:
            return None
            # return out_format_call(origin, "OtherException")
        html_content = self.__page_decode(url, html_content)
        if html_content:
            title = self.__match_title(html_content)
        else:
            # exit(0)
            return None
        try:
            if title:
                if re.findall("[$#]\d{3,};", title):
                    title = self.__html_decoder(title)
                return self.__out_format_call(origin, title)
            else:
                # return self.__out_format_call(origin, "NoTitle")
                return None
        except Exception as e:
            # return self.__out_format_call(origin, "SecondTitleError")
            return None

        return None

    def prepare(self, options):
        '''解析参数
        '''
        for ip in options['target']:
            if 'ip' not in ip or 'port' not in ip:
                continue
            ports = []
            for port in ip['port']:
                ports.append({'port': port})

            self.target.append({'ip': ip['ip'], 'port': ports})

    def execute(self, ips):
        '''获取主机端口上网站的title
        '''
        protocols = ('http', 'https')
        for ip in ips:
            if 'ip' not in ip or 'port' not in ip:
                continue
            for port in ip['port']:
                title = None
                for protocol in protocols:
                    title = self.__get_title(
                        '{}://{}:{}'.format(protocol, ip['ip'], port['port']))
                    if title:
                        break
                if title:
                    port['title'] = title

        return ips

    def run(self, options):
        '''获取主机端口title的任务
        '''
        self.prepare(options)
        self.execute(self.target)
        result = {'status': 'success', 'count': self.save_ip(self.target)}

        return result
