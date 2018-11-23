import xadmin
from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ["name", "desc", "add_time"]
    search_fields = ["name", "desc"]
    list_filter = ["name", "desc", "add_time"]
    model_icon = "fa fa-cog fa-spin fa-la fa-fw"


xadmin.site.register(CityDict, CityDictAdmin)


class CourseOrgAdmin(object):
    list_display = ["name", "desc", "click_nums", "fav_nums", "image", "address", "city", "add_time"]
    search_fields = ["name", "desc", "click_nums", "fav_nums", "image", "address", "city"]
    list_filter = ["name", "desc", "click_nums", "fav_nums", "image", "address", "city", "add_time"]
    relfield_style = 'fk_ajax'  # 后台从下拉可选变为可搜索
    model_icon = "fa fa-cog fa-spin fa-la fa-fw"


xadmin.site.register(CourseOrg, CityDictAdmin)


class TeacherAdmin(object):
    list_display = ["org", "name", "work_year", "work_company", "work_position", "points", "click_nums", "fav_nums",
                    "add_time"]
    search_fields = ["org", "name", "work_year", "work_company", "work_position", "points", "click_nums", "fav_nums"]
    list_filter = ["org", "name", "work_year", "work_company", "work_position", "points", "click_nums", "fav_nums",
                   "add_time"]
    model_icon = "fa fa-cog fa-spin fa-la fa-fw"


xadmin.site.register(Teacher, TeacherAdmin)
