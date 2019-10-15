from chalice import Chalice
import boto3
from botocore.client import Config

BUCKET_NAME = "chalice-handson-masato-shima-20191003"

S3 = boto3.client("s3", config=Config(s3={"addressing_style": "path"}))

app = Chalice(app_name="chalice-hands-on-s3upload")


@app.route(
    "/upload_via_api",
    methods=["PUT"],
    content_types=["application/octet-stream"]
)
def upload_via_api():
    # 今回はシンプルに S3 上のオブジェクト名を固定します
    key = 'uploaded_via_api'

    # クライアントからのリクエストボディ
    body = app.current_request.raw_body

    result = S3.put_object(
        Body=body,
        Bucket=BUCKET_NAME,
        Key=key
    )

    return {"result": result}


@app.route("/presigned_url", methods=["GET"])
def presigned_url():
    # シンプルにするためオブジェクト名は固定します
    key = "uploaded_by_client"

    # 10分間有効な署名付き URL を生成
    expires_in = 600

    url = S3.generate_presigned_url(
        ClientMethod="put_object",

        Params={
            "Bucket": BUCKET_NAME,
            "Key": key,
            "ContentType": "application/octet-stream"
        },
        ExpiresIn=expires_in,
        HttpMethod="PUT"
    )

    return {
        "presigned_url": url,
        "expires_in": expires_in
    }

# End
