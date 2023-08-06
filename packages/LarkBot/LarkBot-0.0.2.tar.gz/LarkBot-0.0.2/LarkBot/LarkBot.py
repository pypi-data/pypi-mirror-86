import json
import re
import requests
class Bot:
    def __init__(self,AppID,AppSecret):
        self.AppID=AppID
        self.AppSecret=AppSecret
        url="https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
        header={"Content-Type":"application/json"}
        data=json.dumps({
        "app_id":self.AppID,
        "app_secret":self.AppSecret,
        })
        res=requests.post(url,data=data,headers=header)
        self.token="Bearer "+eval(res.text)["tenant_access_token"]
        return None
    def textMessage(self,open_id=None,user_id=None,email=None,chat_id=None,root_id=None,mention=None,text=None):
        url="https://open.feishu.cn/open-apis/message/v4/send/"
        header={"Authorization":self.token,"Content-Type":"application/json"}
        if mention != None:
            for id in mention:
                text='<at user_id="'+id+'">''</at>'+text
        data=json.dumps({       
        "user_id": user_id,
        "chat_id":chat_id,
        "email":email,
        "chat_id":chat_id,
        "root_id":root_id,
        "msg_type":"text",
        "content":{
                "text":text  
        }
        })
        res=requests.post(url,data=data,headers=header)
        return res
    def upload_image(self,image_path):
        with open(image_path, 'rb') as f:
            image = f.read()
        resp = requests.post(
            url='https://open.feishu.cn/open-apis/image/v4/put/',
            headers={'Authorization': self.token},
            files={
                "image": image
            },
            data={
                "image_type": "message"
            },
            stream=True)
        resp.raise_for_status()
        content = resp.json()
        print(content)
        if content.get("code") == 0:
            return content["data"]['image_key']
        else:
            raise Exception("Call Api Error, errorCode is %s" % content["code"])
    def imageMessage(self,open_id=None,user_id=None,email=None,chat_id=None,root_id=None,image_path=None):
        url="https://open.feishu.cn/open-apis/message/v4/send/"
        header={"Authorization":self.token,"Content-Type":"application/json"}
        data=json.dumps({       
        "user_id": user_id,
        "chat_id":chat_id,
        "email":email,
        "chat_id":chat_id,
        "root_id":root_id,
        "msg_type":"image",
        "content":{
                "image_key":self.upload_image(image_path)
        }
        })
        res=requests.post(url,data=data,headers=header)
        return res
    def postMessage(self,open_id=None,user_id=None,email=None,chat_id=None,root_id=None,mention=None,title=None,content=None):
        url="https://open.feishu.cn/open-apis/message/v4/send/"
        header={"Authorization":self.token,"Content-Type":"application/json"}
        #解析富文本
        content=content.split('\n')
        while '' in content:
            content.remove('')
        import re
        for i in range(len(content)):
            if content[i][0]=="(":
                content[i]=[{"tag":"img","image_key":self.upload_image(content[i][1:-1])}]
            elif content[i][0]=='[':
                content[i]=[{"tag":"a","text":re.sub(r"[\[\]]","",re.search(r"(\[.*?\])",content[i]).group()).strip(),"href":re.sub(r"[()]","",re.search(r"(\(.*?\))",content[i]).group()).strip()}]
            else:
                content[i]=[{"tag": "text","text":content[i]}]
        if mention !=None:
            for id in mention:
                content.append([{"tag": "at","user_id":id}])


        data=json.dumps({       
        "user_id": user_id,
        "chat_id":chat_id,
        "email":email,
        "chat_id":chat_id,
        "root_id":root_id,
        "msg_type":"post",
        "content":{
            "post":{
                "zh_cn":{
                    "title":title,
                    "content":content
                }
            }
        }
        })
        res=requests.post(url,data=data,headers=header)
        return res

    def userId(self,emails=None,mobiles=None):
        url="https://open.feishu.cn/open-apis/user/v1/batch_get_id"
        header={"Authorization":self.token}
        data={
        "mobiles":mobiles,
        "emails":emails,
        }
        res=requests.post(url,data=data,headers=header)
        return eval(res.text)["data"]['mobile_users'][mobiles][0]
    def groupId(self,name):
        url="https://open.feishu.cn/open-apis/chat/v4/list"
        header={"Authorization":self.token}
        res=requests.get(url,headers=header)
        for group in json.loads(res.text)["data"]["groups"]:
            if group["name"]==name:
                return group["chat_id"]
           
        return "未找到"


        

    def createGroup(self,name=None,description=None,open_ids=None,user_ids=None,i18n_names=None,only_owner_add=False,share_allowed=False,only_owner_at_all=False,only_owner_edit=False):

        url="https://open.feishu.cn/open-apis/chat/v4/create/"
        header={"Authorization":self.token,"Content-Type":"application/json"}
        data=json.dumps({
            "name":name,
            "description":description,
            "open_ids":open_ids,
            "user_ids":user_ids,
            "i18n_names":i18n_names,
            "only_owner_add":only_owner_add,
            "share_allowed":share_allowed,
            "only_owner_at_all":only_owner_at_all,
            "only_owner_edit":only_owner_edit
        })
        res=requests.post(url,data=data,headers=header)
        return res

    def destoryGroup(self,chat_id):
        url="https://open.feishu.cn/open-apis/chat/v4/disband"
        header={"Authorization":self.token,"Content-Type":"application/json"}
        data=json.dumps({
            "chat_id":chat_id
        })
        res=requests.post(url,data=data,headers=header)
        return res
