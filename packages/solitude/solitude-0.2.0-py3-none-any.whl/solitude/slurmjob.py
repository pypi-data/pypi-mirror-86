from typing import Dict, Optional, Type

import logging
import requests
import time

from solitude.cache import CacheData


DEFAULT_HOST = "http://oni:11080/"
logger = logging.getLogger("SlurmJob")


class SlurmJob(CacheData):
    def __init__(
        self,
        jobid: int,
        user: Optional[str] = None,
        priority: Optional[str] = None,
        timestamp: Optional[int] = None,
    ):
        super(SlurmJob, self).__init__(timestamp=timestamp)
        self.id: int = jobid
        self.user: Optional[str] = user
        self.priority: Optional[str] = priority
        self._status: Optional[str] = None

    def update(self):
        info = requests.get(f"{DEFAULT_HOST}json/jobinfo/{self.id}").json()
        self.id = info["jobid"]
        self.user = info["user"]
        self.priority = info["priority"]
        self._status = info["status"]

    def is_running(self) -> bool:
        return self._status in ("RUNNING", "PENDING")

    def is_pending(self) -> bool:
        return self._status == "PENDING"

    def is_timeout(self) -> bool:
        return self._status == "TIMEOUT"

    def get_log_text(self) -> str:
        return requests.get(
            f"{DEFAULT_HOST}text/log/{self.id}", allow_redirects=True
        ).text

    def get_log_url(self) -> str:
        return "{}show/{}".format(DEFAULT_HOST, self.id)

    def to_dict(self) -> Dict:
        return dict(
            id=self.id,
            user=self.user,
            priority=self.priority,
            timestamp=self.timestamp,
        )

    @staticmethod
    def check_if_job_exists(jobid: int) -> bool:
        txt = requests.get(f"{DEFAULT_HOST}json/jobinfo/{jobid}").text
        return "does not exist" not in txt

    @classmethod
    def from_dict(cls: Type, dic: Dict) -> "SlurmJob":
        return SlurmJob(
            jobid=dic["id"],
            user=dic["user"],
            priority=dic["priority"],
            timestamp=dic.get("timestamp", int(time.time())),
        )
