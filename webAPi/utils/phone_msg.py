# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/14 22:34
# Warning    ：The Hard Way Is Easier
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from webAPi.utils.com import get_config_from_env
from webAPi.utils.snowflake import snow_flake


class SendSms(object):
    def __init__(self, phone: str = None, category: str = None, template_param=None):
        """
        发送短信验证码
        :param phone: 发送的手机号
        :param category: 选择短信模板（阿里云上申请注册）
        :param template_param: 短信验证码或者短信模板中所需要替换的参数，使用字典传入，例如： {"code":123456}
        """
        config = get_config_from_env()
        access_key_id = config.get('SMS_ACCESS_KEY_ID', None)  # 阿里云账号密钥信息
        access_key_secret = config.get('SMS_ACCESS_KEY_SECRET', None)
        sign_name = config.get("SMS_SIGN_NAME", None)  # 短信签名，阿里云上申请

        if access_key_id is None:
            raise ValueError("缺失短信key")
        elif access_key_secret is None:
            raise ValueError("缺失短信secret")
        elif phone is None:
            raise ValueError("手机号错误")
        elif template_param is None:
            raise ValueError("短信模板参数无效")
        elif category is None:
            raise ValueError("短信模板编码无效")
        elif sign_name is None:
            raise ValueError("短信签名错误")

        self.acs_client = AcsClient(access_key_id, access_key_secret)
        self.phone = phone
        self.category = category
        self.template_param = template_param
        self.template_code = self.template_code()
        self.sign_name = sign_name

    def template_code(self):
        """
        选择模板编码
        :param self.category
           authentication: 身份验证
           login_confirmation: 登陆验证
           login_exception: 登陆异常
           user_registration: 用户注册
           change_password:修改密码
           information_change:信息修改
        :return:
        """
        if self.category == "authentication":
            code = self.config.get('AUTHENTICATION', None)
            if code is None:
                raise ValueError("配置文件中未找到模板编码AUTHENTICATION")
            return code

        elif self.category == "login_confirmation":
            code = self.config.get('LOGIN_CONFIRMATION', None)
            if code is None:
                raise ValueError("配置文件中未找到模板编码LOGIN_CONFIRMATION")
            return code
        elif self.category == "login_exception":
            code = self.config.get('LOGIN_EXCEPTION', None)
            if code is None:
                raise ValueError("配置文件中未找到模板编码LOGIN_EXCEPTION")
            return code
        elif self.category == "user_registration":
            code = self.config.get('USER_REGISTRATION', None)
            if code is None:
                raise ValueError("配置文件中未找到模板编码USER_REGISTRATION")
            return code
        elif self.category == "change_password":
            code = self.config.get('CHANGE_PASSWORD', None)
            if code is None:
                raise ValueError("配置文件中未找到模板编码CHANGE_PASSWORD")
            return code
        elif self.category == "information_change":
            code = self.config.get('INFORMATION_CHANGE', None)
            if code is None:
                raise ValueError("配置文件中未找到模板编码INFORMATION_CHANGE")
            return code
        else:
            raise ValueError("短信模板编码无效")

    def send_sms(self):
        """
        发送短信
        :return:
        """

        sms_request = CommonRequest()

        # 固定设置
        sms_request.set_accept_format('json')
        sms_request.set_domain('dysmsapi.aliyuncs.com')
        sms_request.set_method('POST')
        sms_request.set_protocol_type('https')  # https | http
        sms_request.set_version('2020-12-11')
        sms_request.set_action_name('SendSms')

        # 短信发送的号码列表，必填。
        sms_request.add_query_param('PhoneNumbers', self.phone)
        # 短信签名，必填。
        sms_request.add_query_param('SignName', self.sign_name)

        # 申请的短信模板编码,必填
        sms_request.add_query_param('TemplateCode', self.template_code)

        # 短信模板变量参数 类似{"code":"12345"}，必填。
        sms_request.add_query_param('TemplateParam', self.template_param)

        # 设置业务请求流水号，必填。使用雪花算法生成唯一id
        build_id = snow_flake.get_id()
        sms_request.add_query_param('OutId', build_id)

        # 调用短信发送接口，返回json
        sms_response = self.acs_client.do_action_with_exception(sms_request)

        return sms_response


