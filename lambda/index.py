import json

def _resp(status, payload):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(payload),
    }

def lambda_handler(event, context):
    method = event.get("httpMethod", "")
    path = event.get("path", "")

    qs = event.get("queryStringParameters") or {}
    name = qs.get("name", "world")

    if path != "/hello":
        return _resp(404, {"error": "Not found", "path": path})

    if method == "GET":
        return _resp(200, {"message": f"Hello, {name}!"})

    if method == "POST":
        body_raw = event.get("body") or ""
        try:
            body = json.loads(body_raw) if body_raw else {}
        except json.JSONDecodeError:
            body = {"raw": body_raw}
        return _resp(200, {"message": f"Created for {name}", "received": body})

    if method == "DELETE":
        return _resp(200, {"message": f"Deleted {name}"})

    return _resp(405, {"error": "Method not allowed", "method": method})
