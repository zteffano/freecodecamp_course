import pika, sys, os, time 
from pymongo import MongoClient
import gridfs
from convert import to_mp3 

def main():
    client = MongoClient("host.minikube.internal",27017)
    db_videos = client.videos
    db_mp3s = client.mp3s 

    # gridfs
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    #rabbitmq connection
    connection = pika.BlockingConnection(
        pika.ConnectionParamenters(host="rabbitmq") # Da vores service name er rabbitmq
    )

    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)

        if err:
            ch.basic_nack(delievery_tag=method.delievery_tag)
        else:
            ch.basic_ack(delievery_tag=method.delievery_tag)

    

    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"),
        on_message_callback=callback

    )

    print("Waiting for messages. To exit press CTRL + C")

    channel.start_consuming()

if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)