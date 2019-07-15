import sublime
import sublime_plugin
import base64
import os
import sys
sys.path.append('/usr/lib/python3.7/site-packages')

try:
	import arrow
except:
	...

class NowCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		selection = view.sel()
		for i in range(0,len(selection)):
			view.insert(edit,selection[i].begin(),str(arrow.now()))

class B64encgbkCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ses = self.view.sel()
		for region in ses:
			src = self.view.substr(region)
			src = base64.b64encode(src.encode('gb18030')).decode('utf-8')
			self.view.replace(edit,region,src)

class B64decgbkCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ses = self.view.sel()
		for region in ses:
			src = self.view.substr(region)
			src = base64.b64decode(src.encode('utf-8')).decode('gb18030')
			self.view.replace(edit,region,src)


class SeqNumberCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		selection = view.sel()
		for i in range(0,len(selection)):
			view.insert(edit,selection[i].begin(),str(i))

class DuplicateCommand(sublime_plugin.TextCommand):

	def done(self, value):
		selection = self.view.sel()
		for region in selection:
			src = self.view.substr(region)
			src = src*int(value)
			# self.view.replace(edit,region,src)
			print(src)
		self.view.run_command('insert', {"characters": src})
	def run(self, edit):

		self.view.window().show_input_panel('input pleae', "", self.done, None, None)

class DuplicateExtCommand(sublime_plugin.TextCommand):

	def done(self, value):
		selection = self.view.sel()
		for region in selection:
			src = self.view.substr(region)
			dst = ''
			for v in range(int(value)):
				dst += '%s%d'%(src,v)
			# src = src*int(value)
			# self.view.replace(edit,region,src)
		self.view.run_command('insert', {"characters": dst})
	def run(self, edit):

		self.view.window().show_input_panel('input pleae', "", self.done, None, None)

class UsEditCommand(sublime_plugin.WindowCommand):
	def run(self, reverse=False):
		window = self.window
		window.run_command("show_panel", {"panel": "find"})#打开查找面板
		window.run_command("insert", {"characters": "[\(\)\{\}\$\^\-]"})#输入字符串[\(\)\{\}\$\^\-]
		window.run_command("hide_panel",{"cancel":"true"})#关掉查找面板
		window.run_command("find_all", {"characters": "n"})#查找所有符合的内容
		window.run_command("left_delete")#左删除

class CloseSameCommand(sublime_plugin.TextCommand):
	def run(self, reverse=False):
		view = self.view
		view_name = view.name() or view.file_name() or 'untitled'

		for view in self.view.window().views():
			name = view.name() or view.file_name() or 'untitled'
			if view_name == name:
				view.close()

class CloseMatchCommand(sublime_plugin.WindowCommand):
	def done(self, value):

		# for view in self.window.find_output_panel(value):
		# 	print(view.name() or view.file_name())

		# print('---------------------')
		# for view in self.window.find_open_file(value):
		# 	print(view.name() or view.file_name())

		print('---------------------')
		vs = []
		for view in self.window.views():
			name = view.name() or view.file_name() or 'untitled'
			print(name)
			if value in name:
				self.selected.append(view)
				vs.append(name)

		self.window.show_quick_panel(vs, self.on_done)


				# view.close()
		# print('---------------------')
		# print(value)
	def on_done(self, value):
		for view in self.selected:
			view.close()
	def changed(self, value):
		print(value)
		# self.window.show_quick_panel([[value, value]], lambda x: x)
	
	def canceled(self, value):
		print(value)
	def run(self, reverse=False):
		self.selected = []
		window = self.window
		window.show_input_panel('input pleae', "", self.done, self.changed, self.canceled)


# class CloseMatchCommand(sublime_plugin.WindowCommand):
# 	def done(self, value):
# 		print(value)

# 	def highlighted(self, value):
# 		print('-------------------')
# 		print(value)
# 		self.highlight = value

# 	def run(self, reverse=False):
# 		self.window.show_quick_panel([str(view.name() or view.file_name()) for view in self.window.views()], self.done, sublime.MONOSPACE_FONT, 2, self.highlighted)