# -*- coding:utf-8 -*-
"""
配置文件
@Author  :   g1879
@Contact :   g1879@qq.com
@File    :   config.py
"""
from configparser import ConfigParser, NoSectionError, NoOptionError
from pathlib import Path
from typing import Any, Union

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class OptionsManager(object):
    """管理配置文件内容的类"""

    def __init__(self, path: str = None):
        """初始化，读取配置文件，如没有设置临时文件夹，则设置并新建  \n
        :param path: ini文件的路径，默认读取模块文件夹下的
        """
        self.ini_path = path or str(Path(__file__).parent / 'configs.ini')
        self._conf = ConfigParser()
        self._conf.read(self.ini_path, encoding='utf-8')

        if 'global_tmp_path' not in self.paths or not self.get_value('paths', 'global_tmp_path'):
            global_tmp_path = str((Path(__file__).parent / 'tmp').absolute())
            Path(global_tmp_path).mkdir(parents=True, exist_ok=True)
            self.set_item('paths', 'global_tmp_path', global_tmp_path)
            self.save()

    def __text__(self) -> str:
        """打印ini文件内容"""
        return (f"paths:\n"
                f"{self.get_option('paths')}\n\n"
                "chrome options:\n"
                f"{self.get_option('chrome_options')}\n\n"
                "session options:\n"
                f"{self.get_option('session_options')}")

    @property
    def paths(self) -> dict:
        """返回paths设置"""
        return self.get_option('paths')

    @property
    def chrome_options(self) -> dict:
        """返回chrome设置"""
        return self.get_option('chrome_options')

    @property
    def session_options(self) -> dict:
        """返回session设置"""
        return self.get_option('session_options')

    def get_value(self, section: str, item: str) -> Any:
        """获取配置的值         \n
        :param section: 段名
        :param item: 项名
        :return: 项值
        """
        try:
            return eval(self._conf.get(section, item))
        except SyntaxError:
            return self._conf.get(section, item)
        except NoSectionError and NoOptionError:
            return None

    def get_option(self, section: str) -> dict:
        """把section内容以字典方式返回   \n
        :param section: 段名
        :return: 段内容生成的字典
        """
        items = self._conf.items(section)
        option = dict()

        for j in items:
            try:
                option[j[0]] = eval(self._conf.get(section, j[0]).replace('\\', '\\\\'))
            except:
                option[j[0]] = self._conf.get(section, j[0])

        return option

    def set_item(self, section: str, item: str, value: Any):
        """设置配置值            \n
        :param section: 段名
        :param item: 项名
        :param value: 项值
        :return: 当前对象
        """
        self._conf.set(section, item, str(value))
        return self

    def save(self, path: str = None):
        """保存配置文件                                               \n
        :param path: ini文件的路径，传入 'default' 保存到默认ini文件
        :return: 当前对象
        """
        path = Path(__file__).parent / 'configs.ini' if path == 'default' else path
        path = Path(path or self.ini_path)
        path = path / 'config.ini' if path.is_dir() else path
        path = path.absolute()
        self._conf.write(open(path, 'w', encoding='utf-8'))

        return self


