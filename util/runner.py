import os
import sublime
import subprocess


class CommandRunner():
    def __init__(self, working_dir):
        self.working_dir = working_dir

    def build_command(self, string):
        settings = sublime.load_settings("TerminalWindow.sublime-settings")
        shell = settings.get("shell")
        for k, v in os.environ.items():
            print("{}: {}".format(k,v))
        print(shell)
        args = ()
        prefix = ""
        if shell == "zsh":
            args = ("-l", "-c")
            prefix = "source ~/.zshrc && "
        elif shell == "bash":
            args = ("-l", "-c")
            prefix = ""
        else:
            pass

        cmd = (shell,) + args + (prefix + string, )
        print(cmd)
        return cmd

    def run(self, string, stdin=None):
        command = self.build_command(string)
        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        env = os.environ
        # env["TERM"] = "xterm-256color"
        # env["TERM"] = "xterm"

        p = subprocess.Popen(command,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             cwd=self.working_dir,
                             env=env,
                             startupinfo=startupinfo)
        stdout, stderr = p.communicate(stdin.encode(encoding="UTF-8") if stdin else None)
        stdout, stderr = stdout.decode(), stderr.decode()

        return stdout, stderr

