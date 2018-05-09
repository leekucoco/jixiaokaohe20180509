import xadmin
from .models import Agent,Post,Rank13Coefficent,Rank13Demands

class AgentAdAdmin(object):
    list_display = ["name", "add_time"]
class PostAdAdmin(object):
    list_display = ["name", "add_time"]
    list_editable = ["name", ]
class Rank13DemandsAdmin(object):
    list_display = ["agent", "post","rank","demandyears","educationdemands",
                    "primccbpdemands","titledemands","add_time",]
    list_editable = ["rank","demandyears","educationdemands",
                    "primccbpdemands","titledemands",]
    search_fields = ['agent__name','post__name','rank', ]
class Rank13CoefficentAdmin(object):
    list_display = ["agent", "post","rank","level","coefficent","add_time",]
    list_editable = ["coefficent", ]
    search_fields = ['agent__name', 'post__name', 'coefficent',]

xadmin.site.register(Agent, AgentAdAdmin)
xadmin.site.register(Post, AgentAdAdmin)
xadmin.site.register(Rank13Demands, Rank13DemandsAdmin)
xadmin.site.register(Rank13Coefficent, Rank13CoefficentAdmin)

