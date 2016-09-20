from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager as DefaultUserManager
from django.db.models import Avg, F
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from base.mixins import FieldsMixin


class UserManager(DefaultUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        "Returns the short name for the user."
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class WotAccount(models.Model):
    account_id = models.IntegerField(unique=True, db_index=True)
    nickname = models.CharField(max_length=256, unique=True, db_index=True)

    def __unicode__(self):
        return "%s %d" % (self.nickname, self.account_id)


class Tank(models.Model):
    tank_id = models.IntegerField(unique=True)
    accounts = models.ManyToManyField(WotAccount, related_name='tanks')

    avg_draws = models.FloatField(default=0.0)
    avg_losses = models.FloatField(default=0.0)
    avg_wins = models.FloatField(default=0.0)
    avg_frags = models.FloatField(default=0.0)
    avg_survived_battles = models.FloatField(default=0.0)


    probability_of_survival = models.FloatField(default=0.0)
    probability_of_losses = models.FloatField(default=0.0)
    probability_of_wins = models.FloatField(default=0.0)
    probability_of_draws = models.FloatField(default=0.0)


    def update_general_statistic(self):
        statistic_objects = self.tankstatistic_set.all()
        count_of_statistics = len(statistic_objects)

        t = TankStatistic.objects.raw('SELECT DISTINCT ON (a.tank_id) *, b.max FROM base_tankstatistic AS a '
                                      'INNER JOIN ('
                                      '   SELECT account_id, tank_id, MAX(battles) AS max FROM base_tankstatistic '
                                      '   GROUP BY account_id, tank_id'
                                      ') AS b ON a.account_id = b.account_id AND a.tank_id = b.tank_id '
                                      'WHERE a.battles = b.max')
        t = list(t)


        values = {
            'avg_wins': Avg(F('wins')/F('battles')),
            'avg_losses': Avg(F('losses')/F('battles')),
            'avg_draws': Avg(F('draws')/F('losses')),

        }

        self.tankstatistic_set.values('tank_id' ).aggregate(avg_draws=Avg('draws'), avg_wins=Avg('wins'), avg_losses=Avg('losses'))


class ObjectStatisticManager(models.Manager):

    def build_from_api_object(self, api_obj, commit=True):
        """
        :param commit: save object to db permanently
        :type api_obj: wot_api.objects.AccountInfo
        :type commit: bool
        :rtype: wot_api.objects.ApiObject
        """
        namespaces = ['statistics__all__', 'all__']
        fields = self.model.get_field_names()
        data = {}
        for field_name in fields:
            for namespace in namespaces:
                field_name_with_namespace = namespace + field_name
                if hasattr(api_obj, field_name_with_namespace):
                    data[field_name] = getattr(api_obj, field_name_with_namespace)
                elif hasattr(api_obj, field_name):
                    data[field_name] = getattr(api_obj, field_name)
        obj = self.model(**data)
        if commit:
            obj.save()
        return obj


class TankStatistic(FieldsMixin, models.Model):
    excluded_fields = ('id', 'account', 'tank')

    account = models.ForeignKey(WotAccount, to_field='account_id', db_index=True)
    tank = models.ForeignKey(Tank, to_field='tank_id', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    mark_of_mastery = models.IntegerField()
    max_frags = models.IntegerField()
    max_xp = models.IntegerField()
    avg_damage_blocked = models.FloatField()
    battle_avg_xp = models.FloatField()
    battles = models.FloatField()
    capture_points = models.IntegerField()
    damage_dealt = models.IntegerField()
    damage_received = models.IntegerField()

    draws = models.IntegerField()
    losses = models.IntegerField()
    wins = models.IntegerField()

    frags = models.IntegerField()

    survived_battles = models.IntegerField()

    objects = ObjectStatisticManager()


class AccountStatistic(FieldsMixin, models.Model):
    excluded_fields = ('id', 'account', 'created_at')

    account = models.ForeignKey(WotAccount, to_field='account_id', related_name='statistics')
    created_at = models.DateTimeField(auto_now_add=True)

    global_rating = models.IntegerField()

    avg_damage_assisted = models.FloatField()
    avg_damage_assisted_radio = models.FloatField()
    avg_damage_assisted_track = models.FloatField()
    avg_damage_blocked = models.FloatField()

    battle_avg_xp = models.IntegerField()
    capture_points = models.IntegerField()
    damage_dealt = models.IntegerField()
    damage_received = models.IntegerField()
    direct_hits_received = models.IntegerField()
    dropped_capture_points = models.IntegerField()
    explosion_hits = models.IntegerField()
    explosion_hits_received = models.IntegerField()

    frags = models.IntegerField()
    hits = models.IntegerField()
    hits_percents = models.FloatField()

    max_damage = models.IntegerField()
    max_damage_tank_id = models.IntegerField()
    max_frags = models.IntegerField()
    max_frags_tank_id = models.IntegerField()
    max_xp = models.IntegerField()
    max_xp_tank_id = models.IntegerField()

    shots = models.IntegerField()
    spotted = models.IntegerField()

    survived_battles = models.IntegerField()

    draws = models.IntegerField()
    losses = models.IntegerField()
    wins = models.IntegerField()

    objects = ObjectStatisticManager()
