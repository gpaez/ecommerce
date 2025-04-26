# tienda/mixins.py (crealo si no existe)

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class SoloSuperuserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('/')
