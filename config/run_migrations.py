from django.core.management import call_command
from django.http import HttpResponse

def run_migrations(request):
    call_command("migrate")
    return HttpResponse("Migrations applied!")
