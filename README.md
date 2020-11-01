# Invoice Analyzer

The project contains backend api in flask and frontend in react.js

Hosted at : https://invoice-analyzer.glitch.me/


REACT node_modules : npm install<br>
RUN : npm start<br>
BUILD : npm run build<br> 


API Call
---------

The user can access api at /api/v1?query=status


Response Validation
------------------

The app checks whether the device is connected to the internet and responds appropriately. The result of the request is validated to account for a bad server response or lack of server response.


Async Task
------------------

The network call occurs off the UI thread using an AsyncTask or similar threading object.


JSON Parsing
------------

The JSON response is parsed correctly, and relevant information is stored in the app.
