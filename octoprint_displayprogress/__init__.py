# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.events

class DisplayProgressPlugin(octoprint.plugin.ProgressPlugin,
							octoprint.plugin.EventHandlerPlugin,
							octoprint.plugin.SettingsPlugin,
							octoprint.plugin.TemplatePlugin,
							octoprint.plugin.AssetPlugin):

	##~~ SettingsPlugin
	def on_after_startup(self):
		self._logger.info("Hello World!")

	def get_settings_defaults(self):
		return dict(
			barsymbol="pound",
			message="{bar} {progress:>3}%"
			)

	##~~ TemplatePlugin

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]

	def get_template_vars(self):
		return dict(barsymbol=self._settings.get(["barsymbol"]))

	##~~ AssetPlugin

	def get_assets(self):
		return dict(
			css=["css/displayprogress.css"],
			js=["js/displayprogress.js"]
		)
	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			displayprogress=dict(
				displayName="DisplayProgress Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="OctoPrint",
				repo="OctoPrint-DisplayProgress",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/OctoPrint/OctoPrint-DisplayProgress/archive/{target_version}.zip"
			)
		)

	##~~ EventHandlerPlugin

	def on_event(self, event, payload):
		if event == octoprint.events.Events.PRINT_STARTED:
			self._send_message(payload["origin"], payload["path"], 0)
		elif event == octoprint.events.Events.PRINT_DONE:
			self._send_message(payload["origin"], payload["path"], 100)

	##~~ ProgressPlugin

	def on_print_progress(self, storage, path, progress):
		if not self._printer.is_printing():
			return
		self._send_message(storage, path, progress)

	##~~ helpers

	def _send_message(self, storage, path, progress):
		message = self._settings.get(["message"]).format(progress=progress,
														 storage=storage,
														 path=path,
														 bar=self.__class__._progress_bar(progress))
		self._printer.commands("M117 {}".format(message))

	@classmethod
	def _get_symbol():
		symbol_dict = {
			"bar" : "|",
			"equals" : "=",
			"pound" : "#",
			"tilde" : "~",
			"dash" : "-",
			"underscore" : "_",
			"colon" : ":"
			}

		barSymbol = self._settings.get("barsymbol")
		symbol = symbol_dict.get(barSymbol, "#")
		return symbol

	@classmethod
	def _progress_bar(cls, progress):
		symbols = self.__class__._get_symbol() * int(round(progress / 10))
		spaces = " " * (10 - len(hashes))
		return "[{}{}]".format(symbols, spaces)

__plugin_name__ = "DisplayProgress"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = DisplayProgressPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
