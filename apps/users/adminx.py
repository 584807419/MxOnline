import xadmin

from .models import EmailVerifyRecord, Banner


class EmailVerifyRecordAdmin(object):
    list_display = ["code", "email", "send_type", "send_time"]  # 设置默认管理界面显示数据的内容
    search_fields = ["code", "email", "send_type"]  # 添加搜索功能
    list_filter = ["code", "email", "send_type", "send_time"]  # 添加筛选过滤器,时间不好搜索加到筛选里面就好用了


class BannerAdmin(object):
    list_display = ["title", "image", "url", "index", "add_time"]  # 设置默认管理界面显示数据的内容
    search_fields = ["title", "image", "url", "index", "add_time"]
    list_filter = ["title", "image", "url", "index", "add_time"]


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
