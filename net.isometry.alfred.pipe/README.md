# pipe workflows by isometry

A workflow for [Alfred](http://www.alfredapp.com/) to transform the currently selected text or the contents of the clipboard by passing it through an arbitrary shell one-liner.

## Requirements

- [Alfred](http://www.alfredapp.com/) (version 2.0+)
- The [Alfred Powerpack](http://www.alfredapp.com/powerpack/).
- [pipe.alfredworkflow](https://raw.github.com/isometry/alfredworkflows/pipe.alfredworkflow)

## Usage

(Optional) assign hotkeys for the two Hotkey handlers in the workflow. I recommend `Cmd+Shift+|` and `Cmd+Ctrl+\`, respectively.

Two actions are available, both taking an arbitrarily complex shell pipe as their argument:

1. triggered by the first hotkey or by the `|` or `pipe` keywords, will transform the clipboard in-place by passing its contents through the pipe given as argument.
2. triggered by the second hotkey, will transform the currently selected text in-place by passing its contents through the pipe given as argument.

A number of built-in pipelines are [included](https://raw.github.com/isometry/alfredworkflows/net.isometry.alfred.pipe/builtins.json), and custom aliases can also be defined with the following syntax:

`| alias NAME=PIPE | LINE@@`

`| alias tac=sed '1!G;h;$!d'@@`

## Contributions & Thanks

- ctwise

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