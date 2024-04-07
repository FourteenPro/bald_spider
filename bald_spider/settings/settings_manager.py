from importlib import import_module
from collections.abc import MutableMapping   # 容器的抽象基类  可变映射

from bald_spider.settings import default_settings


class SettingsManager(MutableMapping):      # 管理文件配置的类  把这个类做得像一个字典 更方便管理
    def __init__(self, values=None):
        self.attributes = {}
        self.set_settings(default_settings)  # 把默认配置设置进来
        self.update_settings(values)   # 兼容不用utils 目录下 get_setting的方式设置配置的方式 而直接把配置传入管理配置文件类中的方式

    def __getitem__(self, item):  # 设置对象中括号取值(Object['取值'])是走这个方法  对象像列表 像字典一样取值
        if item not in self:   # 判断item 是否在 attributes中  这里会运行 __contains__魔法方法
            return None                   # 没有返回None
        return self.attributes[item]      # 有返回值

    def get(self, name, default=None):
        return self[name] if self[name] is not None else default  # 执行self[name] 就像 对象[取值] 执行魔法方法 __getitem__

    def getint(self, name, default=0):  # 返回整数
        return int(self.get(name, default))

    def getfloat(self, name, default=0.0):
        return float(self.get(name, default))

    def getbool(self, name, default=False):  # noqa
        got = self.get(name, default)
        try:
            return bool(int(got))
        except ValueError:
            if got in ('True', 'true', 'TRUE'):
                return True
            if got in ('False', 'false', 'FALSE'):
                return False

            raise ValueError("supported values for bool settings are (0 or 1),(False or True),(false or true),"
                             "(False or True),('0' or '1'),('False' or 'True'),('false' or 'true'),('False' or 'True')")

    def getlist(self, name, default=None):  # 为什么default不是空列表 因为列表是可变的
        value = self.get(name, default or [])  # 在这里才把默认值制空
        if isinstance(value, str):  # 判断是否是字符串
            value = value.split(',')  # 以逗号分割的字符串
        return list(value)

    def __contains__(self, item):   # 这个魔法方法 用于实现in操作符的行为。当你使用in来检查一个元素是否存在于一个容器对象（如列表、元组、字典、集合或自定义对象）中时就会运行这个魔法方法
        return item in self.attributes

    def __setitem__(self, key, value):  # 设置对象中括号设置值(Object['key'] = value)是走这个方法  对象像列表 像字典一样设置值
        self.set(key, value)

    def set(self, key, value):   # 为什么这里要进行封装， 防止在其他地方还用到 里面的代码 封装起来后 直接执行set方法就可以了
        # print(key, value)
        self.attributes[key] = value

    def __delitem__(self, key):  # 设置对象中括号删除值(del Object['key'])是走这个方法  对象像列表 像字典一样删除值
        self.delete(key)

    def delete(self, key):  # 在进行一次封装
        del self.attributes[key]

    def set_settings(self, module):  # 把配置文件里面的 设置 导入到 配置管理类中来
        if isinstance(module, str):   # 判断module 是否是字符串
            module = import_module(module)  # 是字符串 导入包   import_module的功能是导入字符串那个包
        for key in dir(module):     # 把配置模块的属性和值导入 配置管理类中
            if key.isupper():   # 判断key值是否是大写   配置文件的 配置属性名称是大写的
                self.set(key, getattr(module, key))

    def __str__(self):    # 打印实例的时候 会执行这个魔法方法
        return f"<Settings values={self.attributes}>"  # 美化一下打印结果

    __repr__ = __str__

    def __iter__(self):
        return iter(self.attributes)

    def __len__(self):
        return len(self.attributes)

    def update_settings(self, values):
        if values is not None:
            for key, value in values.items():
                self.set(key, value)


if __name__ == '__main__':

    settings = SettingsManager()
    settings['CONCURRENCY'] = 16
    # print(setting['CONCURRENCY'])
    # setting.set_settings('settings')
    # print(SettingsManager())
    print(settings.items())
    print(settings.values())  # 继承可变映射的抽象基类 使SettingsManager类变得像一个字典
    # print(settings.pop())

