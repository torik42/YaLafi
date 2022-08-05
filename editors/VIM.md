We shortly describe important points of the different interfaces to Vim.

## "Plain Vim"
We use the Vim compiler interface, [see README](../master/README.md#plain-vim). The compiler file for Vim is
[editors/ltyc.vim](../master/editors/ltyc.vim).
- expects plain text output from yalafi.shell, this is parsed by Vim's errorformat variable that is set starting at
  [editors/ltyc.vim#116](../master/editors/ltyc.vim#L116)
  - test of this text output format: [tests/test\_shell/test\_shell.py](../master/tests/test_shell/test_shell.py), assertion
    at the end `assert out_txt == expect_txt`
- by default, ltyc.vim passes some options to yalafi.shell, starting at [editors/ltyc.vim#93](../master/editors/ltyc.vim#L93)
   - --lt-command: no automatic test, as far as I can see
   - --lt-server: no test
   - --encoding: [tests/test\_shell\_cmd/test\_lt\_options.py](../master/tests/test_shell_cmd/test_lt_options.py)
   - --language: [tests/test\_shell\_cmd/test\_lt\_options.py](../master/tests/test_shell_cmd/test_lt_options.py)
   - --disable: [tests/test\_shell\_cmd/test\_lt\_options.py](../master/tests/test_shell_cmd/test_lt_options.py)
   - --disablecategories: [tests/test\_shell\_cmd/test\_lt\_options.py](../master/tests/test_shell_cmd/test_lt_options.py)
 - user can specify more options to be passed to yalafi.shell, see the example .vimrc in [README](../master/README.md#plain-vim),
   variable `g:ltyc_shelloptions`, some of them are tested in the above test file
   
 ## VimTeX
   
 TBC
