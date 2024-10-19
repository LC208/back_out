import requests

r = requests.post("http://127.0.0.1:8000/api/out/base/user/info", {'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5MzE2MTc0LCJpYXQiOjE3MjkzMTI1NzQsImp0aSI6ImI5NzZlZGJhMjcxYjRlNzY4NDY2NmU2NzVhMzY3ZDQ2IiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJiYWNrIn0.KtlP_4t1EuCDgZBGDm74Y72zVEN2s8MfhqsQ2XsE3ao'})
print(r.data)