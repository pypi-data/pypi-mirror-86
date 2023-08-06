# okws

通过 `redis` 提供 `okex websocket` 服务数据。它将 `okex websocket` 发过来的数据缓存在 `redis` 中, 程序随时提取。

可以以两种方式使用:

1. 做为独立服务：
   安装后，运行 `python -m okws.server` 启动服务。
   也可以用 `python -m okws.server -c <configfile>` 启动, 并在配置文件中设置需要连接到 `okex websocket` 的参数，当然也可以在自己的应用中直接发送命令到 `okws`（详情见 `api`）。

配置文件示例如下：

```ini
[test]
apiKey=
secret=
password=
commands =
    {"op": "subscribe", "args": ["spot/ticker:ETH-USDT"]}
    {"op": "subscribe", "args": ["spot/candle60s:ETH-USDT"]}

[ok2]
apiKey=
secret=8C52F
password=
```   
以上的配置，会让 okws 启动后，自动连接两个 websocket ， 分别命名为 test, ok2, 连接上 test 后，还会执行 commands 中的命令，即订阅 ETH-USDT 的 ticker 数据和一分钟的 K 线数据。


2. 内嵌到自己的程序中：

```python
from okws.server import run
from okws.client import create_client
import asyncio

async def client():
    okex = await create_client()
    ret = await okex.subscribe('tests', "spot/ticker:ETH-USDT")
    
    # 等待服务器完成订阅和接收 ticker 数据
    await asyncio.sleep(2)
    ret = await okex.get('tests', "spot/ticker", {"instrument_id": "ETH-USDT"})
    print(ret)
    
    # okws 退出
    await okex.server_quit()
    # 关闭客户端
    await okex.close()
    await asyncio.sleep(1)
   
async def test_server():
    await asyncio.gather(
        run(),
        client()
    )


if __name__ == '__main__':
    asyncio.run(test_server())
   
```


## 安装

1. 安装 redis
    * ubuntu: 
    
      `sudo apt-get install redis`
    
    * macOS: 
    
       `brew install redis`    

2. 安装 okws 包

    `pip install okws`

## 使用示例

1. 启动服务

`python -m okws.server`
`python -m okws.server -c 配置文件`

2. 使用示例

```python
import asyncio
import logging
from okws.client import create_client

logger = logging.getLogger(__name__)

okex = await create_client()
ret = await okex.open_ws('tests',{'apiKey':'','secret':'','password':''})  # 连接到 okex websockets
logger.info(ret)

# 等待 tests 连接完成
await asyncio.sleep(10)
ret = await okex.subscribe('tests', "spot/ticker:ETH-USDT")
await asyncio.sleep(1)
ret = await okex.get('tests', "spot/ticker", {"instrument_id": "ETH-USDT"})
logger.info(ret)
```

## 客户端 `api`

提供了一个简单的客户端用以返问 `redis` 的数据，用户也可以自己直接从 `redis` 中获取。
 `create_client` 返回的类有以下几个函数：

1. `open_ws(name, auth_params={})`

    连接到 okex websocket 并命名为 name

2. `close_ws(name)`

    关闭 okex websocket 连接

3. `subscribe(name, path)`

    订阅 websocket 数据，如：`subscribe('tests', "spot/ticker:ETH-USDT")`

4. `get(name, path, params={})`

    取得 ws 数据 如：`get('tests', "spot/ticker", {"instrument_id": "ETH-USDT"})`

5. `servers()`

    取得可用的 okex websocket 连接

6. `redis_clear(self, path="okex/*")`
    
    清除 redis 上的缓存数据

7. 如果要在 websocket 发送数据时获得通知，可以使用 redis 订阅

    * redis 的 key 为 "okex/name/频道名"
    * 如果 websocket 返回的是 event, redis 的 key 为 "okex/name/event"
 
 
## 测试

export oktest='{"apiKey": "", "secret": "", "password": ""}'

运行 `pytest`

<!--
;## install for dev
;`$ pip install -e .  # 或者 python setup.py develop`
-->
