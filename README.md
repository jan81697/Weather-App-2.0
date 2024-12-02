This Code is a for a weather site using openweathermap.org. <br>
You'll need a API key from there to use. <br>
Also Use HTML so be formiliar with that. <br>
<br>
Communication contract; I'll link to this repository along with communicating changes I make over discord<br>
<br>
REQUESTING DATA<br>
1. Send a GET request to the `/get_image` endpoint with the description<br>
   parameter, which contains the weather description (such as "clear", "rain", <br>
   "snow", "sunny", etc.)
2. Parse the response which will be a JSON object containing the `image_url`, which<br>
   is the URL of the weather image<br>
EXAMPLE REQUEST<br>

```
weather = "Heavy Snowfall"
response = requests.get('http://126.0.0.1:5001/get_image, params={'description': weather.lower()})

if response.status_code == 200:
    data = response.json()
    image_url = data['image_url']
```

<br>
RECIEVING DATA<br>
1. Parse the JSON response. After getting the GET request, the server will respond <br> with a JSON object. You can access the `image_url` field, which is the URl for the image
2. Use the `image_url` which displays the image on a webpage<br>
EXAMPLE REQUEST<br>

```
# response will look like this in the JSON 
{
    "image_url": "http://127.0.0.1:5001/static/images/snow.png"
}

if response.status_code == 200:
    data = response.json()
    image_url = data['image_url']
```
<br>

![scratch pepah jpeg](https://github.com/user-attachments/assets/136b0799-bbb5-4ce1-b936-c8b8fb97c269)


