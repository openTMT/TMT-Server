from django.db import models


class BaseDeviceInfo(models.Model):
    """ iOS设备基础信息表
    数据来源：https://www.theiphonewiki.com/wiki/Models
    https://www.blakespot.com/ios_device_specifications_grid.html
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField('设备名称', max_length=100, blank=True, default='')
    model_id = models.CharField('model_id', max_length=100, blank=True, default='')
    year = models.CharField('上市年', max_length=100, blank=True, default='')
    ram = models.CharField('内存大小', max_length=100, blank=True, default='')
    screen = models.CharField('分辨率', max_length=100, blank=True, default='')

    def __str__(self):
        return self.id


class iOSDevice(models.Model):
    """ 本系统内支撑的iOS设备 """
    id = models.AutoField(primary_key=True)
    uuid = models.CharField('设备uuid', max_length=100, blank=True, default='')
    status = models.CharField('状态：离线/在线', max_length=100, blank=True, default='')
    device_name = models.CharField('设备名称', max_length=100, blank=True, default='')
    personal_name = models.CharField('个人设置的名称', max_length=100, blank=True, default='')
    model_id = models.CharField('model_id', max_length=100, blank=True, default='')
    version = models.CharField('系统版本', max_length=100, blank=True, default='')
    update_time = models.DateTimeField('更新时间', auto_now=True)
    owner = models.CharField('所属', max_length=100, blank=True, default='public')

    def __str__(self):
        return self.id
