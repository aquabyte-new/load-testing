from urllib.parse import urljoin

from imageservice.wsgi import app

from utils.dummy_data import ingress_payload


TEST_USER = 'test_user'

EP_PRODUCTION = "https://user_dev:7ff463baf99c9d947b39d1b435a9711f@imageservice.aquabyte.ai:443"
EP_STAGING = "https://user_dev:7ff463baf99c9d947b39d1b435a9711f@imageservice-stg.aquabyte.ai:443"
EP = EP_PRODUCTION

class Sample:
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
        "penId": "5",
        "siteId": "23",
        "imageScore": 0.0033,
        "capturedAt": "2019-04-11T09:21:03.822683000Z",
        "key": "environment=production/site-id=23/pen-id=4/date=2019-04-24/hour=14/at=2019-04-24T14:58:36.060286000Z/left_frame_crop_1262_782_3082_2256.jpg",
        "pairId": "environment=production/site-id=23/pen-id=4/date=2019-04-24/hour=14/at=2019-04-24T14:58:36.060286000Z/left_frame_crop_1262_782_3082_2256.jpg",
        "leftCropUrl": "https://s3-eu-west-1.amazonaws.com/aquabyte-crops/environment=production/site-id=23/pen-id=4/date=2019-04-24/hour=14/at=2019-04-24T14:58:36.060286000Z/left_frame_crop_1262_782_3082_2253.jpg",
        "rightCropUrl": "https://s3-eu-west-1.amazonaws.com/aquabyte-crops/environment=production/site-id=23/pen-id=4/date=2019-04-24/hour=14/at=2019-04-24T14:58:36.060286000Z/right_frame_crop_1006_811_2674_2294.jpg",
        "leftCropMetadata": {"width": 1820, "height": 1471, "x_coord": 1262, "y_coord": 782, "crop_area": 2677220,
                             "qualityScore": {"quality": 0.003383773611858487, "darkness": 0.9823471307754517,
                                              "modelInfo": {"model": "Mobilenet", "input_size": [224, 224, 3],
                                                            "description": "binary classification good / bad for filtering",
                                                            "output_size": [3],
                                                            "probability": {"is_dark": 2, "is_good": 0,
                                                                            "is_blurry": 1}},
                                              "blurriness": 0.014788443222641945}, "mean_luminance": 14.36250625648994},
        "rightCropMetadata": {"width": 1668, "height": 1483, "x_coord": 1006, "y_coord": 811, "crop_area": 2473644,
                              "qualityScore": {"quality": 0.003383773611858487, "darkness": 0.9823471307754517,
                                               "modelInfo": {"model": "Mobilenet", "input_size": [224, 224, 3],
                                                             "description": "binary classification good / bad for filtering",
                                                             "output_size": [3],
                                                             "probability": {"is_dark": 2, "is_good": 0,
                                                                             "is_blurry": 1}},
                                               "blurriness": 0.014788443222641945},
                              "mean_luminance": 14.129674278109542},
        "cameraMetadata": {"baseline": 0.10079791852561114, "focalLength": 0.013842509663066934,
                           "pixelCountWidth": 3000, "focalLengthPixel": 4012.3216414686767, "imageSensorWidth": 0.01412,
                           "pixelCountHeight": 4096, "imageSensorHeight": 0.01035}
    }

    SAMPLE_IMAGES = """
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:22:31.917740000Z/right_frame_crop_0_173_4096_2252.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:24:26.934641000Z/left_frame_crop_924_0_3588_2527.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:24:26.934641000Z/right_frame_crop_236_0_2756_2504.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:15.970363000Z/left_frame_crop_1420_671_3756_2158.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:15.970363000Z/left_frame_crop_1628_905_3508_1988.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:15.970363000Z/right_frame_crop_1092_905_2828_1994.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:15.970363000Z/right_frame_crop_852_659_3076_2152.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:36.893564000Z/left_frame_crop_1276_483_3884_1883.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:36.893564000Z/left_frame_crop_1404_689_3796_1736.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:36.893564000Z/right_frame_crop_668_407_3204_1848.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:36.893564000Z/right_frame_crop_820_700_3156_1707.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:40.009007000Z/left_frame_crop_1060_1661_3116_2615.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:40.009007000Z/left_frame_crop_916_1497_3220_2814.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:40.009007000Z/right_frame_crop_420_1480_2732_2808.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:40.009007000Z/right_frame_crop_612_1702_2564_2603.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:41.847102000Z/left_frame_crop_1788_0_4096_1244.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:41.847102000Z/left_frame_crop_1956_108_4096_1080.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:41.847102000Z/right_frame_crop_1332_0_3868_1285.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:41.847102000Z/right_frame_crop_1516_120_3700_1074.jpg
    /environment=production/site-id=23/pen-id=4/date=2020-07-28/hour=04/at=2020-07-28T04:36:47.884568000Z/left_frame_crop_1036_841_3148_1994.jpg
    """.split()

