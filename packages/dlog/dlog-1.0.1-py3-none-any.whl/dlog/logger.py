# coding:utf-8
# author caturbhuja
# date   2020/11/24 2:43 下午
# wechat chending2012
import logging
from logging import config as log_config
import os
from collections import namedtuple
from dlog.conf.split_by_maxBytes import set_log_config  # todo 还有一个按照日期分割，暂时不测试了。
from dlog.decorator import with_metaclass, Singleton

RootPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class DLog(with_metaclass(Singleton)):
    def __init__(self, debug=False, singleton=False, log_dir_path=None, user_config=None, **kwargs):
        """
        :param debug: debug模式
        :param singleton: 开启单例模式
        :param log_dir_path: 日志文件夹绝对路径
        :param user_config: 用户自定义日志配置
        :param kwargs: 其他参数
        """
        log_dir_path = log_dir_path or "{}{}logs".format(RootPath, os.sep)
        self._check_dir_exists(log_dir_path)
        # 准备参数
        if user_config:
            self._final_config = user_config
        else:
            log_level_info = logging.DEBUG if debug else logging.INFO
            info_log_path = os.path.join(log_dir_path, "./info.log")
            warning_log_path = os.path.join(log_dir_path, "./warn.log")
            error_log_path = os.path.join(log_dir_path, "./error.log")
            self._final_config = set_log_config(
                debug=debug, log_level_info=log_level_info, info_log_path=info_log_path, warning_log_path=warning_log_path,
                error_log_path=error_log_path, **kwargs
            )
        self.log = self._cook_log(self._final_config)

    @staticmethod
    def _check_dir_exists(log_dir_path):
        if not os.path.exists(log_dir_path):
            os.mkdir(log_dir_path)

    @staticmethod
    def _cook_log(config: dict):
        log_config.dictConfig(config)
        info = logging.getLogger("log.info")
        warning = logging.getLogger("log.warning")
        error = logging.getLogger("log.error")
        log_ = namedtuple('log', ["info", "warning", "error"])
        return log_(info=info.info, warning=warning.warning, error=error.error)

    @property
    def get_log(self):
        return self.log

    @property
    def show_log_config(self):
        return self._final_config
