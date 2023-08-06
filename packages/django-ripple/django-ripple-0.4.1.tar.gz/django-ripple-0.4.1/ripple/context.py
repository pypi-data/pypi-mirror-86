from django.conf import settings


def GlobalConfig(request):
    return {'GA_ACCOUNT_ID': settings.GA_ACCOUNT_ID,
            'GTM_ID': settings.GTM_ID,
            'ALLOW_ROBOTS': settings.ALLOW_ROBOTS,
            'SITE_URL': settings.SITE_URL,
            'HJID': settings.HJID,
            'HJSV': settings.HJSV,
            'DEBUG': ('false', 'true')[settings.DEBUG],
            'FEATURES': ','.join(["'%s'" % i for i in request.session.get('features', [])])
            }