class DriverOptions(Options):
    """chrome浏览器配置类，继承自selenium.webdriver.chrome.options的Options类，
    增加了删除配置和保存到文件方法。
    """

    def __init__(self, read_file: bool = True, ini_path: str = None):
        """初始化，默认从文件读取设置                      \n
        :param read_file: 是否从默认ini文件中读取配置信息
        :param ini_path: ini文件路径，为None则读取默认ini文件
        """
        super().__init__()
        self._driver_path = None
        self.ini_path = None

        if read_file:
            self.ini_path = ini_path or str(Path(__file__).parent / 'configs.ini')
            om = OptionsManager(self.ini_path)
            options_dict = om.chrome_options
            self._binary_location = options_dict.get('binary_location', '')
            self._arguments = options_dict.get('arguments', [])
            self._extensions = options_dict.get('extensions', [])
            self._experimental_options = options_dict.get('experimental_options', {})
            self._debugger_address = options_dict.get('debugger_address', None)
            self._driver_path = om.paths.get('chromedriver_path', None)

    @property
    def driver_path(self) -> str:
        return self._driver_path

    @property
    def chrome_path(self) -> str:
        return self.binary_location

    def save(self, path: str = None):
        """保存设置到文件                                              \n
        :param path: ini文件的路径，传入 'default' 保存到默认ini文件
        :return: 当前对象
        """
        om = OptionsManager()
        options = _chrome_options_to_dict(self)
        path = Path(__file__).parent / 'configs.ini' if path == 'default' else path
        path = Path(path or self.ini_path)
        path = path / 'config.ini' if path.is_dir() else path
        path = path.absolute()

        for i in options:
            if i == 'driver_path':
                om.set_item('paths', 'chromedriver_path', options[i])
            else:
                om.set_item('chrome_options', i, options[i])

        om.save(path)

        return self

    def remove_argument(self, value: str):
        """移除一个argument项                                    \n
        :param value: 设置项名，有值的设置项传入设置名称即可
        :return: 当前对象
        """
        del_list = []

        for argument in self._arguments:
            if argument.startswith(value):
                del_list.append(argument)

        for del_arg in del_list:
            self._arguments.remove(del_arg)

        return self

    def remove_experimental_option(self, key: str):
        """移除一个实验设置，传入key值删除  \n
        :param key: 实验设置的名称
        :return: 当前对象
        """
        if key in self._experimental_options:
            self._experimental_options.pop(key)

        return self

    def remove_all_extensions(self):
        """移除所有插件             \n
        :return: 当前对象
        """
        # 因插件是以整个文件储存，难以移除其中一个，故如须设置则全部移除再重设
        self._extensions = []
        return self

    def set_argument(self, arg: str, value: Union[bool, str]):
        """设置浏览器配置的argument属性                          \n
        :param arg: 属性名
        :param value: 属性值，有值的属性传入值，没有的传入bool
        :return: 当前对象
        """
        self.remove_argument(arg)

        if value:
            arg_str = arg if isinstance(value, bool) else f'{arg}={value}'
            self.add_argument(arg_str)

        return self

    def set_headless(self, on_off: bool = True):
        """设置是否隐藏浏览器界面   \n
        :param on_off: 开或关
        :return: 当前对象
        """
        on_off = True if on_off else False
        return self.set_argument('--headless', on_off)

    def set_no_imgs(self, on_off: bool = True):
        """设置是否加载图片           \n
        :param on_off: 开或关
        :return: 当前对象
        """
        on_off = True if on_off else False
        return self.set_argument('--blink-settings=imagesEnabled=false', on_off)

    def set_no_js(self, on_off: bool = True):
        """设置是否禁用js       \n
        :param on_off: 开或关
        :return: 当前对象
        """
        on_off = True if on_off else False
        return self.set_argument('--disable-javascript', on_off)

    def set_mute(self, on_off: bool = True):
        """设置是否静音            \n
        :param on_off: 开或关
        :return: 当前对象
        """
        on_off = True if on_off else False
        return self.set_argument('--mute-audio', on_off)

    def set_user_agent(self, user_agent: str):
        """设置user agent                  \n
        :param user_agent: user agent文本
        :return: 当前对象
        """
        return self.set_argument('user-agent', user_agent)

    def set_proxy(self, proxy: str):
        """设置代理                    \n
        :param proxy: 代理url和端口
        :return: 当前对象
        """
        return self.set_argument('--proxy-server', proxy)

    def set_paths(self,
                  driver_path: str = None,
                  chrome_path: str = None,
                  debugger_address: str = None,
                  download_path: str = None,
                  user_data_path: str = None,
                  cache_path: str = None):
        """快捷的路径设置函数                                             \n
        :param driver_path: chromedriver.exe路径
        :param chrome_path: chrome.exe路径
        :param debugger_address: 调试浏览器地址，例：127.0.0.1:9222
        :param download_path: 下载文件路径
        :param user_data_path: 用户数据路径
        :param cache_path: 缓存路径
        :return: 当前对象
        """

        def format_path(path: str) -> str:
            return path.replace('/', '\\')

        if driver_path is not None:
            self._driver_path = format_path(driver_path)

        if chrome_path is not None:
            self.binary_location = format_path(chrome_path)

        if debugger_address is not None:
            self.debugger_address = debugger_address

        if download_path is not None:
            self.experimental_options['prefs']['download.default_directory'] = format_path(download_path)

        if user_data_path is not None:
            self.set_argument('--user-data-dir', format_path(user_data_path))

        if cache_path is not None:
            self.set_argument('--disk-cache-dir', format_path(cache_path))

        return self


def _dict_to_chrome_options(options: dict) -> Options:
    """从传入的字典获取浏览器设置，返回ChromeOptions对象  \n
    :param options: 配置信息字典
    :return: 保存浏览器配置的ChromeOptions对象
    """
    chrome_options = webdriver.ChromeOptions()
    # 已打开的浏览器路径
    if options.get('debugger_address', None):
        chrome_options.debugger_address = options['debugger_address']

    # 创建新的浏览器
    else:
        # 浏览器的exe文件路径
        if options.get('binary_location', None):
            chrome_options.binary_location = options['binary_location']

        # 启动参数
        if options.get('arguments', None):
            if not isinstance(options['arguments'], list):
                raise Exception(f"Arguments need list，not {type(options['arguments'])}.")

            for arg in options['arguments']:
                chrome_options.add_argument(arg)

        # 加载插件
        if options.get('extension_files', None):
            if not isinstance(options['extension_files'], list):
                raise Exception(f'Extension files need list，not {type(options["extension_files"])}.')

            for arg in options['extension_files']:
                chrome_options.add_extension(arg)

        # 扩展设置
        if options.get('extensions', None):
            if not isinstance(options['extensions'], list):
                raise Exception(f'Extensions need list，not {type(options["extensions"])}.')

            for arg in options['extensions']:
                chrome_options.add_encoded_extension(arg)

        # 实验性质的设置参数
        if options.get('experimental_options', None):
            if not isinstance(options['experimental_options'], dict):
                raise Exception(f'Experimental options need dict，not {type(options["experimental_options"])}.')

            for i in options['experimental_options']:
                chrome_options.add_experimental_option(i, options['experimental_options'][i])
        # if options.get('capabilities' ,None):
        #     pass  # 未知怎么用
    return chrome_options


def _chrome_options_to_dict(options: Union[dict, DriverOptions, None]) -> Union[dict, None]:
    """把chrome配置对象转换为字典                             \n
    :param options: chrome配置对象，字典或DriverOptions对象
    :return: 配置字典
    """
    if options is None or isinstance(options, dict):
        return options

    re_dict = dict()
    re_dict['debugger_address'] = options.debugger_address
    re_dict['binary_location'] = options.binary_location
    re_dict['debugger_address'] = options.debugger_address
    re_dict['arguments'] = options.arguments
    re_dict['extensions'] = options.extensions
    re_dict['experimental_options'] = options.experimental_options

    try:
        re_dict['driver_path'] = options.driver_path
    except:
        re_dict['driver_path'] = None
    # re_dict['capabilities'] = options.capabilities
    return re_dict
