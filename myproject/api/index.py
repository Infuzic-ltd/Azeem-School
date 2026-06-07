import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings.production")

import django
django.setup()

# Run migrations automatically on every cold start so the DB
# stays in sync with the deployed models on Vercel serverless.
_FLAG = "/tmp/.migrated"
if not os.path.exists(_FLAG):
    try:
        from django.core.management import call_command
        call_command("migrate", "--no-input", verbosity=0)
        open(_FLAG, "w").close()
    except Exception as e:
        import sys
        print(f"[migrate] warning: {e}", file=sys.stderr)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
