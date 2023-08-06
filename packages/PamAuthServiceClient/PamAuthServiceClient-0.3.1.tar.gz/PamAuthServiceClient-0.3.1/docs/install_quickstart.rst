PamAuthServiceClient
====================

Client for the PamAuthService_

Installation
------------

::

   pip install PamAuthServiceClient

Quickstart
----------

Use the ``PamAuthService`` running on a unix socket at
``/run/pam_auth_service.sock``.

(If the ``PamAuthService`` is running on a network socket use ``url``
instead of ``path``)

.. code:: python

   from pamauthserviceclient.client import PamAuthServiceClient

   encryption_key = 'ENCRYPTION KEY'
   verification_key = 'VERIFICATION KEY'

   path = "/run/pam_auth_service.sock"
   # url = "http://127.0.0.1:5000"

   client = PamAuthServiceClient(encryption_key, verification_key, path=path)
   # client = PamAuthServiceClient(encryption_key, verification_key, url=url)

   res = client.authenticate("name", "password")
   # None
   #    if  name/password don't match
   # {'version': '1.0', 'username': 'name', 'allowed_groups': []}
   #    if user/password match

   allowed_groups = ["group1", "xxx", "yyy", "zzz"]

   res2 = client.authenticate("name", "password", allowed_groups)
   # {'version': '1.0', 'username': 'name', 'allowed_groups': ['xxx', 'zzz']}
   #    if user is authorized and member of the 'xxx' and 'zzz' group
   #    and not member of the other groups.

.. _PamAuthService: https://in-stigler.htw-aalen.de/gitea/klauck/PamAuthService
