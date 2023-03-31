
# 在 ipykernel 中使用异步接口

在ipykernel 4.10+中默认运行,这就意味着在jupyter中使用协程并不需要显式的申明loop,只需要将协程使用`ensure_future`注册到loop上即可,使用的时候我们就需要关注下task的状态,当其状态是完成时我们就可以使用`result`接口获取到结果


```python
import asyncio
import aiohttp
```


```python
async def get_github():
    async with aiohttp.ClientSession() as session:
        response = await session.get('https://api.github.com')
        result = await response.json()
    return result

```


```python
task = asyncio.ensure_future(get_github())
```


```python
task.done()
```




    True




```python
result = task.result()
```


```python
result
```




    {'current_user_url': 'https://api.github.com/user',
     'current_user_authorizations_html_url': 'https://github.com/settings/connections/applications{/client_id}',
     'authorizations_url': 'https://api.github.com/authorizations',
     'code_search_url': 'https://api.github.com/search/code?q={query}{&page,per_page,sort,order}',
     'commit_search_url': 'https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}',
     'emails_url': 'https://api.github.com/user/emails',
     'emojis_url': 'https://api.github.com/emojis',
     'events_url': 'https://api.github.com/events',
     'feeds_url': 'https://api.github.com/feeds',
     'followers_url': 'https://api.github.com/user/followers',
     'following_url': 'https://api.github.com/user/following{/target}',
     'gists_url': 'https://api.github.com/gists{/gist_id}',
     'hub_url': 'https://api.github.com/hub',
     'issue_search_url': 'https://api.github.com/search/issues?q={query}{&page,per_page,sort,order}',
     'issues_url': 'https://api.github.com/issues',
     'keys_url': 'https://api.github.com/user/keys',
     'notifications_url': 'https://api.github.com/notifications',
     'organization_repositories_url': 'https://api.github.com/orgs/{org}/repos{?type,page,per_page,sort}',
     'organization_url': 'https://api.github.com/orgs/{org}',
     'public_gists_url': 'https://api.github.com/gists/public',
     'rate_limit_url': 'https://api.github.com/rate_limit',
     'repository_url': 'https://api.github.com/repos/{owner}/{repo}',
     'repository_search_url': 'https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}',
     'current_user_repositories_url': 'https://api.github.com/user/repos{?type,page,per_page,sort}',
     'starred_url': 'https://api.github.com/user/starred{/owner}{/repo}',
     'starred_gists_url': 'https://api.github.com/gists/starred',
     'team_url': 'https://api.github.com/teams',
     'user_url': 'https://api.github.com/users/{user}',
     'user_organizations_url': 'https://api.github.com/user/orgs',
     'user_repositories_url': 'https://api.github.com/users/{user}/repos{?type,page,per_page,sort}',
     'user_search_url': 'https://api.github.com/search/users?q={query}{&page,per_page,sort,order}'}



## 直接使用`await`

在ipykernel 5.0+中新增了一组魔术命令用于控制cell处理异步代码的行为,这个魔术命令为`%autoawait`
如果不带参数,则可以查看当前autoawait的状态.


```python
%autoawait
```

    IPython autoawait is `on`, and set to use `asyncio`


如果带上参数,它就可以用于设置使用的lib

+ `True/False`表示是否使用这个特性
+ `asyncio/curio/trio`表示使用哪个包做为异步的时间循环



```python
%autoawait False
```


```python
%autoawait
```

    IPython autoawait is `off`, and set to use `asyncio`



```python
%autoawait True
```


```python
%autoawait
```

    IPython autoawait is `on`, and set to use `asyncio`


### 如何使用autoawait特性

使用autoawait特性我们可以直接在cell中await 一个协程函数的调用


