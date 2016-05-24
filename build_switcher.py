from sublime_plugin import WindowCommand


class BuildSwitcherCommand(WindowCommand):

    def __init__(self, window):
        WindowCommand.__init__(self, window)
        self.available_systems = {};

    def _reload_settings(self, settingsName):
        settings = self.window.active_view().settings()
        self.available_systems[settingsName] = settings.get(settingsName)


    def run(self, settingsName):
        settingsName = settingsName or "build_switcher_systems"
        win = self.window

        settings = self.window.active_view().settings()
        settings.add_on_change(settingsName, self._reload_settings)
        self._reload_settings(settingsName)

        if not self.available_systems[settingsName]:
            # no switcher builds - just do selected build
            win.run_command("build")
        elif len(self.available_systems[settingsName]) is 1:
            # only one build system - just run it
            self._run_build(settingsName, 0)
        else:
            # more options, show the popup
            win.show_quick_panel(self.available_systems[settingsName], lambda idx: self._run_build(settingsName, idx))


    def _run_build(self, settingsName, idx):
        # the dialog was cancelled
        if idx is -1: return

        item = self.available_systems[settingsName][idx]
        if isinstance(item, list):
            system = item[0].partition("#")
            build = item[1]
        else:
            system = item.partition("#")
            build = system[0]

        self.window.run_command("set_build_system", {"file": build})
        if system[1]:
            self.window.run_command("build", {"variant": system[2]})
        else:
            self.window.run_command("build")

        # move the last used system to first position
        self.available_systems[settingsName].insert(0, self.available_systems[settingsName].pop(idx))


    def is_enabled(self):
        return True


    def description(self):
        return "Pop up a dialog with available build commands."
