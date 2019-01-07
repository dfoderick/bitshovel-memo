#naive implement memo.cash op_return protocol
#see https://memo.cash/protocol
#example: redis-cli publish memo.send <action> <value>
#redis-cli publish memo.send "Hello from BitShovel"
import sys
import redis

RED = redis.Redis(host="127.0.0.1", port="6379")
BUS = RED.pubsub()

def main():
    #listen for anyone who wants to send to memo
    memo_send = BUS.subscribe("memo.send")
    for event in BUS.listen():
         process_event(event)

def process_event(event):
    try:
        if event["type"] == "message" :
            process_message(event["data"])
        if event["type"] == "subscribe":
            print('subscribed to {}'.format(event["channel"]))
    except Exception as ex:
        print(ex)

def process_message(data):
    remainder = data
    #default action is to post the data
    prefix = "0x6d02"
    command = "post"
    if " " in data:
        parsed = data.split(' ',1)
        command = parsed[0].lower()
        if len(parsed) > 1:
            remainder = parsed[1]
        if command == "setname":
            prefix = "0x6d01"
        elif command == "post":
            prefix = "0x6d02"
        elif command == "posttopic":
            prefix = "0x6d0c"
        else:
            #no matches so dont eat the first word
            remainder = data
    send(command, prefix, remainder)

def send(command, prefix, remainder):
    op_stuff = '{0} "{1}"'.format(prefix, remainder).lstrip()
    RED.publish("bitshovel.send", op_stuff)
    print('Send to BitShovel > {}'.format(op_stuff))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Shutting down...')
        BUS.unsubscribe()
        sys.exit()