```python
await get_github()
```




    {'current_user_url': 'https://api.github.com/user',
     'current_user_authorizations_html_url': 'https://github.com/settings/connections/applications{/client_id}',
     'authorizations_url': 'https://api.github.com/authorizations',
     'code_search_url': 'https://api.github.com/search/code?q={query}{&page,per_page,sort,order}',
     'commit_search_url': 'https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}',
     'emails_url': 'https://api.github.com/user/emails',
     'emojis_url': 'https://api.github.com/emojis',
     'events_url': 'https://api.github.com/events',
     'feeds_url': 'https://api.github.com/feeds',
     'followers_url': 'https://api.github.com/user/followers',
     'following_url': 'https://api.github.com/user/following{/target}',
     'gists_url': 'https://api.github.com/gists{/gist_id}',
     'hub_url': 'https://api.github.com/hub',
     'issue_search_url': 'https://api.github.com/search/issues?q={query}{&page,per_page,sort,order}',
     'issues_url': 'https://api.github.com/issues',
     'keys_url': 'https://api.github.com/user/keys',
     'notifications_url': 'https://api.github.com/notifications',
     'organization_repositories_url': 'https://api.github.com/orgs/{org}/repos{?type,page,per_page,sort}',
     'organization_url': 'https://api.github.com/orgs/{org}',
     'public_gists_url': 'https://api.github.com/gists/public',
     'rate_limit_url': 'https://api.github.com/rate_limit',
     'repository_url': 'https://api.github.com/repos/{owner}/{repo}',
     'repository_search_url': 'https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}',
     'current_user_repositories_url': 'https://api.github.com/user/repos{?type,page,per_page,sort}',
     'starred_url': 'https://api.github.com/user/starred{/owner}{/repo}',
     'starred_gists_url': 'https://api.github.com/gists/starred',
     'team_url': 'https://api.github.com/teams',
     'user_url': 'https://api.github.com/users/{user}',
     'user_organizations_url': 'https://api.github.com/user/orgs',
     'user_repositories_url': 'https://api.github.com/users/{user}/repos{?type,page,per_page,sort}',
     'user_search_url': 'https://api.github.com/search/users?q={query}{&page,per_page,sort,order}'}



包括异步上下文也可以直接使用


```python
async with aiohttp.ClientSession() as session:
    response = await session.get('https://api.github.com')
    newresult = await response.json()
```


```python
newresult
```




    {'current_user_url': 'https://api.github.com/user',
     'current_user_authorizations_html_url': 'https://github.com/settings/connections/applications{/client_id}',
     'authorizations_url': 'https://api.github.com/authorizations',
     'code_search_url': 'https://api.github.com/search/code?q={query}{&page,per_page,sort,order}',
     'commit_search_url': 'https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}',
     'emails_url': 'https://api.github.com/user/emails',
     'emojis_url': 'https://api.github.com/emojis',
     'events_url': 'https://api.github.com/events',
     'feeds_url': 'https://api.github.com/feeds',
     'followers_url': 'https://api.github.com/user/followers',
     'following_url': 'https://api.github.com/user/following{/target}',
     'gists_url': 'https://api.github.com/gists{/gist_id}',
     'hub_url': 'https://api.github.com/hub',
     'issue_search_url': 'https://api.github.com/search/issues?q={query}{&page,per_page,sort,order}',
     'issues_url': 'https://api.github.com/issues',
     'keys_url': 'https://api.github.com/user/keys',
     'notifications_url': 'https://api.github.com/notifications',
     'organization_repositories_url': 'https://api.github.com/orgs/{org}/repos{?type,page,per_page,sort}',
     'organization_url': 'https://api.github.com/orgs/{org}',
     'public_gists_url': 'https://api.github.com/gists/public',
     'rate_limit_url': 'https://api.github.com/rate_limit',
     'repository_url': 'https://api.github.com/repos/{owner}/{repo}',
     'repository_search_url': 'https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}',
     'current_user_repositories_url': 'https://api.github.com/user/repos{?type,page,per_page,sort}',
     'starred_url': 'https://api.github.com/user/starred{/owner}{/repo}',
     'starred_gists_url': 'https://api.github.com/gists/starred',
     'team_url': 'https://api.github.com/teams',
     'user_url': 'https://api.github.com/users/{user}',
     'user_organizations_url': 'https://api.github.com/user/orgs',
     'user_repositories_url': 'https://api.github.com/users/{user}/repos{?type,page,per_page,sort}',
     'user_search_url': 'https://api.github.com/search/users?q={query}{&page,per_page,sort,order}'}



## 注意

连接spark常用的sparkmagic目前并不支持ipykernel 5.0+,比较推荐将包括sparkmagic在内的数据科学工具单独创建一个虚拟环境,主环境则使用ipykernel 5.0+
