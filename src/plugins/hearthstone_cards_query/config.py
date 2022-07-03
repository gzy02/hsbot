import nonebot

#系统管理员QQ号、数据库等配置，从.env.dev读取，文件里的大写会被转成小写
driver = nonebot.get_driver()
global_config = driver.config
config = global_config.dict()
SYSTEM_ADMIN_QQ_NUMBER = config['system_admin_qq_number']
DATABASE_NAME = config['database_name']
DATABASE_HOST = config['database_host']
DATABASE_USER = config['database_user']
DATABASE_PASSWORD = config['database_password']
DATABASE_PORT = config['database_port']
DATABASE_CHARSET = config['database_charset']
