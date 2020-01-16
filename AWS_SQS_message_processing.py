import boto3

client = boto3.client('sqs')

client.create_queue(QueueName='test_queue')
# get a list of queues, we get back a dict with 'QueueUrls' as a key with a list of queue URLs
queues = client.list_queues(QueueNamePrefix='test_queue') # we filter to narrow down the list
test_queue_url = queues['QueueUrls'][0]
# send 100 messages to this queue
for i in range(0,100):
    # we set a simple message body for each message
    # for FIFO queues, a 'MessageGroupId' is required, which is a 128 char alphanumeric string
    enqueue_response = client.send_message(QueueUrl=test_queue_url, MessageBody='This is test message #'+str(i))
    # the response contains MD5 of the body, a message Id, MD5 of message attributes, and a sequence number (for FIFO queues)
    print('Message ID : ',enqueue_response['MessageId'])

while True:
    messages = client.receive_message(QueueUrl=test_queue_url,MaxNumberOfMessages=10) # adjust MaxNumberOfMessages if needed
    if 'Messages' in messages: # when the queue is exhausted, the response dict contains no 'Messages' key
        for message in messages['Messages']: # 'Messages' is a list
            # process the messages
            print(message['Body'])
            # next, we delete the message from the queue so no one else will process it again
            client.delete_message(QueueUrl=test_queue_url,ReceiptHandle=message['ReceiptHandle'])
    else:
        print('Queue is now empty')
        break
