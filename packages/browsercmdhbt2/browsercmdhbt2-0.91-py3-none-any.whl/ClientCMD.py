import threading, time, requests, json
import browsercmd_func


class ClientCMD():
    def __init__(self, url_browsercmd):
        self.url_browsercmd = url_browsercmd

    def execute(self):
        while True:
            try:
                json_data = requests.get(self.url_browsercmd).json()
                if "id" in json_data:
                    print("Execute: " + str(json_data["id"]))
                    if int(json_data['type']) == 21:
                        browsercmd_func.upload_youtube(json_data['id'], config=json.loads(json_data['config']))
                    if int(json_data['type']) == 22:
                        browsercmd_func.upload_youtube_by_drive_config(json_data['id'],
                                                                       config=json.loads(json_data['config']))
            except Exception as e:
                raise e
            time.sleep(10)

    def start(self):
        self.threadx = threading.Thread(target=self.execute)
        self.threadx.start()

    def join(self):
        self.threadx.join()
