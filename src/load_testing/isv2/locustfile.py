import sys
import time
import random
import requests
import json
import copy
import datetime
import boto3

from locust import HttpUser, TaskSet, task

#######################################
# Endpoints
#######################################
TEST_ENVIRONMENT = 'local'
confirmation = input(f'Confirm that you want to load test {TEST_ENVIRONMENT.upper()} (type yes/no): ')
if not confirmation == "yes":
    print("Terminating execution.")
    sys.exit(1)


def get_api_password():
    ssm = boto3.client('ssm', region_name='eu-west-1')
    param = ssm.get_parameter(Name='/api-password/image-service/user_dev', WithDecryption=True)

    return param['Parameter']['Value']


if TEST_ENVIRONMENT == 'local': EP = 'http://localhost:5000/'
elif TEST_ENVIRONMENT == 'staging': EP = f'https://user_dev:{get_api_password()}@imageservice-stg.aquabyte.ai:443'
elif TEST_ENVIRONMENT == 'production': EP = f'https://user_dev:{get_api_password()}@imageservice-production.aquabyte.ai:443'
else: raise f'TEST_ENVIRONMENT is {TEST_ENVIRONMENT}. Must be one of `local`, `staging`, or `production`.'

#######################################
# Simulated Users
#######################################
users = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

#######################################
# Dummy Data
#######################################
site_pen_ids = [
    (109, 251),
    (45, 160),
    (114, 273),
    (45, 67),
    (68, 123),
    (45, 193)
]

for pen_id in [e[1] for e in site_pen_ids] + ['83', '100', '122', '123', '128', '132', '138', '149',
                                              '151']:  ## Extra pens are from WeightedQueue config file in imageservice-v2
    requests.put(f'{EP}/lati/groupSelection/{pen_id}', json={"enable": True})

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

add_data_payload_template = {
    "pairId": "environment=production/site-id=23/pen-id=4/date=2019-04-24/hour=14/at=2019-04-24T14:58:36.060286000Z/left_frame_crop_1262_782_3082_2256.jpg",
    "capturedAt": "2019-04-11T09:21:03.822683000Z",
    "siteId": "23",
    "penId": "5",
    "bucket": "aquabyte-frames-resized-inbound",
    "imageScore": 0.0033,
    "imageScoreVersion": "unit_testing",
    "feedingHourWeight": 1.0,
    "cameraMetadata": {"baseline": 0.10079791852561114, "focalLength": 0.013842509663066934,
                       "pixelCountWidth": 3000, "focalLengthPixel": 4012.3216414686767, "imageSensorWidth": 0.01412,
                       "pixelCountHeight": 4096, "imageSensorHeight": 0.01035},
    "key": "environment=production/site-id=23/pen-id=4/date=2019-04-24/hour=14/at=2019-04-24T14:58:36.060286000Z/left_frame_crop_1262_782_3082_2256.jpg",
    "groupId": "5",
    "leftCropUrl": "https://s3-eu-west-1.amazonaws.com/aquabyte-crops/environment=production/site-id=23/pen-id=4/date=2019-04-24/hour=14/at=2019-04-24T14:58:36.060286000Z/left_frame_crop_1262_782_3082_2253.jpg",
    "leftCropMetadata": {"width": 1820, "height": 1471, "x_coord": 1262, "y_coord": 782, "crop_area": 2677220,
                         "qualityScore": {"quality": 0.003383773611858487, "darkness": 0.9823471307754517,
                                          "modelInfo": {"model": "Mobilenet", "input_size": [224, 224, 3],
                                                        "description": "binary classification good / bad for filtering",
                                                        "output_size": [3],
                                                        "probability": {"is_dark": 2, "is_good": 0,
                                                                        "is_blurry": 1}},
                                          "blurriness": 0.014788443222641945}, "mean_luminance": 14.36250625648994},
    "rightCropUrl": "https://s3-eu-west-1.amazonaws.com/aquabyte-crops/environment=production/site-id=23/pen-id=4/date=2019-04-24/hour=14/at=2019-04-24T14:58:36.060286000Z/right_frame_crop_1006_811_2674_2294.jpg",
    "rightCropMetadata": {"width": 1668, "height": 1483, "x_coord": 1006, "y_coord": 811, "crop_area": 2473644,
                          "qualityScore": {"quality": 0.003383773611858487, "darkness": 0.9823471307754517,
                                           "modelInfo": {"model": "Mobilenet", "input_size": [224, 224, 3],
                                                         "description": "binary classification good / bad for filtering",
                                                         "output_size": [3],
                                                         "probability": {"is_dark": 2, "is_good": 0,
                                                                         "is_blurry": 1}},
                                           "blurriness": 0.014788443222641945},
                          "mean_luminance": 14.129674278109542}
}


