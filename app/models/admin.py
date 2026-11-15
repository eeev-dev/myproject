import hmac

from flask import current_app
from flask_login import UserMixin

from ..extensions import login_manager


class AdminUser(UserMixin):
    """Единственный пользователь системы. Логин и пароль задаются в .env."""
    id = 'admin'

    @property
    def login(self):
        return current_app.config['ADMIN_LOGIN']

    @staticmethod
    def check(login, password):
        cfg = current_app.config
        if not cfg.get('ADMIN_PASSWORD'):
            return False
        return (hmac.compare_digest(login or '', cfg['ADMIN_LOGIN'])
                and hmac.compare_digest(password or '', cfg['ADMIN_PASSWORD']))


@login_manager.user_loader
def load_user(user_id):
    return AdminUser() if user_id == 'admin' else None
