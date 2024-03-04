# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/4
@Software: PyCharm
@disc:
======================================="""
import json
import time

import requests


def exists(i, name, src_url, dst_url):
    times = 0
    while True:
        _resp = requests.get(dst_url, headers={"Cookie": gitlab_cookies})
        if _resp.status_code == 200:
            with open("projects/" + name + ".html", "wb") as f:
                f.write(_resp.content)
            print(
                "{}, {}, {}    ======>   {}, ✅({})".format(i, name, src_url, dst_url, _resp.status_code))
            return True
        elif _resp.status_code == 404:
            print("{}, {}, {}    ======>   {}, ❌({})".format(i, name, src_url, dst_url, _resp.status_code))
            return False
        else:
            times += 1
            time.sleep(1)


def gitlab_create_project(name, namespace_id: int, src_url, path, description: str):
    """
    """
    resp = requests.post("{}/projects".format(gitlab_base_url),
                         data={
                             "name": name,
                             "url": src_url,
                             "authenticity_token": gitlab_auth_token,
                             "project[import_url]": src_url,
                             "project[import_url_user]": gitee_usrname,
                             "project[import_url_password]": gitee_password,
                             "project[ci_cd_only]": False,
                             "project[name]": name,
                             "project[selected_namespace_id]": namespace_id,
                             "project[namespace_id]": namespace_id,
                             "project[path]": path,
                             "project[description]": description,
                             "project[visibility_level]": 0
                         },
                         headers={"Cookie": gitlab_cookies, "Content-Type": "application/x-www-form-urlencoded"}
                         )
    print("创建完成:", resp.status_code)
    with open("projects/create-post-pages/{}.html".format(path), mode="wb") as f:
        f.write(resp.content)


def main():
    repo = []
    # FIXME: 实现直接爬虫,而不是手动存储接口响应
    #  https://api.gitee.com/enterprises/<enter-prise-id>/projects?page=6&per_page=20&direction=desc&sort=last_push_at&fork_filter=not_fork
    for p in range(1, 6):
        fp = "projects_p{}.json".format(p)
        with open(fp, mode="rb") as f:
            resp = json.load(f)
            data = resp['data']
            repo.extend(data)
    for i in range(len(repo)):
        data = repo[i]
        name = data["name"]
        namespace = data['path']
        gitee_path_with_namespace = data['path_with_namespace']
        gitee_url = "https://gitee.com/{}.git".format(gitee_path_with_namespace)
        git_1_ink_url = "{}/{}/{}".format(gitlab_base_url, gitlab_namespace_name, namespace)
        if not exists(i, name, gitee_url, git_1_ink_url):
            gitlab_create_project(name, gitlab_namespace_id, gitee_url, namespace, data["description"])


if __name__ == '__main__':
    gitee_usrname = "<gitee-username>"
    gitee_password = "<gitee-password>"
    gitlab_cookies = "gitlab-cookies"
    gitlab_auth_token = "<gitlab-auth-token>"
    gitlab_base_url = "https://<selfhost-gitlab-host>"
    gitlab_namespace_name = "<gitlab-group-name>"
    gitlab_namespace_id = int("<gitlab-group-id:int>")
    main()
