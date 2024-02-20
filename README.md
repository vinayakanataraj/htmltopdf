This Python Web app allows you to programatically convert HTML code into base64 via HTTP requests.

This is an app hosted on a Flask web server which takes html code as input and converts it into base64 code and gives the output in JSON format.
The base64 output code can be fed into a printing API or directly to a printer, if available to print the contents of the html code while retaining its source formatting.

The following arguments can be passed via URL parameters in order to specifiy printing specification:

```page_size, margin_top, margin_right, margin_bottom, margin_left```

The actual html code needs to be passed to the body of the HTTP request that is being sent to this Flask server.


Example usage:
```
curl --location 'https://vinayakasmallbay.pythonanywhere.com/convert_to_pdf?page_size=A4' \
--header 'Content-Type: application/json' \
--data '<html>
<body>Your
multi-line
HTML content
here</body>
</html>'
```



