import requests


def _requests(session, method, url, retry=20, timeout=20, **kwargs):
    """
    请求函数
    :param method: 请求方法 小写
    :param url: 请求链接
    :param retry: 请求重试次数 默认20
    :param timeout: 请求等待最大时间
    :param kwargs:
    :return:
    """
    if method in ["get", "post"]:
        # 请求重发
        for _ in range(retry + 1):
            try:
                # print("发送%s请求 %s" % (method, url))
                response = getattr(session, method)(url, timeout=timeout, **kwargs)
                return response
            except Exception as e:
                print(e)
    return []


if __name__ == '__main__':
    a = _requests(requests,"get","https://www.baidu.com")
    print(a.text)