class ImageServiceClient:
    def __init__(self, service, init_pens=None):
        # Our tests focus on one service at a time
        self.service = service

        self.client = app.test_client()
        self.test_external_deployment = True

        if init_pens:
            for pen_id, count in init_pens.items():
                self.put_groupselection(pen_id, {"enable": True})
                for i in range(count):
                    self.post_ingress(ingress_payload(idx=i, pen_id=pen_id))

    @staticmethod
    def _json_payload(**kwargs):
        # Turn parameters into a dict. Omit items those value are None.
        return {k: v for k, v in kwargs.items() if v is not None}

    def _get(self, url):
        test_resp = requests.get(urljoin(EP, url))

        return self._load_response(test_resp)

    def _post(self, url, json=None):
        test_resp = requests.post(urljoin(EP, url), json=json)

        return self._load_response(test_resp)

    def _put(self, url, json=None):
        test_resp = requests.put(urljoin(EP, url), json=json)

        return self._load_response(test_resp)

    def _load_response(self, response):
        if response.status_code >= 400:
            try:
                pp(response.json())
            except:
                print(response.content)
        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return response.text

    def put_annotation(self, requesterId=TEST_USER, numImages=5):
        return self._put(f'/lati/annotation/images', json=self._json_payload(
            requesterId=requesterId,
            numImages=numImages
        ))

    def post_annotation(self,
                        requesterId=TEST_USER,
                        id=None,
                        accepted=None,
                        annotation=None,
                        skipReasons=None,
                        imageScore=None,
    ):
        return self._post(f'/lati/annotation/images', json=self._json_payload(
            requesterId=requesterId,
            id=id,
            accepted=accepted,
            annotation=annotation,
            skipReasons=skipReasons,
            imageScore=imageScore,
        ))

    def put_qa(self, requesterId=TEST_USER, numImages=5):
        return self._put(f'/lati/qa/images', json=self._json_payload(
            requesterId=requesterId,
            numImages=numImages
        ))

    def post_qa(self,
                requesterId=TEST_USER,
                id=None,
                accepted=None,
                annotation=None,
                skipReasons=None,
                imageScore=None,
    ):
        return self._post(f'/lati/qa/images', json=self._json_payload(
            requesterId=requesterId,
            id=id,
            accepted=accepted,
            annotation=annotation,
            skipReasons=skipReasons,
            imageScore=imageScore,
        ))

    def put_annotation_pen(self, pen_id, requesterId=TEST_USER, numImages=None):
        return self._put(f'/lati/annotation/images/groupId/{pen_id}', json=self._json_payload(
            requesterId=requesterId,
            numImages=numImages
        ))

    def post_annotation_pen(self, pen_id,
                            requesterId=TEST_USER,
                            id=None,
                            accepted=None,
                            annotation=None,
                            skipReasons=None,
                            imageScore=None,
    ):
        return self._post(f'/lati/annotation/images/groupId/{pen_id}', json=self._json_payload(
            requesterId=requesterId,
            id=id,
            accepted=accepted,
            annotation=annotation,
            skipReasons=skipReasons,
            imageScore=imageScore,
        ))

    def put_qa_pen(self, pen_id, requesterId=TEST_USER, numImages=None):
        return self._put(f'/lati/qa/images/groupId/{pen_id}', json=self._json_payload(
            requesterId=requesterId,
            numImages=numImages
        ))

    def post_qa_pen(self, pen_id,
                    requesterId=TEST_USER,
                    id=None,
                    accepted=None,
                    annotation=None,
                    skipReasons=None,
                    imageScore=None,
    ):
        return self._post(f'/lati/qa/images/groupId/{pen_id}', json=self._json_payload(
            requesterId=requesterId,
            id=id,
            accepted=accepted,
            annotation=annotation,
            skipReasons=skipReasons,
            imageScore=imageScore,
        ))

    def get_groupselection(self):
        return self._get('/lati/groupSelection/')

    def put_groupselection(self, pen_id, json):
        return self._put(f'/lati/groupSelection/{pen_id}', json)

    def get_count(self, pen_id):
        return self._get(f'/lati/count/{pen_id}')

    def get_kpi_config(self, pen_id):
        return self._get(f'/lati/kpiconfig/{pen_id}')

    def set_kpi_config(self, pen_id, kpi_limit):
        return self._post(f'/lati/kpiconfig/{pen_id}', json={
            "kpi_limit": kpi_limit
        })
