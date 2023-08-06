from __future__ import print_function

import importlib
import json
# python
import logging
import os
import random
import uuid

from.exceptions import ApiTimeOutExpiredError
from .settingsx import settingsx

logger = logging.getLogger(__name__)

settings = settingsx()

class AWSUtil():

    def __init__(self):
        pass

    event_req_context = None

    #######################################################################################################


    @classmethod
    def get_aws_request_id(cls, request):
        """

        :param request:
        :return:
        """
        context = cls.get_lambda_context(request)
        if context:
            return context.aws_request_id
        return uuid.uuid4().__str__()

    @staticmethod
    def get_func_name():
        """

        :return:
        """
        if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
            return os.environ['AWS_LAMBDA_FUNCTION_NAME']
        else:
            return settings.FUNC_NAME

    @staticmethod
    def get_func_ver():
        """

        :return:
        """
        if 'AWS_LAMBDA_FUNCTION_VERSION' in os.environ:
            return os.environ['AWS_LAMBDA_FUNCTION_VERSION']
        else:
            return "VER"

    @staticmethod
    def get_func_mem():
        """

        :return:
        """
        if 'AWS_LAMBDA_FUNCTION_MEMORY_SIZE' in os.environ:
            return os.environ['AWS_LAMBDA_FUNCTION_MEMORY_SIZE']
        else:
            return "MEM"

    @staticmethod
    def get_func_region():
        """

        :return:
        """
        if 'AWS_REGION' in os.environ:
            return os.environ['AWS_REGION']
        else:
            if 'AWS_DEFAULT_REGION' in os.environ:
                return os.environ['AWS_DEFAULT_REGION']
            return settings.AWS_REGION



    @classmethod
    def get_context(cls):
        """

        :return:
        """
        ret = {"awsRegion": cls.get_func_region(), "functionName": cls.get_func_name(),
               "functionVersion": cls.get_func_ver(), "functionMemorySize": cls.get_func_mem()}
        return ret




    @classmethod
    def get_correlation_from_event(cls, event):
        """

        :param event:
        :return:
        """
        if cls.event_req_context:
            logger.debug("cached event req_context", extra=cls.event_req_context)
            return cls.event_req_context
        correlate_id = ''
        user_agent = ''
        debug_flag = ''
        # from api gateway
        if "httpMethod" in event and "requestContext" in event:
            if "headers" in event:
                headers = event["headers"]
                # get correlation-id
                if "x-correlation-id" in headers:
                    correlate_id = headers["x-correlation-id"]
                else:
                    if "aws_request_id" in headers:
                        correlate_id = headers["aws_request_id"]
                    else:
                        correlate_id = uuid.uuid4().__str__()
                # get user-agent = get_func_name + ':' + path + ':' + request.method + ':' + host_ip
                if "x-user-agent" in headers:
                    user_agent = headers["x-user-agent"]
                else:
                    if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
                        func_name = os.environ['AWS_LAMBDA_FUNCTION_NAME']
                    else:
                        if "apiId" in event["requestContext"]:
                            func_name = event["requestContext"]["apiId"]
                        else:
                            func_name = headers["Host"]
                    if "path" in event["requestContext"]:
                        path = event["requestContext"]["path"]
                    else:
                        path = "path"
                    if "httpMethod" in event:
                        method = event["httpMethod"]
                    else:
                        if "httpMethod" in event["requestContext"]:
                            method = event["requestContext"]["httpMethod"]
                        else:
                            method = "method"
                    host_ip = "12.34.56.78"
                    user_agent = str(func_name) + ':' + str(path) + ':' + str(method) + ':' + str(host_ip)
                    logger.debug("user_agent:" + user_agent, extra=cls.event_req_context)
        # from other source
        else:
            if "x-correlation-id" in event:
                correlate_id = event["x-correlation-id"]
            if "x-user-agent" in event:
                user_agent = event["x-user-agent"]
            if "debug-log-enabled" in event:
                debug_flag = event["debug-log-enabled"]
        ret = {"x-user-agent": user_agent, "aws_request_id": '',
               "x-correlation-id": correlate_id, "debug-log-enabled": debug_flag}
        if "x-api-key" in event:
            ret["x-api-key"] = event["x-api-key"]
        # @TODO get all data for request contect
        cls.event_req_context = ret
        return cls.event_req_context


    @classmethod
    def get_timeout(cls, request):
        """

        :param request:
        :return:
        """
        if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
            context = cls.get_lambda_context(request)
            if context:
                return cls.get_timeout_mili(context)
        return None

    @classmethod
    def get_timeout_mili(cls, context):
        """

        :param context:
        :return:
        """
        mili = context.get_remaining_time_in_millis()
        logger.debug("mili=" + str(mili))
        sc = mili / 1000
        timeout = sc - settings.RECOVER_TIMEOUT_IN_SC
        logger.debug("timeout=" + str(timeout))
        if timeout > settings.MINIMUM_SERVICE_TIMEOUT_IN_SC:
            return timeout
        raise ApiTimeOutExpiredError("left " + str(timeout))

    @staticmethod
    def get_lambda_context(request):
        """

        :param request:
        :return:
        """
        # AWS_REGION
        # AWS_LAMBDA_FUNCTION_NAME
        # 'lambda.context'
        # x-amzn-RequestId
        if 'lambda.context' in request.headers:
            return request.headers['lambda.context']
        elif 'context' in request.headers:
            return request.headers['context']
        else:
            return None
