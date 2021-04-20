import requests

def nutrition(food):
    payload = {
        "appId": 'e4d96968',
        "appKey": '4c9e97e39eafccbbf4d2fe28d3deec81',
        "fields": [
            "item_name",
            "nf_calories",
            "nf_sodium",
        ],
        "min_score": 0.5,
        "offset": 0,
        "limit": 1,
        "query": food,
    }
    res = requests.post('https://api.nutritionix.com/v1_1/search', data=payload)
    res = res.json()
    response = {
        "name": res["hits"][0]["fields"]["item_name"],
        "calories": res["hits"][0]["fields"]["nf_calories"],
        "sodium": res["hits"][0]["fields"]["nf_sodium"],
    }
    return(response)

# response format below
''' {
    "total":8196,"max_score":5.602788,
    "hits":[
        {
        "_index":"f762ef22-e660-434f-9071-a10ea6691c27",
        "_type":"item","_id":"57cd18543f8b952b70e36da6",
        "_score":5.602788,
        "fields":{
            "item_name":"Pork Pie",
            "nf_calories":373.55,
            "nf_sodium":528
            }
        }
    ]
}'''