from app import app
from loguru import logger

logger.add(
    app.config.get('APP_LOG_FILENAME', '/tmp/app.log'),
    rotation='10 MB', compression='gz', level='DEBUG'
)

logger.opt(exception=True, lazy=True, colors=True, record=True)
# 新增 logger 信息等级, SNAKY 用于调试信息打印备用

logger.level("SNAKY", no=28, color='<MAGENTA>', icon='🐍')
