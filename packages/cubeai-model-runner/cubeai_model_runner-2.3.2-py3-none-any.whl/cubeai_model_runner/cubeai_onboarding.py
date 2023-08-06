import json
import yaml
import getpass
import requests
from urllib3 import encode_multipart_formdata


url_server = 'https://cubeai.dimpt.com'
url_login = '{}/api/data'.format(url_server)
url_onboarding = '{}/umu/api/file/onboard_model'.format(url_server)


def get_tokens():
    username = input('username:')
    password = getpass.getpass('password:')

    body = {
        'action': 'login_cmd',
        'args': {
            'username': username,
            'password': password,
        }
    }
    res = requests.post(url_login, json=body)
    res = json.loads(res.text, encoding='utf-8')

    if res['status'] == 'ok':
        tokens = res['value']
        return 'refresh_token={}; access_token={}'.format(tokens['refresh_token'], tokens['access_token'])
    else:
        return None


def get_file_path():
    try:
        with open('./application.yml', 'r') as f:
            yml = yaml.load(f, Loader=yaml.SafeLoader)
    except:
        print('错误： 模型配置文件application.yml不存在！')
        return None

    try:
        name = yml['model']['name']
    except:
        print('错误： 未指定模型名称！')
        print('请在application.yml文件中编辑修改...')
        return None

    return 'out/{}.zip'.format(name)


def onboarding():
    file_path = get_file_path()
    if file_path is None:
        return

    tokens = get_tokens()
    if tokens is None:
        print('用户名或密码错误！')
        return

    data = {
        'onboard_model': (file_path.split('/')[-1], open(file_path, 'rb').read())
    }
    encode_data = encode_multipart_formdata(data)

    headers = {
        'Content-Type': encode_data[1],
        'Cookie': tokens,
    }

    res = requests.post(url_onboarding, headers=headers, data=encode_data[0])
    res = json.loads(res.text, encoding='utf-8')
    if res['status'] == 'ok':
        print('文件上传成功！请在CubeAI平台[我的任务]页面中查看模型导入进度...')
    else:
        print('文件上传失败： {}'.format(res['value']))


if __name__ == '__main__':
    onboarding()
