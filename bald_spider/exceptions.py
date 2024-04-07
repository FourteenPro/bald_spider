# 自定义异常


class TransformTypeError(TypeError):    # 这里可以继承于 Exception 也可以继承 TypeError
    pass


class OutputError(Exception):
    pass
