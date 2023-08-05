from quakestats.web import (
    api,
)
from quakestats.web.app import (
    app,
    data_store,
    mongo_db,
)

# FIXME mongo shouldn't exposed here
# for now it is due to fact that config file is loaded
# by flask
__all__ = ['app', 'api', 'mongo_db', 'utils', 'data_store']
