import requests
import json

def demonstrate_on_website(url):
    #sends get and post requests to a website.
    print(f"1. Testing on a website: {url}")
    
    # get request on website
    print("\n[GET Request]")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        # check if the request was successful
        if response.ok:
            print("webpage fetched successfully.")
            print("Response body:")
            print(response.text[:300]) #.text is for html content
        else:
            print("Failed to fetch the webpage.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    #  post request on website
    print("\n[POST Request]")
    try:
        # we are sending data, but the server isn't expecting it at this url
        post_data = {'name': 'test'}
        response = requests.post(url, json=post_data)
        print(f"Status Code: {response.status_code}")
        
        # likely be an error code
        if not response.ok:
            print("the POST request was not successful.")
            print("Server Response (if any):")
            print(response.text[:300])
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def demonstrate_on_api(url):
    #Sends GET and POST requests to a test API.
    print(f"\n2. Testing on a Test API: {url}")
    
    # GET Request on API
    print("\n[GET Request]")
    try:
        # requesting
        response = requests.get(f"{url}/posts/1")
        print(f"Status Code: {response.status_code}")
        if response.ok:
            print("Successfully fetched API data.")
            print("Response Body (JSON):")
            print(json.dumps(response.json(), indent=2))# .json() decodes the JSON into a Python dictionary
        else:
            print("Failed to fetch API data.")
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    # POST Request on API
    print("\n[POST Request]")
    try:
        post_data = {
            'title': 'My New Post',
            'body': 'This is for my CN Lab.',
            'userId': 1
        }
        response = requests.post(f"{url}/posts", json=post_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201: # 201 Created is the specific success code for POST
            print("Successfully created a new resource on the API.")
            print("Response Body (JSON from server):")
            print(json.dumps(response.json(), indent=2))
        else:
            print("POST request to API failed.")
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    website_url = "https://www.google.com"
    api_url = "https://jsonplaceholder.typicode.com"
    
    demonstrate_on_website(website_url)
    print("\n" + "\n")
    demonstrate_on_api(api_url)