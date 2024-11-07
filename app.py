from flask import Flask, render_template, request
import json
import urllib.request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def details():
    if request.method == 'POST':
        location = request.form.get("location")
        api_key = 'AQwhmdsNoAXIAMKQY6lWSTNt_2Gg5rgc63hYO4_hBps'

        try:
            # Construct API URL with the location input
            url = f'https://geocode.search.hereapi.com/v1/geocode?apikey={api_key}&q={location}'
            source = urllib.request.urlopen(url).read()

            # Print the raw API response for debugging
            print(f"API Response (raw): {source}")

            # Parse the JSON response
            responseData = json.loads(source)

            # Check if 'items' exist in the response and there are results for the location
            if 'items' in responseData and len(responseData['items']) > 0:
                # Extract latitude and longitude from the response
                data = {
                    "latitude": str(responseData['items'][0]['position']['lat']),
                    "longitude": str(responseData['items'][0]['position']['lng']),
                }
                return render_template('index.html', data=data, apikey=api_key)
            else:
                # No valid location found in the API response
                return render_template('index.html', error="Invalid location. Please enter a correct one.")

        except Exception as e:
            # Print the exception for debugging
            print(f"Error: {e}")
            return render_template('index.html', error="Something went wrong. Please try again.")

    # Render the default form on GET request
    return render_template('index.html')

# Running the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
