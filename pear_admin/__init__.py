from flask import Flask, render_template

from configs import config
from pear_admin.apis import register_apis
from pear_admin.extensions import register_extensions
from pear_admin.orms import DepartmentORM
from pear_admin.views import register_views


def create_app(config_name="dev"):
    app = Flask("pear_admin_flask")
    app.config.from_object(config.get(config_name))

    # 注册插件
    register_extensions(app)

    # 注册蓝图
    register_views(app)

    # 注册 api
    register_apis(app)
    return app
