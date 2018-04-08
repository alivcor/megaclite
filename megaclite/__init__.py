from notebook.base.handlers import IPythonHandler
from notebook.utils import url_path_join
import os
import json, requests
from subprocess import Popen, PIPE
import logging
from .megaclite_config import *

logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)


def _jupyter_server_extension_paths():
    """
    This allows use of
        jupyter serverextension enable --py megaclite --sys-prefix
    :return: module
    """
    return [{
        "module": "megaclite"
    }]




def _jupyter_nbextension_paths():
    """
    Handler to load the Javascript elements
    :return:
    """
    return [dict(
        section="notebook",
        src="static",
        dest="megaclite",
        require="megaclite/index"
    )]




def killNotebookSession(username):
    session = requests.Session()
    session.trust_env = False
    r = session.delete(api_url + "/users/" + username + "/servrer",
                       headers={
                           'Authorization': 'token %s' % token,
                           'Content-Type': 'application/json'
                       })
    logger.debug('Sent Request: %s', str(r.__dict__))
    r.raise_for_status()
    users_info = r.json()
    logger.debug('Received Response: %s', str(users_info))
    return True




def monitorUsage(username, memory_usage):
    logger.info("user : " + username + " | usage : %s", str(memory_usage))
    if(memory_usage > 1.2*memory_limit):
        logger.debug("Killing Notebook Session for user: %s. Surpassed Limits", username)
        killed = killNotebookSession(username)
        if not killed:
            logger.debug("Error killing notebook session for user: %s", username)


def fetchUsage(username):
    memory_usage = float(Popen("ps uU " + username + "| grep jup | awk '{sum=sum+$6}; END {print sum/(1024)}'", shell=True, stdout=PIPE).stdout.read().decode("utf-8").strip())
    monitorUsage(username, memory_usage)
    return memory_usage


def _build_msg_json(**kwargs):
    return dict(**kwargs)

class Megaclite(IPythonHandler):
    def get(self, username):
        try:
            usage_val = fetchUsage(username=username)
            logger.debug("fetched usage_val : %s", str(usage_val))
            if usage_val > memory_limit:
                self.finish(_build_msg_json(title="Memory Limits Surpassed", body="You are currently using "  + str(usage_val), actual_val=usage_val, zone="A"))
            elif usage_val > 0.75*memory_limit:
                self.finish(_build_msg_json(title="Approaching Memory Limits", body="You are currently using " + str(usage_val), actual_val=usage_val, zone="W"))
            else:
                self.finish(_build_msg_json(title="Current Memory Usage", body="You are currently using " + str(usage_val), actual_val=usage_val, zone="S"))
        except:
            self.finish(json.dumps("Jupyter has many moons. Maybe double check your orbit. Megaclite is 148° to Jupiter's equator"))




def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    :param nb_server_app:  NotebookWebApplication
    :return:
    """
    here = os.path.dirname(__file__)
    nb_server_app.log.info("\n\n Megaclite Jupyter Extension loaded from %s \n\n" % here)
    jupyter_orbit = nb_server_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(jupyter_orbit.settings['base_url'], '/megaclite/(.*)')
    jupyter_orbit.add_handlers(host_pattern, [(route_pattern, Megaclite)])
