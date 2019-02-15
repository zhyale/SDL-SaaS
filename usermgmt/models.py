#coding=utf-8
from django.db import models

# Create your models here.
# domain_name.com
class Company(models.Model):
    top_domain_name=models.CharField(max_length=128, unique=True)
    abbr=models.CharField(max_length=32,blank=True,null=True)
    name=models.CharField(max_length=128,blank=True,null=True)

    def __unicode__(self):
        return self.top_domain_name


class Tag(models.Model):
    name=models.CharField(max_length=128)


class User(models.Model):
    username=models.CharField(max_length=64)
    # salt=base64.b64encode(os.urandom(6))
    salt=models.CharField(max_length=8,default='eUAmmjNo')
    # password=hashlib.sha512(pwd+salt).hexdigest()
    hashpwd=models.CharField(max_length=128, default='0cf521620fff49efec6774413ac4d0aa3b389a9526b9d5604cf204d998b5c6307446ebd417c5234d5b52de4d8bf21ab3fe51268b70930db5411a67a2b858d657') # Flzx3000c
    email=models.EmailField(unique=True)
    email_checked=models.BooleanField(default=True)
    check_code=models.CharField(max_length=8, blank=True, null=True)
    nickname=models.CharField(max_length=64,blank=True,null=True, default='匿名')
    mobile=models.CharField(max_length=32,blank=True,null=True)
    company=models.ForeignKey(Company, related_name='company_users')
    location=models.CharField(max_length=512,blank=True,null=True)
    department=models.CharField(max_length=512,blank=True,null=True)
    introduction=models.CharField(max_length=1024,blank=True,null=True)
    last_login_time=models.DateTimeField(blank=True,null=True, auto_now=True)
    last_login_ip=models.CharField(max_length=128,blank=True,null=True)
    avatar_link=models.CharField(max_length=512, blank=True,null=True)
    need_modify_pwd=models.BooleanField(default=False)
    career_tags=models.ManyToManyField(Tag, related_name='tag_users', blank=True) # career circles
    default_team=models.ForeignKey('Team', blank=True, null=True, related_name='default_team_users')

    def __unicode__(self):
            return self.username

    def display_avatar_link(self):
        #return self.avatar_link if self.avatar_link else "/media/upload/avatars/thumb/default.jpg"
        return self.avatar_link or "/media/upload/avatars/thumb/default.jpg"

    def get_default_team(self):
        if self.default_team:
            return self.default_team
        _teams=self.member_teams.all()
        if _teams:
            return _teams[0]
        else:
            return None


# Organization unit, such as product team or department
class Team(models.Model):
    name=models.CharField(max_length=128)
    company=models.ForeignKey(Company, related_name='company_teams')
    abbr=models.CharField(max_length=32) # XL-AC
    admins=models.ManyToManyField(User, blank=True, related_name='admin_teams')
    members=models.ManyToManyField(User,blank=True, related_name='member_teams')
    create_date=models.DateField(auto_now_add=True)
    vip_expire_date=models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class DayStat(models.Model):
    date=models.DateField(auto_now_add=True)
    pv=models.IntegerField()
    visitors=models.ManyToManyField(User, blank=True)

    def uv(self):
        return self.visitors.count()
