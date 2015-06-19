import sublime, sublime_plugin, json, os

# Default - must have settings
# TODO: Put this in a config file that users can choose to modify
omni_sharp_default_dict = { "folders": [ { "follow_symlinks": "true", "path": "." } ], "solution_file": "" }

# how to test:
# view.run_command( 'build_omnisharp_project' )
class BuildOmnisharpProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		proj_name = self.view.window().project_file_name()
		proj_path = ""
		solution_file = ""

		# If We aren't in a project, then we need to prompt the user to make one
		if proj_name == None or proj_name == "":
			print ( "OmnisharpProjectBuilder: Project Not Found, prompting user to make one" )
			user_requested_save_project = sublime.ok_cancel_dialog( "Not currently in a project, would you like to save this current session as a project?", "Yes, Save Project As ...")
			
			print( user_requested_save_project )

			if user_requested_save_project:
				print ("Prompting now ...")
				self.view.window().run_command( "save_project_as" )
				
			proj_name = self.view.window().project_file_name()

			# If project is still null, that means they didn't save the project, those fucking LIARS
			if proj_name == None or proj_name == "":
				print ( "OmnisharpProjectBuilder: User Chose not to make Project, exiting" )
				return
			else:
				print ( "OmnisharpProjectBuilder: User Saved New Project, continuing" )
				proj_path = os.path.dirname( os.path.realpath(proj_name))    # Regrab path

		else:
			print ( "OmnisharpProjectBuilder: Found Project '%s', continuing" % proj_name )

		proj_path = os.path.dirname( os.path.realpath(proj_name))

		# Prompt user for the Location of their solution file
		# root = tk.Tk()
		# root.withdraw()
		# solution_file = filedialog.askopenfilename()
		# Determine solution's relative path to the project and try to use that instead of the absolute path

		# Attempt to find the solution file ( .sln ) in the same path the project file lives in
		for file in os.listdir( proj_path ):
			if file.endswith(".sln") and not file.endswith("-csharp.sln") :
				solution_file = file

		# Give a warning to the user
		if solution_file == "":
			sublime.error_message( "OmnisharpProjectBuilder\nFailed to Find sln file next to the project file, defaulting to blank, please update after ")
		else:
			solution_file = "./" + solution_file

		# Add Required OmniSharp Info to their Project Settings ( don't overwrite what they currently have )
		new_proj_data = omni_sharp_default_dict.copy()		
		new_proj_data.update( self.view.window().project_data() )    # Add the OmniSharp Info

		# Setup Solution Location ( will override anything they've already set )
		new_proj_data[ "solution_file" ] = solution_file

		self.view.window().set_project_data( new_proj_data )    # Save the new project settings
		self.view.window().open_file( proj_name )               # Open Project file to user to see



