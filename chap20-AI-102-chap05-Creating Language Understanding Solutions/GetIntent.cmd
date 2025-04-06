@echo off

rem Set values for your Language Understanding app
set app_id=2bc90f31-0593-4fa9-a655-11125d438445
set endpoint=https://azluis1688.cognitiveservices.azure.com
set key=a587e04a00d84a64bd6c038371bde2a4

rem Get parameter and encode spaces for URL
set input=%1
set query=%input: =+%

rem Use cURL to call the REST API
curl -X GET "%endpoint%/luis/prediction/v3.0/apps/%app_id%/slots/production/predict?subscription-key=%key%&log=true&query=%query%"