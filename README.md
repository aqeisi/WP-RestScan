# WP-RestScan
Scan Wordpress Servers for Access Control Issues

## Just Another Wordpress Tool?
Unlike most tools that look for unpatched plugins and scans for newly released CVE's, WP-RestScan scans your wordpress blog for access control issues that might allow unauthenticated users to perform actions on behalf of the administrators. It relies on the default/plugin Wordpress REST API endpoints.

## Installation

```git clone https://github.com/aqeisi/WP-RestScan```

```pip3 install -r requirements.txt```

## Usage

```python3 WP-RestScan.py --help```

![image](https://user-images.githubusercontent.com/84850150/203375773-b6380f4f-64ca-4e83-9a41-707349e210ef.png)

``` --url -> Wordpress blog url ending with the wordpress root```

``` --oob -> Fills every 'url' parameter in the fetched endpoints with your provided out of band URL e.g. burp collaborator/webhook.site```

``` --media -> Only check for issues in media/images endpoints```

``` --users -> Only check for issues in user endpoints```

``` --posts -> Only check for issues in post endpoints```

## Example issues that can be detected:
- Delete any/all wordpress users/posts/images on the website from an unauthenticated user.
- Create a new post on behalf of an administrator.
- SSRF via well known plugin endpoints.

![image](https://user-images.githubusercontent.com/84850150/203382120-ac7b934a-f123-416e-af98-7696c3dd1ce1.png)


