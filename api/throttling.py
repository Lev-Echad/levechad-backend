from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

# TODO find a way to do this with metaclasses to reduce code duplication


class HamalDataListThrottle(UserRateThrottle):
    scope = 'hamal-data'


class LoginThrottle(AnonRateThrottle):
    scope = 'login'


class RegistrationThrottle(AnonRateThrottle):
    scope = 'register'
    THROTTLE_SECONDS = 5

    def parse_rate(self, rate):
        """
        This function parses the string rate given (e.g 1/second). We ignore it and return a custom answer.
        :returns: tuple (int, int) (<allowed number of requests>, <period of time in seconds>)
        """
        return 1, type(self).THROTTLE_SECONDS


class SendSMSThrottle(AnonRateThrottle):
    scope = 'send-sms'
    THROTTLE_SECONDS = 60 * 5

    def parse_rate(self, rate):
        """
        This function parses the string rate given (e.g 1/second). We ignore it and return a custom answer.
        :returns: tuple (int, int) (<allowed number of requests>, <period of time in seconds>)
        """
        return 1, type(self).THROTTLE_SECONDS


class CheckSMSThrottle(AnonRateThrottle):
    scope = 'check-sms'
    THROTTLE_SECONDS = 2

    def parse_rate(self, rate):
        """
        This function parses the string rate given (e.g 1/second). We ignore it and return a custom answer.
        :returns: tuple (int, int) (<allowed number of requests>, <period of time in seconds>)
        """
        return 1, type(self).THROTTLE_SECONDS
