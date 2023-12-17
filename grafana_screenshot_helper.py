import requests
import base64
import os


class GrafanaScreenshotHelper:
    # SCREENSHOT_DATA = {
    #     "grafana_username": "grafana_user", # Will override standard password (from config) if provided
    #     "grafana_password": "grafana_pw",
    #     "grafana_url": "192.168.1.71:3000",
    #     "requests": [
    #         {
    #             "file_name": "AccountBalances.png",
    #             "url_suffix": "/d/fa448709-898c-438d-b578-2557ff169a36/monarch2b-mint-account-balance-history",
    #             "width": 600,
    #             "height": 11000,
    #         },
    #         {
    #             "file_name": "Transactions.png",
    #             "url_suffix": "/d/u4a1SzZgz/multi-transaction-aggregations",
    #             "width": 600,
    #             "height": 4000,
    #         },
    #     ],
    # }

    def __init__(
        self,
        scraper_url,
        grafana_username=None,
        grafana_password=None,
        grafana_url=None,
    ) -> None:
        self.scraper_url = scraper_url
        self.grafana_username = grafana_username
        self.grafana_password = grafana_password
        self.grafana_url = grafana_url
        self._requests = []
        self._request_json = None
        self._http_request_result = None

    def add_request(self, file_name, url_suffix, width, height) -> None:
        request = {
            "file_name": file_name,
            "url_suffix": url_suffix,
            "width": width,
            "height": height,
        }
        self._requests.append(request)

    def _create_json(self) -> None:
        temp_json = {}

        # TODO - Start here
        if self.grafana_username is not None:
            temp_json["grafana_username"] = self.grafana_username
        if self.grafana_password is not None:
            temp_json["grafana_password"] = self.grafana_password
        if self.grafana_url is not None:
            temp_json["grafana_url"] = self.grafana_url

        if len(self._requests) == 0:
            raise Exception("You must add a request")
        else:
            temp_json["requests"] = self._requests

        self._request_json = temp_json

    def _make_http_request(self) -> None:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # TODO - Need a timeout something
        self._http_request_result = requests.post(
            f"http://{self.scraper_url}/get_screenshots",
            json=self._request_json,
            headers=headers,
        )

    def _save_pictures_from_http_request(self, save_folder_path):
        try:
            images64 = self._http_request_result.json()[
                "images"
            ]  # List of dictionaries with Image and Filename

            # https://stackoverflow.com/questions/2323128/convert-string-in-base64-to-image-and-save-on-filesystem
            for image in images64:
                if image["Success"]:
                    output_path = f'{save_folder_path}/{image["Filename"]}'
                    with open(output_path, "wb") as fh:
                        fh.write(base64.decodebytes(bytes(image["Image"], "utf-8")))
                        print(f"File saved to: {output_path}")
                else:
                    # raise Exception("Failed image creation")
                    print(f"Failed image creation for {image['Filename']}")
        except Exception as e:
            print(e)

    def _erase_contents_of_save_folder(self, save_folder_path):
        for file_name in os.listdir(save_folder_path):
            os.remove(f"{save_folder_path}/{file_name}")

    def download_screenshots(self, save_folder_path) -> bool:
        # True if successful
        try:
            self._create_json()
            self._make_http_request()
            self._erase_contents_of_save_folder(save_folder_path=save_folder_path)
            self._save_pictures_from_http_request(save_folder_path=save_folder_path)
            return True
        except Exception as e:
            return False
