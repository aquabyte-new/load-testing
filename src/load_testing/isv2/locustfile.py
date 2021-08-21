import time
import random
import json

from locust import HttpUser, TaskSet, task


EP_PRODUCTION = "https://user_dev:7ff463baf99c9d947b39d1b435a9711f@imageservice.aquabyte.ai:443"
EP_STAGING = "https://user_dev:7ff463baf99c9d947b39d1b435a9711f@imageservice-stg.aquabyte.ai:443"
EP = "http://localhost:5000"

users = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

lati_ann = {
    "lice": [
        {
            "category": "MOVING",
            "xCrop": 2385,
            "yCrop": 342,
            "width": 14,
            "height": 11,
            "liceLocation": "MIDDLE",
            "bodySection": "VENTRAL_POSTERIOR"
        },
        {
            "category": "MOVING",
            "xCrop": 925,
            "yCrop": 353,
            "width": 13,
            "height": 9,
            "liceLocation": "MIDDLE",
            "bodySection": "DORSAL_ANTERIOR"
        },
        {
            "category": "MOVING",
            "xCrop": 940,
            "yCrop": 345,
            "width": 13,
            "height": 10,
            "liceLocation": "MIDDLE",
            "bodySection": "DORSAL_ANTERIOR"
        },
        {
            "category": "ADULT FEMALE",
            "xCrop": 538,
            "yCrop": 576,
            "width": 14,
            "height": 12,
            "liceLocation": "MIDDLE",
            "bodySection": "DORSAL_ANTERIOR"
        },
        {
            "category": "MOVING",
            "xCrop": 588,
            "yCrop": 538,
            "width": 14,
            "height": 13,
            "liceLocation": "MIDDLE",
            "bodySection": "DORSAL_ANTERIOR"
        },
        {
            "category": "MOVING",
            "xCrop": 572,
            "yCrop": 543,
            "width": 14,
            "height": 13,
            "liceLocation": "MIDDLE",
            "bodySection": "DORSAL_ANTERIOR"
        }
    ],
    "isPartial": True,
    "visibleBodySections": [
        "HEAD",
        "DORSAL_ANTERIOR",
        "DORSAL_POSTERIOR",
        "VENTRAL_ANTERIOR",
        "VENTRAL_POSTERIOR"
    ]
}

lati_ann_no_lice = {
    "lice": [],
    "isPartial": True,
    "visibleBodySections": [
        "HEAD"
    ]
}


class HappyPathBehavior(TaskSet):
    def on_start(self):
        if len(users) > 0:
            user_id = users.pop()
            self.requester_id = f'load_test_user_{user_id}'

    @staticmethod
    def _json_payload(**kwargs):
        # Turn parameters into a dict. Omit items those value are None.
        return {k: v for k, v in kwargs.items() if v is not None}

    @task
    def happy_path(self):
        # 1. PUT annotation
        result = self.client.put(f'/lati/annotation/images', json=self._json_payload(
            requesterId=self.requester_id,
            numImages=3
        ), name="annotation_put").json()

        is_at_least_one_accepted = False
        for r in result:
            time.sleep(random.randint(1,5))

            # 2. POST annotation
            if not is_at_least_one_accepted:
                self.client.post(f'/lati/annotation/images', json=self._json_payload(
                    requesterId=self.requester_id,
                    id=r['id'],
                    accepted=True,
                    annotation=lati_ann,
                    skipReasons=None,
                    imageScore=None,
                ), name="annotation_post")

                is_at_least_one_accepted = True
            else:
                if random.randint(0,100) < 50:
                    # Accept
                    self.client.post(f'/lati/annotation/images', json=self._json_payload(
                        requesterId=self.requester_id,
                        id=r['id'],
                        accepted=True,
                        annotation=lati_ann,
                        skipReasons=None,
                        imageScore=None,
                    ), name="annotation_post")
                else:
                    # Skip
                    self.client.post(f'/lati/annotation/images', json=self._json_payload(
                        requesterId=self.requester_id,
                        id=r['id'],
                        accepted=False,
                        annotation=None,
                        skipReasons=['is_bad_crop'],
                        imageScore=None,
                    ), name="annotation_post")

        # 3. PUT qa
        time.sleep(random.randint(1,5))
        result = self.client.put(f'/lati/qa/images', json=self._json_payload(
            requesterId=self.requester_id,
            numImages=3
        ), name="qa_put").json()

        for r in result:
            time.sleep(random.randint(1,5))

            # 4. POST annotation
            random_int = random.randint(0, 100)

            if random_int < 50:
                # Accept With Original Annotation
                self.client.post(f'/lati/qa/images', json=self._json_payload(
                    requesterId=self.requester_id,
                    id=r['id'],
                    accepted=True,
                    annotation=lati_ann,
                    skipReasons=None,
                    imageScore=None,
                ), name="qa_post")
            elif random_int < 75:
                # Accept With New Annotation
                self.client.post(f'/lati/qa/images', json=self._json_payload(
                    requesterId=self.requester_id,
                    id=r['id'],
                    accepted=True,
                    annotation=lati_ann_no_lice,
                    skipReasons=None,
                    imageScore=None,
                ), name="qa_post")
            else:
                # Skip
                self.client.post(f'/lati/qa/images', json=self._json_payload(
                    requesterId=self.requester_id,
                    id=r['id'],
                    accepted=False,
                    annotation=None,
                    skipReasons=['is_bad_crop'],
                    imageScore=None,
                ), name="qa_post")


class HappyPathUser(HttpUser):
    tasks = {HappyPathBehavior:1}
    host = EP
