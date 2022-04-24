from retry import retry
import requests

timeout_retry = retry(TimeoutError, delay=2, tries=3, max_delay=3)


@timeout_retry
def test_upload(host='127.0.0.1', port=5000):
    data = {
        'model_type': 'captcha'
    }
    files = {'file': open('../muggle_images/test02.jpg', 'rb')}
    res = requests.post('http://{}:{}/ocr/api/v1/muggle-ocr'.format(host, port), data=data,
                        files=files)
    print(res.text)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    test_upload()
