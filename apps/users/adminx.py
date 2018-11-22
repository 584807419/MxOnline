import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = "慕雪在线后台管理系统"
    site_footer = "慕课网"
    menu_style= "accordion"



class EmailVerifyRecordAdmin(object):
    list_display = ["code", "email", "send_type", "send_time"]  # 设置默认管理界面显示数据的内容
    search_fields = ["code", "email", "send_type"]  # 添加搜索功能
    list_filter = ["code", "email", "send_type", "send_time"]  # 添加筛选过滤器,时间不好搜索加到筛选里面就好用了
    # 图标用到：https://fontawesome.com/v4.7.0/examples/
    model_icon = 'fa fa-camera-retro fa-lg'


class BannerAdmin(object):
    list_display = ["title", "image", "url", "index", "add_time"]  # 设置默认管理界面显示数据的内容
    search_fields = ["title", "image", "url", "index", "add_time"]
    list_filter = ["title", "image", "url", "index", "add_time"]
    model_icon = 'fa fa-spinner fa-spin fa-lg fa-fw'


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
