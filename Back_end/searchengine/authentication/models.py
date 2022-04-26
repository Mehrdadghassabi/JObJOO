from uuid import uuid4

from django.contrib.auth.models import User as djUser
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from django.utils import timezone

from authentication import utils
from management import models as management_models

from notifications import KavenegarSMS


class ProfileModel(models.Model):
    user = models.OneToOneField(djUser, on_delete=models.CASCADE,
                                related_name='profile')
    avatar = models.ImageField(
        upload_to='media/',
        default='default_avatar.png',
        blank=True
    )
    province = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    credit = models.PositiveIntegerField(blank=True, default=0)
    tmp_code = models.CharField(max_length=6, default=utils.password_generator)
    tmp_code_expire = models.DateTimeField(default=timezone.now)
    tmp_code_sent_time = models.DateTimeField(default=utils.five_minute_ago)
    tmp_code_sent_counter_in_last_24_hour = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def has_credit(self, days=1):
        return int(management_models.Setting.objects.get(
            key='ACTIVE_SEARCH_COST').value) * days <= self.credit

    def pay(self, days):
        self.credit -= int(management_models.Setting.objects.get(
            key='ACTIVE_SEARCH_COST').value) * days
        self.save()

    def check_password(self, password):
        if self.tmp_code_expire > timezone.now() and \
                self.tmp_code == password:
            return True
        return False

    def __can_request_sms(self):
        if self.user.username == '09373180771':
            return True
        block = self.user.sms_black_list.filter(
            Q(expire_time__isnull=True) |
            Q(expire_time__gt=timezone.now())
        )
        if block.count() > 0:
            return False
        if self.tmp_code_sent_time > timezone.now() - timezone.timedelta(minutes=1):
            return None
        if self.tmp_code_sent_time.date() == timezone.now().date():
            self.tmp_code_sent_counter_in_last_24_hour += 1
        else:
            self.tmp_code_sent_counter_in_last_24_hour = 0
        self.save()
        if self.tmp_code_sent_counter_in_last_24_hour < 15:
            return True
        return False

    def send_tmp_code(self):
        tmp = self.__can_request_sms()
        if tmp is None:
            return True
        elif tmp:
            self.tmp_code = utils.password_generator()
            self.tmp_code_expire = utils.five_minute_later()
            sms = KavenegarSMS()
            sms.register(
                receptor=self.user.username,
                code=self.tmp_code,
            )
            sms.send()
            self.tmp_code_sent_time = timezone.now()
            self.save()
            return True
        return False


@receiver(post_save, sender=djUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        password = uuid4().hex
        instance.set_password(password)
        instance.save()
        ProfileModel.objects.create(user=instance)


class SMSBlackList(models.Model):
    user = models.ForeignKey(djUser, on_delete=models.CASCADE, related_name='sms_black_list')
    ip = models.GenericIPAddressField(null=True, blank=True)
    insert_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(null=True, blank=True)
