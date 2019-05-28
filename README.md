# selenium-ticket

Selenium で LINE チケットを 取る

# 実行方法

## `pipenv`を利用した方法

.env.sampleをコピーし.envファイルを作成する

``` console
$ pipenv sync
$ pipenv run main
```

## `venv`を利用した方法

.env.sampleをコピーし.envファイルを作成する

``` console
$ python3 -m venv venv
$ ./venv/bin/python -m pip install -r requirements.txt
$ ./venv/bin/python main.py
```
