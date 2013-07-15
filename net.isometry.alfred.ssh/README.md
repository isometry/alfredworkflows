# ssh workflow by isometry

A workflow for [Alfred](http://www.alfredapp.com/) to rapidly open a Secure SHell (ssh) sessions with smart hostname autocompletion based on the contents of `~/.ssh/known_hosts`, `~/.ssh/config`, `/etc/hosts` and (optionally) Bonjour.

![Example 1](https://raw.github.com/isometry/alfredworkflows/master/screenshots/ssh_local.png)

![Example 2](https://raw.github.com/isometry/alfredworkflows/master/screenshots/ssh_user@local.png)

## Requirements

- [Alfred](http://www.alfredapp.com/) (version 2.0+)
- The [Alfred Powerpack](http://www.alfredapp.com/powerpack/).
- [ssh.alfredworkflow](https://raw.github.com/isometry/alfredworkflows/master/ssh.alfredworkflow)
- (optional) [pybonjour](https://pypi.python.org/pypi/pybonjour)

## Usage

Type `ssh` in Alfred followed by either a literal hostname or by some letters from the hostname of a host referenced in any of `~/.ssh/known_hosts`, `~/.ssh/config`, `/etc/hosts`, or (with `pybonjour` installed) Bonjour.

If you wish to use iTerm rather than Terminal.app, instructions for overriding the ssh protocol handler can be found [here](http://apple.stackexchange.com/questions/28938/set-iterm2-as-the-ssh-url-handler) and [here](http://www.alfredforum.com/topic/826-ssh-with-smart-hostname-autocompletion/#entry4147)

## Contributions & Thanks

- [nikipore](https://github.com/nikipore)

## License

(The MIT License)

Copyright (c) 2013 Robin Breathe

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