def generate_ingress_payload(
        site_id: str = add_data_payload_template['siteId'],
        pen_id: str = add_data_payload_template['penId'],
        utc_timestamp: datetime.datetime = None,
        image_score: float = 0.5
) -> dict:
    generated_payload = copy.deepcopy(add_data_payload_template)

    generated_payload['penId'] = pen_id
    generated_payload['siteId'] = site_id

    if not utc_timestamp:
        utc_timestamp = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    utc_timestamp = utc_timestamp.replace(tzinfo=datetime.timezone.utc)
    generated_payload['capturedAt'] = utc_timestamp.isoformat()

    path_string = f'environment=production/' \
                  + f'site-id={site_id}/' \
                  + f'pen-id={pen_id}/' \
                  + f'date={utc_timestamp.date().isoformat()}/' \
                  + f'hour={utc_timestamp.hour:02d}/' \
                  + f'at={utc_timestamp.isoformat()}/'
    generated_payload['key'] = path_string + add_data_payload_template['key'].split('/')[-1]
    generated_payload['pairId'] = path_string + add_data_payload_template['pairId'].split('/')[-1]

    url_prefix = 'https://s3-eu-west-1.amazonaws.com/aquabyte-crops/'
    generated_payload['leftCropUrl'] = url_prefix + path_string + add_data_payload_template['leftCropUrl']
    generated_payload['rightCropUrl'] = url_prefix + path_string + add_data_payload_template['rightCropUrl']

    generated_payload['imageScore'] = image_score

    return generated_payload


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
    def qa(self):
        # 3. PUT qa
        time.sleep(random.randint(1, 5))
        result = self.client.put(f'/lati/qa/images', json=self._json_payload(
            requesterId=self.requester_id,
            numImages=5
        ), name="qa_put").json()

        for r in result[0:random.randint(3, 5)]:
            time.sleep(random.randint(1, 5))

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
                ), name="qa_post_accept")
            elif random_int < 75:
                # Accept With New Annotation
                self.client.post(f'/lati/qa/images', json=self._json_payload(
                    requesterId=self.requester_id,
                    id=r['id'],
                    accepted=True,
                    annotation=lati_ann_no_lice,
                    skipReasons=None,
                    imageScore=None,
                ), name="qa_post_accept")
            else:
                # Skip
                self.client.post(f'/lati/qa/images', json=self._json_payload(
                    requesterId=self.requester_id,
                    id=r['id'],
                    accepted=False,
                    annotation=None,
                    skipReasons=['is_bad_crop'],
                    imageScore=None,
                ), name="qa_post_skip")

    @task(3)
    def annotation(self):
        # 1. PUT annotation
        result = self.client.put(f'/lati/annotation/images', json=self._json_payload(
            requesterId=self.requester_id,
            numImages=5
        ), name="annotation_put").json()

        is_at_least_one_accepted = False
        for r in result[0:random.randint(3, 5)]:
            time.sleep(random.randint(1, 5))

            # 2. POST annotation
            if not is_at_least_one_accepted:
                self.client.post(f'/lati/annotation/images', json=self._json_payload(
                    requesterId=self.requester_id,
                    id=r['id'],
                    accepted=True,
                    annotation=lati_ann,
                    skipReasons=None,
                    imageScore=None,
                ), name="annotation_post_accept")

                is_at_least_one_accepted = True
            else:
                if random.randint(0, 100) < 50:
                    # Accept
                    self.client.post(f'/lati/annotation/images', json=self._json_payload(
                        requesterId=self.requester_id,
                        id=r['id'],
                        accepted=True,
                        annotation=lati_ann,
                        skipReasons=None,
                        imageScore=None,
                    ), name="annotation_post_accept")
                else:
                    # Skip
                    self.client.post(f'/lati/annotation/images', json=self._json_payload(
                        requesterId=self.requester_id,
                        id=r['id'],
                        accepted=False,
                        annotation=None,
                        skipReasons=['is_bad_crop'],
                        imageScore=None,
                    ), name="annotation_post_skip")

    @task(10)
    def ingress(self):
        # 1. POST ingress
        for _ in range(10):
            site_id, pen_id = random.choice(site_pen_ids)
            self.client.post(f'/lati/ingress/images', json=generate_ingress_payload(site_id, pen_id), name="ingress")
            time.sleep(1)


class HappyPathUser(HttpUser):
    tasks = {HappyPathBehavior: 1}
    host = EP
