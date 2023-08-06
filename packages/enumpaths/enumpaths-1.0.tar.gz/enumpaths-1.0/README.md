# enumpaths
Simple standalone Python tool that takes a host argument and file of URL paths, iterates through the URLs sending a proxied GET request (for Burp Suite).

**Why?**

*Speed up your pentesting workflow* but mostly because I kept running into this issue where I would have a list of paths & a target but wanted to see the requests/responses in Burp Suite.

**Repo**
- https://github.com/0xBruno/enumpaths/

**Usage:**

- Use pipx to use as standalone tool. Otherwise you will have to do `python3 -m enumpaths`.

- `$ enumpaths https://your.target paths.txt`

or 

- `$ cat paths | enumpaths https://your.target -`

>*With gobuster output, -n is necessary so you do not include status codes.*

`--help` if you get confused

**Default settings:**
- Proxy -> localhost:8080
- User-Agent -> Tesla carbrowser

**Example:**

Link: https://github.com/0xBruno/enumpaths/blob/main/example.PNG

![Example](https://github.com/0xBruno/enumpaths/blob/main/example.PNG)


**I want to know more:**

Its like 10 lines of code. Just read it.

There's probably a better tool somewhere out there or a flag for an existing tool. Cool. Let me know.
