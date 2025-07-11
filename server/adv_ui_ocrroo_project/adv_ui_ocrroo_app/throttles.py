from rest_framework import throttling

class GetVidFrameThrottle(throttling.AnonRateThrottle):
    scope = 'vid_frame'


class ThrottleTest(throttling.AnonRateThrottle):
    scope = 'test'