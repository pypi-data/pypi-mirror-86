# tinyXMPP

tinyXMPP is a small XMPP client for Python applications. It allows developer to easily connect to XMPP servers and exchange messages in a fast and secure way.

## Getting Started

```
pip install tinyxmpp
```

To connect to an XMPP server:

```python
from tinyxmpp import XMPPClient

async def main():
    client = XMPPClient(jid='stan@finetuned.nl/python',
                        password='P0ivQWSLXXg8l23YicdT')
    client.on_message = on_message
    client.on_iq = on_iq
    client.on_presence = on_presence
    await client.connect(host_addr='finetuned.nl')
    await client.send_message(to='stan@finetuned.nl/Desktop van Stan',
                              message='Hello There')

async def on_message(message):
    print(message)

async def on_presence(element):
    print(element)

async def on_iq(element):
    print(element)

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()

```

## License

This project is made available under the Apache 2.0 License.

## Contruibu