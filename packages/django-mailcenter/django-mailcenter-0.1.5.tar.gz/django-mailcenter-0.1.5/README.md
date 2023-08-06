# django-mailcenter

Django mailcenter application.

## Install

```
pip install django-mailcenter
```

## Usage

**pro/settings.py**

```
INSTALLED_APPS = [
    ...
    'django_static_ace_builds',
    'django_db_lock',
    'django_fastadmin',
    'django_mailcenter',
    ...
]
```

- AceWidget used for options editor, so we needs `django_static_ace_builds` to provide ace-builds static files, and `django_fastadmin.widgets.AceWidget`.
- models.MailForDelivery as based on `django_fastadmin.models.SimpleTask` and it use `django_db_lock` to do distribute lock.


## Releases

### v0.1.5 2020/11/27

- Fix MailForDeliveryAdmin search filed problem.

### v0.1.4 2020/11/23

- Fix model import problem.

### v0.1.3 2020/09/08

- Add django_mailcenter.client module.
- Upgrade SimpleTask base class.
- Use abstract models classes.

### v0.1.2 2020/09/01

- Rename zh_hans to zh_Hans.
- Update depends packages' version.

### v0.1.1 2020/09/01

- Add many required packages in requirements.txt.

### v0.1.0 2020/08/31

- First release.
