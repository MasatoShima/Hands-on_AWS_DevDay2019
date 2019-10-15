from chalice import Chalice
from chalice import Response
from chalice import CORSConfig
from chalice import BadRequestError
from chalice import Rate
from datetime import datetime


app = Chalice(app_name="chalice-hands-on-helloworld")
app.debug = True

CITIES_TO_STATE = {
    "seattle": "WA",
    "portland": "OR",
}

cors_config = CORSConfig(
    allow_origin="https://foo.example.com",
    allow_headers=["X-Special-Header"],
    max_age=600,
    expose_headers=["X-Special-Header"],
    allow_credentials=True
)


@app.route('/')
def index():
    return {"chalice": "hands-on"}


@app.route("/cities/{city}")
def state_of_city(city):
    try:
        city = CITIES_TO_STATE[city]

        return Response(
            body=city,
            status_code=200,
            headers={
                "Content-Type": "text/plain"
            }
        )

    except KeyError:
        raise BadRequestError(
            f"Unknown city '{city}', valid choices are: {', '.join(CITIES_TO_STATE.keys())}"
        )


@app.route("/resource/{value}", methods=["PUT"])
def put_test(value):
    return {"value": value}


# 下の method (myview_post, myview_put) と競合するため, コメントアウト
# @app.route("/myview", methods=["POST", "PUT"])
# def myview():
#     return {"message": "Hello!"}


@app.route("/myview", methods=["POST"])
def myview_post():
    return {"message": "Method is POST"}


@app.route("/myview", methods=["PUT"])
def myview_put():
    return {"message": "Method is PUT"}


@app.route("/introspect")
def introspect():
    return app.current_request.to_dict()


@app.route("/supports-cors", methods=["PUT"], cors=True)
def supports_cors():
    return {}


@app.route("/custom_cors", methods=["GET"], cors=cors_config)
def supports_custom_cors():
    return {'cors': True}


@app.schedule(Rate(1, unit=Rate.MINUTES))
def periodic_task(event):
    launch_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # CloudWatch Logs にログを出力
    print(f"function_launched: {launch_time}")

    return {"function_launched": launch_time}


@app.route("/apikey-needed", methods=["GET"], api_key_required=True)
def apikey_needed():
    return {"Key": True}

# End
