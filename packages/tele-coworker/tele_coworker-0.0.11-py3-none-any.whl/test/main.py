from time import sleep

from kazoo.client import KazooClient

zk = KazooClient()
zk.start()

zk.ensure_path("/test")


@zk.ChildrenWatch("/test", send_event=True)
def foo(children, event):
    print(f"Children are now: {children}, event: {event}")


@zk.DataWatch("/test")
def bar(data, stat, event):
    print("Data is %s" % data)
    print("Version is %s" % stat.version)
    # print("Event is %s" % event)
    print(f"hzn debug ==> {stat}")


while True:
    sleep(1)
