from django.db import migrations

def set_user_for_existing_mailings(apps, _schema_editor):
    Mailing = apps.get_model('mailing', 'Mailing')
    User = apps.get_model('users', 'User')
    # Назначаем всем рассылкам пользователя с id=1 (админ)
    default_user = User.objects.filter(id=1).first()
    if default_user:
        for mailing in Mailing.objects.filter(user__isnull=True):
            mailing.user = default_user
            mailing.save()

class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0012_mailing_user'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_user_for_existing_mailings),
    ]
