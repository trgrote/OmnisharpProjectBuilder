import sublime, sublime_plugin, json, os

# Default - must have settings
# TODO: Put this in a config file that users can choose to modify
omni_sharp_default_dict = { "folders": [ { "follow_symlinks": "true", "path": "." } ], "solution_file": "" }

# Command for Building Omnisharp Project
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

		proj_path = os.path.dirname( os.path.realpath( proj_name ) )

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

# Listens for anytime somebody loads up a *sln file
# When you run 'Sync Mono Project' in Unity, for example.
class SLNProjectListener( sublime_plugin.EventListener ):
	def on_load(self, view):
		print ( "OmnisharpProjectBuilder: Loaded File: " + view.file_name() )

		# IF the file loaded is an SLN, then kick it off
		if view.file_name().endswith(".sln") and not view.file_name().endswith("-csharp.sln") :
			
			proj_name = view.window().project_file_name()
			proj_path = ""
			solution_file = view.file_name()
			solution_file_path = os.path.dirname( os.path.realpath( solution_file ) )

			# If we don't have a project already loaded, then prompt the user to make one
			if proj_name == None or proj_name == "":
				user_requested_save_project = sublime.ok_cancel_dialog( "Would you like to build an Omnisharp project, based off this Solution?", "Yes, Save Project As ...")
				if user_requested_save_project:
					view.window().run_command( "save_project_as" )
					
				proj_name = view.window().project_file_name()
				# If project is still null, that means they didn't save the project, those fucking LIARS
				if proj_name == None or proj_name == "":
					print ( "OmnisharpProjectBuilder: User Chose not to make Project, exiting" )
					return
				else:
					print ( "OmnisharpProjectBuilder: User Saved New Project, continuing" )
					proj_path = os.path.dirname( os.path.realpath( proj_name ) )    # Regrab path
				
				# Edit the Project Settings to refer to the solution ( relative path )
				print ( "OmnisharpProjectBuilder: Project Path: " + proj_path )
				print ( "OmnisharpProjectBuilder: Solution File Path: " + solution_file_path )

				# Find Relative path from project folder to solution file
				rel_solution_file_path = os.path.relpath( solution_file_path, proj_path )
				rel_solution_file_path = rel_solution_file_path.replace( '\\', '/' )  # for the WinDOS
				print ( "OmnisharpProjectBuilder: Relative Solution File Path: " + rel_solution_file_path )

				# Setup Project Data Info
				project_data = omni_sharp_default_dict.copy()

				# Setup Solution Location ( will override anything they've already set )
				project_data[ "solution_file" ] = rel_solution_file_path + "/" + os.path.basename( solution_file )

				# Default Folder Path to the same path as the solution
				project_data[ "folders" ][ 0 ][ "path" ] = rel_solution_file_path

				project_data.update( view.window().project_data() )    # Update the Project Data Info

				# Save Project Data and Display it to user
				view.window().set_project_data( project_data )    # Save the new project settings
				view.window().open_file( proj_name )              # Open Project file to user to see

			# If We already have a project loaded
			else:
				# Check to see if the project already has a solution linked to it
				print ( "OmnisharpProjectBuilder: Project Already Loaded, checking to see if a project is already loaded" )

				project_data = view.window().project_data()
				proj_path = os.path.dirname( os.path.realpath( proj_name ) )

				rel_solution_file_path = os.path.relpath( solution_file_path, proj_path )    # get Relative Solution Path
				rel_solution_file_path = rel_solution_file_path.replace( '\\', '/' )
				rel_solution_file = rel_solution_file_path + "/" + os.path.basename( solution_file )

				# If project data doesn't have a solution file set, or it's not the solution file we just loaded, then ask them if they want to reassocate
				if "solution_file" not in project_data or project_data[ "solution_file" ] == None or project_data[ "solution_file" ] != rel_solution_file:
					
					user_requested_update_project = sublime.ok_cancel_dialog( "Would you like to associate your current project with this Solution?", "Yes")

					if user_requested_update_project:
						project_data[ "solution_file" ] = rel_solution_file
						# Save Project Data and Display it to user
						view.window().set_project_data( project_data )    # Save the new project settings
						view.window().open_file( proj_name )              # Open Project file to user to see



