from django.db import models

# Create your models here.
# 发布会表
class Event(models.Model):
    name = models.CharField(max_length=100) # 发布会标题
    limit = models.IntegerField()   # 参加人数
    status = models.BooleanField()  # 状态 表示发布会是否开启
    address = models.CharField(max_length=200)  # 地址
    start_time = models.DateField('events time')    #发布会时间
    create_time = models.DateField(auto_now=True)   #创建时间（自动获取当前时间）

    def __str__(self):
        return self.name
# 嘉宾表
class Guest(models.Model):
    # 注意这里
    event = models.ForeignKey(Event,on_delete=models.DO_NOTHING,) #关联发布会id
    realname = models.CharField(max_length=64)  #姓名
    phone = models.CharField(max_length=16) # 手机号
    email = models.EmailField() # 邮箱
    sign = models.BooleanField()    # 签到状态
    create_time = models.DateField(auto_now=True) # 创建时间 （自动获取当前时间）

    class Meta:
        # 设置两个字段为联合主键
        unique_together = ('event', 'phone')

    def __str__(self):
        return self.realname