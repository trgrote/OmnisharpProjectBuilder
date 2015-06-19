# OmnisharpProjectBuilder
Sublime Text Plugin to aid is generating projects for use with Omnisharp.

Intended to be used in conjunction with [Omnisharp Sublime](https://github.com/OmniSharp/omnisharp-sublime)

## How to Use
Run the command `Save as Omnisharp Project` either from the Command Palette or from `Project->Save as Omnisharp Project`

If you currently have a project open, this plugin will attempt to find the `*.sln` solution file in the same directory as your `*sublime-project`.  If it finds one, it will update your project settings to include this as the solution used by Omnisharp.

If you currently are not currently in a project, it will prompt you to save your current session as a new one.  Preferably save your project in the same directory as the solution file (`*.sln` ) you want Omnisharp to use.
