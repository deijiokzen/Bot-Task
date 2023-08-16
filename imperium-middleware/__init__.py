import logging
import azure.functions as func
import requests
import datetime 
import calendar
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    o_id =  req.params.get('o_id')
    if not o_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            o_id = req_body.get('o_id')

    if o_id:
        url = "https://orderstatusapi-dot-organization-project-311520.uc.r.appspot.com/api/getOrderStatus"
        data = {
            "orderId": o_id
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            response_json = response.json()
            
            shipment_date_str = response_json["shipmentDate"]
            shipment_date = datetime.datetime.strptime(shipment_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

            day_of_week = calendar.day_name[shipment_date.weekday()]
            month_name = shipment_date.strftime("%B")
            day_of_month = shipment_date.day
            year = shipment_date.year

            formatted_date = f"{day_of_week}, {day_of_month} {month_name} {year}"
   
            
            response_data = {
                "fulfillmentText": "The " + o_id + " you have provided will be shipped on " + formatted_date
            }
            response_json = json.dumps(response_data)
            return func.HttpResponse(response_json, mimetype="application/json", status_code=200)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a prompt in the query string or in the request body for a personalized response.",
             status_code=200
        )
