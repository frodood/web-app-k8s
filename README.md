# web-app-k8s

python web-server application with in-built prometheus exporter


Requests to the application for "/homersimpson" receive a image of homersimpson as response

Requests to the application for "/covilha" receive local time in covilha as response

Requests to the application for "/metrics" receive application metrics way that prometheus understand

Following metrics are expose
- Number of requests it receives on /homersimpson and /covilha and the response status sent.
- Time spent by the server for each request.
