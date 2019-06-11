import requests, json, re
from django.conf import settings

host = settings.ZENTAO_HOST


class Zentao:
    @classmethod
    def login(cls, account, password):
        result = requests.get(f'{host}/api-getsessionid.json')
        zentaosid = result.cookies.get('zentaosid')
        result = requests.post(f'{host}/user-login.json?zentaosid={zentaosid}',
                               data={"account": account, "password": password, "keepLogin": "on"})
        if result.json().get('status') == 'success':
            user_info = result.json().get('user')
            return zentaosid, user_info
        else:
            return None, None

    @classmethod
    def get_product_list(cls, zentaosid):
        cookies = dict(zentaosid=zentaosid)
        result = requests.get(f'{host}/product-index.json', cookies=cookies)
        try:
            return [[key, value] for key, value in json.loads(result.json().get('data')).get('products').items()]
        except:
            return None

    @classmethod
    def get_project_list(cls, zentao_sid, product_id):
        cookies = dict(zentaosid=zentao_sid)
        result = requests.get(f'{host}/product-ajaxGetProjects-{product_id}-0-0.json', cookies=cookies)
        try:
            return [[k, v] for k, v in result.json().items() if k]
        except:
            return None

    @classmethod
    def get_all_users(cls, zentaosid):
        cookies = dict(zentaosid=zentaosid)
        result = requests.get(f'{host}/bug-ajaxLoadAllUsers.json', cookies=cookies)
        return re.findall("value='(.*?)' title='.*?:(.*?)' data-keys='(.*?)'", result.text)

    @classmethod
    def create_bug(cls, zentaosid, data, files=None):

        cookies = dict(zentaosid=zentaosid)
        result = requests.post(f'{host}/bug-create-{data.get("product")}-0-moduleID=0.xhtml', data=data, files=files,
                               cookies=cookies)
        print(result.text)
        if "alert('" in result.text:
            return False, re.findall("alert\('(.*?)'\)", result.text)[0]
        try:
            bug_id = re.findall('bug-view-(.*?)\.xhtml', result.text)[0]
            return True, bug_id
        except:
            return False, 'error'

    @classmethod
    def is_login(cls, zentaosid):
        cookies = dict(zentaosid=zentaosid)
        result = requests.get(f'{host}/api-getmodel-user-isLogon.json', cookies=cookies)
        if 'user-login' in result.text:
            return False
        elif 'success' in result.text:
            return True

    @classmethod
    def upload_file(cls, zentaosid, files):
        cookies = dict(zentaosid=zentaosid)
        result = requests.post(f'{host}/file-ajaxUpload.html?dir=image', files=files,
                               cookies=cookies)
        print(result.text)
        try:
            return result.json()['url'].replace('/zentao', "")
        except:
            return False


if __name__ == '__main__':
    pass
    print(Zentao.login('chengm'))
    # print(Zentao.get_product_list('h0gotg7gvftsmnh7im4o67sva1'))
    # print(Zentao.ping('0g3cm5m7fjh60d3rr3muet4hd3'))
    # print(Zentao.get_project_list('h0gotg7gvftsmnh7im4o67sva1', 19))
    # print(Zentao.get_all_users('h0gotg7gvftsmnh7im4o67sva1'))
    data = {
        'product': 27,
        'module': 0,
        'project': 391,
        'openedBuild[]': 'trunk',
        'assignedTo': 'chengm',
        'type': 'codeerror',
        'title': 'bug标题223332',
        'severity': '3',
        'pri': '3',
        'steps': '<p>[步骤]</p>1111<br /><p>	[结果]</p>2222<br /><p>	[期望]</p>33333',
        'mailto[1]': 'chengm',
        # 'files[1]': ("a.mp4", open("E:/Workspace/TMTServer/files/2019-03/1552395045974_video.mp4", "rb")),
        # 'files[2]': ("b.png", open("E:/Workspace/TMTServer/files/2019-03/1552395022317_image.png", "rb")),

    }
    files = {
        'files[1]': ("a.mp4", open("E:/Workspace/TMTServer/files/2019-03/1552395045974_video.mp4", "rb")),
        'files[2]': ("b.png", open("E:/Workspace/TMTServer/files/2019-03/1552395022317_image.png", "rb")),
    }
    # ("files[]", ("a.mp4", open("E:/Workspace/TMTServer/files/2019-03/1552289319880_video.mp4", "rb"))),
    # ("labels[]", "tu1"),
    # ("files[]", ("2.png", open("E:/Workspace/TMTServer/files/2019-03/1552290262736_image.png", "rb"), "image/png")),
    # ("labels[]", "tu2"),

    print(Zentao.create_bug('j3ja2otjh8ff1hko94v72cgd53', data, files))
    # Zentao.create_bug_model('0g3cm5m7fjh60d3rr3muet4hd3', data)
