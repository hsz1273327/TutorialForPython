
# 使用http客户端获取数据

python自带一个http客户端,但接口不友好,主流的http客户端有:

+ [requests](https://github.com/kennethreitz/requests),最知名的python http客户端,是阻塞的.

+ [aiohttp](https://github.com/aio-libs/aiohttp),最知名的python异步http客户端

+ [requests-async](https://github.com/encode/requests-async)或[http3](https://github.com/encode/http3),requests的异步版本,接口更加友好


通常http协议获取的数据形式是两种:

+ html文件,这种我们可以使用[lxml](https://github.com/lxml/lxml)或者[pyquery](https://github.com/gawel/pyquery),通常爬虫技术就是依赖于这个
+ json文件,这种一般是企业或者组织提供的[RESTful接口服务](http://blog.hszofficial.site/recommend/2019/03/14/RESTful%E9%A3%8E%E6%A0%BC%E7%9A%84%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1/),我们直接使用标准库json就可以解析成字典.

## 使用requests


```python
import requests
```


```python
rep =requests.get("https://api.github.com")
rep.status_code
```




    200




```python
rep.json()
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



## 使用aiohttp


```python
import aiohttp
```


```python
async with aiohttp.ClientSession() as session:
    async with session.get('https://api.github.com') as resp:
        print(resp.status)
        print(await resp.json())
```

    200
    {'current_user_url': 'https://api.github.com/user', 'current_user_authorizations_html_url': 'https://github.com/settings/connections/applications{/client_id}', 'authorizations_url': 'https://api.github.com/authorizations', 'code_search_url': 'https://api.github.com/search/code?q={query}{&page,per_page,sort,order}', 'commit_search_url': 'https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}', 'emails_url': 'https://api.github.com/user/emails', 'emojis_url': 'https://api.github.com/emojis', 'events_url': 'https://api.github.com/events', 'feeds_url': 'https://api.github.com/feeds', 'followers_url': 'https://api.github.com/user/followers', 'following_url': 'https://api.github.com/user/following{/target}', 'gists_url': 'https://api.github.com/gists{/gist_id}', 'hub_url': 'https://api.github.com/hub', 'issue_search_url': 'https://api.github.com/search/issues?q={query}{&page,per_page,sort,order}', 'issues_url': 'https://api.github.com/issues', 'keys_url': 'https://api.github.com/user/keys', 'notifications_url': 'https://api.github.com/notifications', 'organization_repositories_url': 'https://api.github.com/orgs/{org}/repos{?type,page,per_page,sort}', 'organization_url': 'https://api.github.com/orgs/{org}', 'public_gists_url': 'https://api.github.com/gists/public', 'rate_limit_url': 'https://api.github.com/rate_limit', 'repository_url': 'https://api.github.com/repos/{owner}/{repo}', 'repository_search_url': 'https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}', 'current_user_repositories_url': 'https://api.github.com/user/repos{?type,page,per_page,sort}', 'starred_url': 'https://api.github.com/user/starred{/owner}{/repo}', 'starred_gists_url': 'https://api.github.com/gists/starred', 'team_url': 'https://api.github.com/teams', 'user_url': 'https://api.github.com/users/{user}', 'user_organizations_url': 'https://api.github.com/user/orgs', 'user_repositories_url': 'https://api.github.com/users/{user}/repos{?type,page,per_page,sort}', 'user_search_url': 'https://api.github.com/search/users?q={query}{&page,per_page,sort,order}'}


## 使用requests-async


```python
import requests_async as requests
response = await requests.get('https://api.github.com')
print(response.status_code)
print(response.json())
```

    200
    {'current_user_url': 'https://api.github.com/user', 'current_user_authorizations_html_url': 'https://github.com/settings/connections/applications{/client_id}', 'authorizations_url': 'https://api.github.com/authorizations', 'code_search_url': 'https://api.github.com/search/code?q={query}{&page,per_page,sort,order}', 'commit_search_url': 'https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}', 'emails_url': 'https://api.github.com/user/emails', 'emojis_url': 'https://api.github.com/emojis', 'events_url': 'https://api.github.com/events', 'feeds_url': 'https://api.github.com/feeds', 'followers_url': 'https://api.github.com/user/followers', 'following_url': 'https://api.github.com/user/following{/target}', 'gists_url': 'https://api.github.com/gists{/gist_id}', 'hub_url': 'https://api.github.com/hub', 'issue_search_url': 'https://api.github.com/search/issues?q={query}{&page,per_page,sort,order}', 'issues_url': 'https://api.github.com/issues', 'keys_url': 'https://api.github.com/user/keys', 'notifications_url': 'https://api.github.com/notifications', 'organization_repositories_url': 'https://api.github.com/orgs/{org}/repos{?type,page,per_page,sort}', 'organization_url': 'https://api.github.com/orgs/{org}', 'public_gists_url': 'https://api.github.com/gists/public', 'rate_limit_url': 'https://api.github.com/rate_limit', 'repository_url': 'https://api.github.com/repos/{owner}/{repo}', 'repository_search_url': 'https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}', 'current_user_repositories_url': 'https://api.github.com/user/repos{?type,page,per_page,sort}', 'starred_url': 'https://api.github.com/user/starred{/owner}{/repo}', 'starred_gists_url': 'https://api.github.com/gists/starred', 'team_url': 'https://api.github.com/teams', 'user_url': 'https://api.github.com/users/{user}', 'user_organizations_url': 'https://api.github.com/user/orgs', 'user_repositories_url': 'https://api.github.com/users/{user}/repos{?type,page,per_page,sort}', 'user_search_url': 'https://api.github.com/search/users?q={query}{&page,per_page,sort,order}'}



```python

```
