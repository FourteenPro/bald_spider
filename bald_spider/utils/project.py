from bald_spider.settings.settings_manager import SettingsManager


def get_settings(settings='settings'):   # 获取配置文件参数
    # _settings = SettingsManager({'1': '2'})  # 直接把配置参数传入配置管理类中
    _settings = SettingsManager()
    _settings.set_settings(settings)   # 把配置文件导入配置管理类中
    return _settings
