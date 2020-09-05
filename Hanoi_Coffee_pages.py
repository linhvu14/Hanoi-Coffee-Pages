import requests
import json
import configparser

config = configparser.ConfigParser()
config.read("token.ini")
token = config["Authentication"]["token"]


def get_page(keyword):
    ses = requests.session()
    resp = ses.get(
        "https://graph.facebook.com/search?type=place&q={}&center=21.027875, 105.853654&distance=1000&fields=id,name,location,link&access_token={}".format(
            keyword, token
        )
    )
    places = resp.json()
    places_result = {"type": "FeatureCollection", "features": []}
    for info_place in places["data"]:
        lat = info_place["location"]["latitude"]
        lng = info_place["location"]["longitude"]
        data = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lng, lat]},
            "properties": {
                "id": info_place["id"],
                "name": info_place["name"],
                "link": info_place["link"],
            },
        }
        places_result["features"].append(data)
    with open("hanoi_coffee.geojson", "wt", encoding="utf-8") as f:
        json.dump(places_result, f, ensure_ascii=False, indent=4)


def main():
    get_page("coffee")
    print("See results at: https://github.com/linhvu14/Hanoi-Coffee-Pages")


if __name__ == "__main__":
    main()
