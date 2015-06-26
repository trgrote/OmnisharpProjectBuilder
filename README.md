# OmnisharpProjectBuilder
Sublime Text Plugin to aid is generating projects for use with Omnisharp.

Intended to be used in conjunction with [Omnisharp Sublime](https://github.com/OmniSharp/omnisharp-sublime)

## How to Use
1. Run Command to autodetect *sln
  * Run the command `Save as Omnisharp Project` either from the Command Palette or from `Project->Save as Omnisharp Project`
  * If you currently have a project open, this plugin will attempt to find the `*.sln` solution file in the same directory as your `*sublime-project`.  If it finds one, it will update your project settings to include this as the solution used by Omnisharp.
  * If you currently are not currently in a project, it will prompt you to save your current session as a new one.  Preferably save your project in the same directory as the solution file (`*.sln` ) you want Omnisharp to use.
2. Open sln to build or update project
  * Opening *.sln file without of a project - A prompt will appear asking you if you want to make a new project with this solution file.
  * Opening *.sln file with an active project - A prompt will appear asking you if you want to update your project, setting this file as the solution file of the project.
3. Butts
