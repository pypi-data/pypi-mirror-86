# Objective

This library creates a python wrapper over Konker API to allow easier usage and integration 
with Konker REST API

# Sample Usage

from pykonker.main.api import Client

konker = Client()
konker.login(username='', password='')
applications = konker.getApplications()
devices = konker.getAllDevicesForApplication('default')
data = konker.readData(guid=devices[0]['guid'])

# Change and publish the library on PyPi

make shell 
make pylint  
* NOTE: solve problems identified by lint process .. after that it will generate the module to be published
make upload

after that, the module will be available on pip 


pip install pykonker

or 

pip install --upgrade pykonker 


# References

https://www.konkerlabs.com/developers/developers-en.html
https://konker.atlassian.net/wiki/spaces/DEV/pages/28180518/Guia+de+Uso+da+Plataforma+Konker
https://api.demo.konkerlabs.net/v1/swagger-ui.html
