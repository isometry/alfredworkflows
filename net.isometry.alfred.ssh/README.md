# ssh workflow by isometry

A workflow for [Alfred](http://www.alfredapp.com/) Powerpack users to rapidly open Secure SHell (ssh) sessions with smart hostname autocompletion based on the contents of `~/.ssh/known_hosts`, `~/.ssh/config`, `/etc/hosts` and (optionally) Bonjour.

![Example 1](https://raw.github.com/isometry/alfredworkflows/master/screenshots/ssh_local.png)

![Example 2](https://raw.github.com/isometry/alfredworkflows/master/screenshots/ssh_user@local.png)

## Download
- Alfred 2 workflow: [ssh.alfredworkflow](https://raw.github.com/isometry/alfredworkflows/master/ssh.alfredworkflow) (v1.3)
- Alfred 3 workflow: [ssh.alfred3workflow](https://raw.github.com/isometry/alfredworkflows/master/ssh.alfred3workflow) (v2.0)

## Prerequisites

- [Alfred](http://www.alfredapp.com/) (version 2.4+)
- The [Alfred Powerpack](http://www.alfredapp.com/powerpack/).
- (optional) [pybonjour](https://pypi.python.org/pypi/pybonjour)

## Usage

Type `ssh` in Alfred followed by either a literal hostname or by some letters from the hostname of a host referenced in any of `~/.ssh/known_hosts`, `~/.ssh/config`, `/etc/hosts`, or (with `pybonjour` installed) Bonjour.

Alfred 3 only: workflow configuration is available by setting/changing Workflow Environment Variables (accessed via the [𝓍] button within the workflow):
- disable unwanted sources by setting the associated Workflow Environment Variable to 0; e.g. `alfredssh_known_hosts`, `alfredssh_ssh_config`, `alfredssh_hosts`, `alfredssh_bonjour`.
- change the maximum number of returned results by changing `alfredssh_max_results` (default=36).
- add additional files listing valid host completions (e.g. for pre-seeding) by adding space-separated short-name=~/file/path entries to the `alfredssh_extra_files` Workflow Environment Variable. Lines beginning with `#` are ignored, all other whitespace separated words are assumed to be valid hostnames.

If you wish to have [iTerm2](https://www.iterm2.com/) act as ssh protocol handler rather than Terminal.app, create a new iTerm2 profile with “Name” `$$USER$$@$$HOST$$`, “Command” `$$` and “Schemes handled” `ssh` (e.g. [here](http://apple.stackexchange.com/questions/28938/set-iterm2-as-the-ssh-url-handler) and [here](http://www.alfredforum.com/topic/826-ssh-with-smart-hostname-autocompletion/#entry4147)).

## Contributions & Thanks

- [nikipore](https://github.com/nikipore)

## License

(The MIT License)

Copyright (c) 2013-2016 Robin Breathe

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
