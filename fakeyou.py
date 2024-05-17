from json import JSONDecodeError
from time import sleep
from uuid import uuid4

from requests import Session, Response

# ERROR_TYPES = {
#     401: UnAuthorized,
#     429: TooManyRequests,
#
#     "InvalidCredentials": InvalidCredentials,
#     "UsernameReserved": UsernameTaken,
#     "UsernameTaken": UsernameTaken,
#     "EmailTaken": EmailTaken,
#     "server error": ServerError,
#     "not found": NotFount
# }

ERROR_TYPES = {
    401: Exception,
    429: Exception,

    "InvalidCredentials": Exception,
    "UsernameReserved": Exception,
    "UsernameTaken": Exception,
    "EmailTaken": Exception,
    "server error": Exception,
    "not found": Exception
}

def handle_exception(response):
    request_error_code = ERROR_TYPES.get(response.status_code)

    try:
        body = response.json()
    except JSONDecodeError:
        body = {"error": response.text}

    if request_error_code:
        raise request_error_code(body)

    if not body.get("success"):
        error_type = body.get("error_type", body.get("error_reason"))

        raise ERROR_TYPES.get(
            error_type, Exception
        )(
            body.get("error_message", body.get("error", error_type))
        )


def handle_response(response):
    return response if response.status_code < 300 else handle_exception(response)


class Service:
    def __init__(self, proxies: dict = None):
        self.api = "https://api.fakeyou.com{}".format
        self.__session = Session()
        self.__session.headers = {"accept": "application/json", "content-Type": "application/json"}
        self.proxies = proxies

    def clear_cookies(self):
        return self.__session.cookies.clear()

    def post(self, path: str, data: dict = None, params: dict = None, files: dict = None) -> Response:
        response = self.__session.post(
            self.api(path),
            json=data,
            params=params,
            proxies=self.proxies,
            files=files
        )
        return handle_response(response)

    def get(self, path: str, params: dict = None) -> Response:
        response = self.__session.get(
            self.api(path),
            params=params,
            proxies=self.proxies
        )
        return handle_response(response)

    def get_url(self, url: str, params: dict = None) -> Response:
        response = self.__session.get(
            url,
            params=params,
            proxies=self.proxies
        )
        return handle_response(response)

    def delete(self, path: str, params: dict = None) -> Response:
        response = self.__session.delete(
            self.api(path),
            params=params,
            proxies=self.proxies
        )
        return handle_response(response)


class Wav:
    def __init__(self, hjson, content=None):
        json = hjson["state"]
        self.json = json
        self.jobToken = json["job_token"]
        self.status = json["status"]
        self.resultToken = json["maybe_result_token"]

        if json["maybe_public_bucket_wav_audio_path"]:
            self.link = self.link = "https://storage.googleapis.com/vocodes-public" + str(
                json["maybe_public_bucket_wav_audio_path"])
        else:
            self.link = None

        self.title = json["title"]
        self.text = json["raw_inference_text"]
        if content:
            self.content = content

    def save(self, path=None):
        file_name = path or f"fakeyou_{self.title}_{str(uuid4()).replace('-', '_')}.wav"

        with open(file_name, "wb") as f:
            f.write(self.content if isinstance(self.content, bytes) else bytes(self.content, "utf-8"))

        return file_name


class FakeYou(Service):
    def __init__(self, proxies: dict = None):
        Service.__init__(self, proxies)

    def make_tts_job(self, text: str, tts_model_token: str):
        data = {
            "uuid_idempotency_token": str(uuid4()),
            "tts_model_token": tts_model_token,
            "inference_text": text
        }
        return self.post("/tts/inference", data).json()["inference_job_token"]

    def tts_poll(self, ijt: str):
        while True:
            ijt_data = self.get(f"/tts/job/{ijt}").json()
            wav = Wav(ijt_data)
            # wav = ijt_data
            status_cases = {
                "started": None,
                "pending": None,
                "attempt_failed": Exception("attempt failed"),
                "dead": Exception("dead"),
                "complete_success": "success"
            }
            status = status_cases.get(wav.status)

            if status:
                return self.get_wav_content(wav, ijt_data)
            else:
                sleep(0.2)
                continue



    def get_wav_content(self, wav, ijt_data):
        if wav.link:
            content = self.get_url(wav.link).content
            del wav
            return Wav(ijt_data, content)
        else:
            raise Exception("Path null")

    def say(self, text: str, tts_model_token: str):
        return self.tts_poll(self.make_tts_job(text=text, tts_model_token=tts_model_token))

    def tts_status(self, ijt: str):
        return self.get(f"/tts/job/{ijt}").json()["state"]["status"]

    def get_queue_length(self):
        return self.get("/tts/queue_length").json()["pending_job_count"]

    def delete_tts_result(self, result_token):
        data = {"set_delete": True, "as_mod": True}
        return self.post(f"/tts/result/{result_token}/delete", data)

    def logout(self):
        self.clear_cookies()