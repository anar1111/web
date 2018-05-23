# Generated by Django 2.0.5 on 2018-05-20 03:57

from django.db import migrations
from django.db.models import Q


def migrate_bounty_owner_profiles(apps, schema_editor):
    Bounty = apps.get_model('dashboard', 'Bounty')
    Profile = apps.get_model('dashboard', 'Profile')
    bounties = Bounty.objects.all()
    profiles = Profile.objects.all()

    for bounty in bounties:
        try:
            bounty.bounty_owner_profile = profiles.filter(
                Q(handle__iexact=bounty.bounty_owner_github_username) |
                Q(handle__iexact=f'@{bounty.bounty_owner_github_username}')
            ).last()
            bounty.save()
        except Profile.DoesNotExist:
            # print('No profile found for ({bounty.bounty_owner_github_username})')
            pass
        except Exception as e:
            print(f'Exception in dashboard migration 0076 - bounty_owner_profiles - ({e}) - {bounty}')


def migrate_tip_profiles(apps, schema_editor):
    Tip = apps.get_model('dashboard', 'Tip')
    Profile = apps.get_model('dashboard', 'Profile')
    tips = Tip.objects.all()
    profiles = Profile.objects.all()

    for tip in tips:
        try:
            tip.recipient_profile = profiles.filter(
                Q(handle__iexact=tip.username) |
                Q(handle__iexact=f'@{tip.username}')
            ).last()
            tip.sender_profile = profiles.filter(
                Q(handle__iexact=tip.from_username) |
                Q(handle__iexact=f'@{tip.from_username}')
            ).last()
            tip.save()
        except Profile.DoesNotExist:
            # print('No profile found for: Recipient ({tip.username}) - Sender ({tip.from_username})')
            pass
        except Exception as e:
            print(f'Exception in dashboard migration 0076 - tip_profiles - ({e}) - {tip}')


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0075_auto_20180520_0349'),
    ]

    operations = [migrations.RunPython(migrate_bounty_owner_profiles), migrations.RunPython(migrate_tip_profiles)]
