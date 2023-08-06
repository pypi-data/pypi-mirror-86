import os
import signal
import click
from fastutils import fsutils
from .base import daemon_start
from .base import daemon_stop


class DaemonApplication(object):
    appname = None
    pidfile = None
    workspace = None

    def get_appname(self):
        if self.appname:
            return self.appname
        else:
            return os.path.splitext(os.path.basename(os.sys.argv[0]))[0]

    def get_pidfile(self):
        if self.pidfile:
            return self.pidfile
        else:
            return "{appname}.pid".format(appname=self.get_appname())

    def get_workspace(self):
        if self.workspace:
            return self.workspace
        else:
            return os.path.abspath(os.getcwd())

    def load_config(self):
        return fsutils.load_application_config(appname=self.get_appname())

    def fix_config_pidfile(self, config, pidfile):
        if pidfile:
            config["pidfile"] = pidfile
        else:
            if not "pidfile" in config:
                config["pidfile"] = self.get_pidfile()
    
    def fix_config_daemon(self, config, daemon):
        if not daemon is None:
            config["daemon"] = daemon
        else:
            if not "daemon" in config:
                config["daemon"] = True

    def fix_config_workspace(self, config, workspace):
        if workspace:
            config["workspace"] = workspace
        else:
            if not "workspace" in config:
                config["workspace"] = self.get_workspace()

    def main(self):
        raise NotImplementedError()

    def get_controller(self):

        @click.group()
        @click.option("--pidfile", help="pidfile, default to {}.".format(self.get_pidfile()))
        @click.option("--daemon/--no-daemon", is_flag=True, default=None, help="Run application in background or in foreground.")
        @click.option("--workspace", help="Set running folder, default to {}".format(self.get_workspace()))
        def main(pidfile, daemon, workspace):
            self.config = self.load_config()
            self.fix_config_pidfile(self.config, pidfile)
            self.fix_config_daemon(self.config, daemon)
            self.fix_config_workspace(self.config, workspace)

        @main.command()
        def start():
            """Start daemon application.
            """
            pidfile = self.config["pidfile"]
            daemon = self.config["daemon"]
            workspace = self.config["workspace"]
            daemon_start(self.main, pidfile=pidfile, daemon=daemon, workspace=workspace)

        @main.command()
        @click.option("-s", "--sig", default="SIGTERM", help="Signal send to process, default to SIGTERM")
        def stop(sig):
            """Stop daemon application.
            """
            pidfile = self.config["pidfile"]
            sig = getattr(signal, sig)
            daemon_stop(pidfile, sig=sig)

        @main.command()
        def restart():
            """Restart Daemon application.
            """
            pidfile = self.config["pidfile"]
            stop_signal = self.config["stop_signal"]
            daemon_stop(pidfile, sig=stop_signal)

        @main.command(name="show-config-filepaths")
        def show_config_filepaths():
            """Print out the config searching paths.
            """
            paths = fsutils.get_application_config_paths(self.get_appname())
            print("Application will search config file from follow paths. It will load the first exists file as the config file.")
            for path in paths:
                print("    ", os.path.abspath(path))

        return main
