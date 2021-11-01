#!/usr/bin/env python
import pika
import wikipedia

#cambiar el idioma de busqueda en Wikipedia (es.wikipedia.org)
wikipedia.set_lang("es")

#realiza búsqueda en wikipedia e imprime el resumen de la pagina.

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

def resumen(texto):
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
    pag = wikipedia.page(articulo)
    return articulo[1:], pag.summary




def callback(ch, method, properties, body):
    articulo, res = resumen(body)
    print("El resumen de la pagina {} es: \n{}".format( articulo, res ))
    print(" [x] %r" % body)



channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
