from django.db import models


class Users(models.Model):
    """ 用户信息表 """
    id = models.AutoField(primary_key=True)
    username = models.CharField('用户登录名', max_length=100)
    realname = models.CharField('真实姓名', max_length=100, blank=True, )
    email = models.TextField('邮箱', blank=True, default='')
    status = models.CharField('状态', blank=True, max_length=100, default='1')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.id, self.username, self.realname
