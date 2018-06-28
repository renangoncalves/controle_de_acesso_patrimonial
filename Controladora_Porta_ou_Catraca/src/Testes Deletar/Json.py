Renan --- Cliente.....................

renan@mate-D530:~$ python
Python 2.7.6 (default, Jun 22 2015, 17:58:13) 
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import json
>>> import socket
>>> info = dict()
>>> info['nome'] = 'Renan'
>>> info['id'] = 123456
>>> info
{'id': 123456, 'nome': 'Renan'}
>>> print info
{'id': 123456, 'nome': 'Renan'}
>>> info_str = json.dumps(info)
>>> info_str
'{"id": 123456, "nome": "Renan"}'
>>> sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
>>> sckt.connect(("172.18.131.75", 5555))
>>> sckt.send(info_str)
31
>>> resp = sckt.recv(2)
>>> resp
'\no'
>>> resp = sckt.recv(2)
>>> resp
'k\n'
>>> resp = sckt.recv(2)
>>> resp
'OK'
>>> 








Arliones -- Servidor..........................

nc -l 5555




Arliones -- Cliente................

renan@mate-D530:~$ python
Python 2.7.6 (default, Jun 22 2015, 17:58:13) 
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import json
>>> str = '{"a":0,"b":1,"c":2}'
>>> ls = json.dumps(str)
>>> ls
'"{\\"a\\":0,\\"b\\":1,\\"c\\":2}"'
>>> ls["b"]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: string indices must be integers, not str
>>> ls["b"]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: string indices must be integers, not str
>>> ls("b")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object is not callable
>>> ls = json.loads(str)
>>> ls
{u'a': 0, u'c': 2, u'b': 1}
>>> ls[a]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'a' is not defined
>>> ls['a']
0
>>> str
'{"a":0,"b":1,"c":2}'
>>> ls = json.loads(str)
>>> ls
{u'a': 0, u'c': 2, u'b': 1}
>>> ls['nome']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'nome'
>>> ls['a']
0
>>> ls['b']
1
>>> ls['c']
2
>>> info = dict()
>>> info['nome'] = 'arliones'
>>> info['id'] = 500
>>> info
{'id': 500, 'nome': 'arliones'}
>>> print info
{'id': 500, 'nome': 'arliones'}
>>> info_str = json.dumps(info)
>>> info_str
'{"id": 500, "nome": "arliones"}'
>>> import socket
>>> sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
>>> sckt.connect(("localhost",5555))
>>> sckt.send(info_str)
31
>>> resp = sckt.recv(2)
>>> resp
'Oi'
>>> resp = sckt.recv(2)
>>> resp
'\n'
>>> resp = sckt.recv(2)
>>> resp
'io'
>>> resp = sckt.recv(2)
>>> resp
'\n'
>>> sckt.close()
>>> history
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'history' is not defined
>>> 
