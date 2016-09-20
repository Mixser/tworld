from django.contrib import admin
from base.models import WotAccount, AccountStatistic, TankStatistic


class AccountStatisticModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )

admin.site.register(WotAccount)
admin.site.register(TankStatistic)
admin.site.register(AccountStatistic, AccountStatisticModelAdmin)
