import mysql.connector
import os, time
import pika
import create_database
#import pywhatkit as rep 
import webbrowser
import re
from urllib import parse, request


print("start birthday manager...")
create_database.main()

DATABASE = "bot"

DATABASE_IP = str(os.environ['DATABASE_IP'])

DATABASE_USER = "root"
DATABASE_USER_PASSWORD = "root"
DATABASE_PORT=3306

time.sleep(10)

########### CONNEXIÓN A RABBIT MQ #######################

HOST = os.environ['RABBITMQ_HOST']
print("rabbit:"+HOST)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channel = connection.channel()

#El consumidor utiliza el exchange 'cartero'
channel.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

#Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue="birthday", exclusive=True, durable=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='cartero', queue=queue_name, routing_key="birthday")


##########################################################


########## ESPERA Y HACE ALGO CUANDO RECIBE UN MENSAJE ####

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
	print(body.decode("UTF-8"))
	arguments = body.decode("UTF-8").split(" ")

	if (arguments[0]=="!birthday"):

		person = arguments[1]
		print(person)
		db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,port=DATABASE_PORT, password=DATABASE_USER_PASSWORD)
		cursor = db_connection.cursor()
		cursor.execute(f"USE {DATABASE}")
		cursor.execute(f'''SELECT member,date FROM birthday WHERE member="{person}";''')
		
		for (member, date) in cursor:
			result="{} nació el {:%d %b %Y}".format(member,date)
			print(result)

			########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
			print("send a new message to rabbitmq: "+result)
			channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=result)

	elif (arguments[0]=="!add-birthday"):

		person = arguments[1]
		print(person)
		birthday = arguments[2]
		db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,port=DATABASE_PORT, password=DATABASE_USER_PASSWORD)
		cursor = db_connection.cursor()
		cursor.execute(f"USE {DATABASE}")
		cursor.execute(f'''INSERT INTO birthday(member,date) VALUES("{person}","{birthday}");''')
		cursor.execute(f'''COMMIT;''')


	elif (arguments[0]=="!busca"):
		search = " ".join(arguments[1:])
		
		#url_busqueda = "https://www.youtube.com/results?search_query="+busqueda.replace(" ","+")
		
		query_string = parse.urlencode({'search_query':search})
		html_content = request.urlopen('http://www.youtube.com/results?'+query_string)
		search_results=re.findall('watch\?v=(.{11})',html_content.read().decode('utf-8'))
		url_video = "https://www.youtube.com/watch?v="+search_results[0]
		channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=url_video)

#sudo kill `sudo lsof -t -i:5672`
		

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()



#######################