import json

def lambda_handler(event, context):
    query = event.get("queryStringParameters") or {}
    name = query.get("name", "world")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": f"Hello, {name}!"})
    }
