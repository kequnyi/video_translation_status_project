import time
import requests
import logging

class StatusClient:
    def __init__(self, url, initial_backoff=1, max_backoff=60, timeout=10, retries=5):
        self.url = url
        self.initial_backoff = initial_backoff
        self.max_backoff = max_backoff
        self.timeout = timeout
        self.retries = retries

    def check_status(self, callback=None):
        backoff = self.initial_backoff
        attempts = 0

        while attempts < self.retries:
            try:
                response = requests.get(self.url, timeout=self.timeout)
                response.raise_for_status()
                result = response.json().get("result")

                logging.info(f"Received result: {result}")

                if result in ["completed", "error"]:
                    if callback:
                        callback(result)
                    return result

                time.sleep(backoff)
                backoff = min(backoff * 2, self.max_backoff)
                attempts += 1
            except requests.RequestException as e:
                logging.error(f"Request failed: {e}")
                time.sleep(backoff)
                backoff = min(backoff * 2, self.max_backoff)
                attempts += 1

        logging.warning(f"Max retries reached. Giving up.")
        return None

# callback
def job_finished_callback(status):
    print(f"Job finished with status: {status}")
