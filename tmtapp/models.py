from django.db import models


class Files(models.Model):
    """ 附件上传记录表 """

    id = models.AutoField(primary_key=True)
    username = models.CharField('用户登录名', max_length=100, blank=True, default='')
    file_name = models.CharField('文件名', max_length=200, blank=True, )
    file_size = models.CharField('文件大小', max_length=100, blank=True, )
    file_type = models.CharField('文件后缀', max_length=100, blank=True, )
    file_path = models.TextField('文件位置', blank=True, default='')
    file_url = models.TextField('文件访问地址', blank=True, default='')
    device_info = models.TextField('设备信息', blank=True, default='{}')
    status = models.CharField('状态 1有效 0删除', blank=True, max_length=10, default='1')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.id


class Bugs(models.Model):
    """ BUG提交记录 """
    id = models.AutoField(primary_key=True)
    user_id = models.CharField('用户id', max_length=10, blank=True, )
    username = models.CharField('用户登录名', max_length=100, blank=True, default='')
    realname = models.CharField('真实姓名', max_length=100, blank=True, default='')
    title = models.TextField('标题', blank=True, default='')
    link = models.TextField('链接', blank=True, default='')
    product = models.CharField('产品id', max_length=100, blank=True, default='')
    project = models.CharField('项目id', max_length=100, blank=True, default='')
    assignedTo = models.CharField('指派人', max_length=100, blank=True, default='')
    type = models.CharField('类型', max_length=100, blank=True, default='')
    severity = models.CharField('严重程度', max_length=100, blank=True, default='')
    pri = models.CharField('优先级', max_length=100, blank=True, default='')
    file_count = models.CharField('附件个数', max_length=100, blank=True, default='')
    bug_info = models.TextField('设备信息', blank=True, default='{}')
    device_info = models.TextField('设备信息', blank=True, default='{}')
    status = models.CharField('状态', blank=True, max_length=100, default='1')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.id


class AppUpdate(models.Model):
    """ app更新 """

    id = models.AutoField(primary_key=True)
    file_size = models.CharField('文件大小', max_length=100, blank=True, )
    file_path = models.TextField('文件位置', blank=True, default='')
    file_url = models.TextField('文件访问地址', blank=True, default='')
    version = models.CharField('版本', max_length=100, blank=True, )
    update_log = models.TextField('更新内容', blank=True, default='')
    md5 = models.CharField('md5', max_length=100, blank=True, )
    constraint = models.CharField('是否强制更新', max_length=100, blank=True, default='False')
    status = models.CharField('状态 1有效 0删除', blank=True, max_length=10, default='1')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.id
