# Interfaces to Vim

**Note.** For some reason, links of the form \[README#plain-vim\] only work properly when opening in a new browser tab. 

We describe some points of the different interfaces to Vim.
Most important are "Plain Vim", VimTeX, and ALE.
Plugins vim-grammarous and vim-LanguageTool might be less significant.

## "Plain Vim"
We use the Vim compiler interface, [see README#plain-vim](../README.md#plain-vim).
After activating ltyc as compiler, Vim starts yalafi.shell, when the user invokes the command :make.
The compiler file for Vim is [editors/ltyc.vim](../editors/ltyc.vim).
- expects report in plain text format from yalafi.shell, this is parsed by Vim using the errorformat variable that is set
  starting at [editors/ltyc.vim#L116](../editors/ltyc.vim#L116)
  - change of the output format would require adaptation of the errorformat specification, which unfortunately requires
    a bit of "expert knowlege" ;)
  - test of current output format: [tests/test\_shell/test\_shell.py](../tests/test_shell/test_shell.py), assertion
    at the end `assert out_txt == expect_txt`
- by default, ltyc.vim passes some options to yalafi.shell, starting at [editors/ltyc.vim#L98](../editors/ltyc.vim#L98)
   - --lt-command: no automatic test, as far as I can see
   - --lt-server: no test
   - --encoding: [tests/test\_shell\_cmd/test\_lt\_options.py](../tests/test_shell_cmd/test_lt_options.py),
     [tests/test\_shell\_cmd/test\_shell\_encoding.py](../tests/test_shell_cmd/test_shell_encoding.py)
   - --language: [tests/test\_shell\_cmd/test\_lt\_options.py](../tests/test_shell_cmd/test_lt_options.py)
   - --disable: [tests/test\_shell\_cmd/test\_lt\_options.py](../tests/test_shell_cmd/test_lt_options.py)
   - --disablecategories: [tests/test\_shell\_cmd/test\_lt\_options.py](../tests/test_shell_cmd/test_lt_options.py)
 - user can specify more options to be passed to yalafi.shell, see the example vimrc in [README#plain-vim](../README.md#plain-vim),
   variable `g:ltyc_shelloptions`, some of them are tested in the above test test\_lt\_options.py, too
   
 ## Plugin VimTeX
   
This interface uses the same mechanism as described under ["Plain Vim"](#plain-vim), the Vim interface file
[vimtex/compiler/vlty.vim](https://github.com/lervag/vimtex/blob/master/compiler/vlty.vim) is maintained by
[VimTeX](https://github.com/lervag/vimtex), and our copy under editors/ is only for documentation purposes.
- Vim's errorformat variable again is set near the end of the script vlty.vim
- by default, two additional options are passed to yalafi.shell (VimTeX includes mechanisms to
  extract documentclass and loaded packages from the document's root file)
  - --documentclass: apparently no test
  - --packages: apparently no test
- user can again specify more options to be passed to yalafi.shell, see the example vimrc in [README#plugin-vimtex](../README.md#plugin-vimtex),
  variable `g:vimtex_grammar_vlty.shell_options`

## Plugin vim-grammarous

TBD

## Plugin vim-LanguageTool

TBD

## Plugin ALE

This is a different ball game.
During editing, the plugin asynchronously calls yalafi.shell and marks text parts with problems,
just like in an editor as LibreOffice.
(When using Vim with GUI, then we see the normal underlining for errors.)
Corresponding messages from LanguageTool are displayed in the status line, when the cursur hits
the marked text part.

The interface file to be inserted in the ALE distribution is [editors/lty.vim](../editors/lty.vim).
- expects report in JSON format from yalafi.shell
  - uses --output json: currently no automatic test
- passes default options like "Plain Vim" to yalafi.shell
- more options can be specified by user, see the example vimrc in [README#plugin-ale](../README.md#plugin-ale),
  variable `g:ale_tex_lty_shelloptions`


