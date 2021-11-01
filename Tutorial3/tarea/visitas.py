#!/usr/bin/env python
import pika
import pageviewapi.period

#devuelve el número de visitas en la pagina.

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#El consumidor utiliza el exchange 'log'
channel.exchange_declare(exchange='logs', exchange_type='fanout')

#Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def separador(texto):
    texto = str(texto)[2:(len(str(texto))-1)]
    articulo = ""
    par = 0
    for i in texto:

        if (i=='('):
            par+=1
        elif (i==')'):
            par-=1
        if (par>0):
            articulo+=i    
    return articulo[1:]
def npaginas(body):
    articulo = separador(body)
    return pageviewapi.period.sum_last('es.wikipedia', articulo,last=30, access='all-access', agent='all-agents'),articulo
def callback(ch, method, properties, body):
    n,articulo = npaginas(body)
    print('El numero de visitas a la pagina {} en es.Wikipedia.org es: {}'.format(articulo, n))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
