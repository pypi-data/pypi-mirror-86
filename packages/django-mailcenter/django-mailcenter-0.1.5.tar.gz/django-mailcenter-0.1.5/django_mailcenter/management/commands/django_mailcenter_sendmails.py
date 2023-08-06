import time
import djclick as click
from fastutils import sysutils

from django_simpletask.services import SimpleTaskService
from django_db_lock.client import get_default_lock_service

from django_mailcenter.models import MailForDelivery

@click.command()
@click.option("-n", "--number", type=int, default=10, help="How many tasks to fetch at one time.")
def sendmails(number):
    lock_service = get_default_lock_service()
    mail_delivery_service = SimpleTaskService.serve(MailForDelivery, lock_service, "Django.Management.Commands.django-mailcenter-sendmails")
    mail_delivery_service.serve_forever()


if __name__ == "__main__":
    sendmails()
