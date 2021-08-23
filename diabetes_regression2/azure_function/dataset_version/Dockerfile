# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:3.0-python3.7-appservice
FROM mcr.microsoft.com/azure-functions/python:3.0-python3.7

RUN wget https://packages.microsoft.com/config/debian/10/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
RUN dpkg -i packages-microsoft-prod.deb
RUN apt-get install -y dotnet-runtime-2.1

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

RUN python -m pip install --upgrade pip

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot