# FwR-jmxquery

Automatischen Testen via JMX ausgaben im Fahrwegrechner




## How to install

For pip dependencies:
```shell
pip install -r requirements.txt
```

### jmxquery

```shell
git clone https://github.com/kisstibor/JMXQuery
cd JMXQuery/python
git checkout jmx_method_invokation
pip install .
```

Add a file called 'passwords' containing the connection detail for the JMXConnection:
```shell
connection-uri
username
password
```
example:
```shell
service:jmx:rmi:///jndi/rmi://rcsxaver:5555/something
admin
a-very-good-password
```