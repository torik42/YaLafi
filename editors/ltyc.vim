"
"   ltyc: a "compiler" for Vim,
"         invokes LanguageTool with YaLafi as LaTeX filter
"

if exists("current_compiler")
    finish
endif
let current_compiler = "ltyc"

" older Vim always used :setlocal
if exists(':CompilerSet') != 2
    command -nargs=* CompilerSet setlocal <args>
endif

let s:cpo_save = &cpo
set cpo&vim

"   set default values
"
if !exists("g:ltyc_ltdirectory")
    " home of LT software
    let g:ltyc_ltdirectory = '~/lib/LanguageTool'
endif
if !exists("g:ltyc_server")
    " use an LT server?
    let g:ltyc_server = 'my'
endif
if !exists("g:ltyc_encoding")
    " encoding of LaTeX source
    let g:ltyc_encoding = 'auto'
endif
if !exists("g:ltyc_disable")
    " LT option --disable
    let g:ltyc_disable = 'WHITESPACE_RULE'
endif
if !exists("g:ltyc_enable")
    " LT option --enable
    let g:ltyc_enable = ''
endif
if !exists("g:ltyc_disablecategories")
    " LT option --disablecategories
    let g:ltyc_disablecategories = ''
endif
if !exists("g:ltyc_enablecategories")
    " LT option --enablecategories
    let g:ltyc_enablecategories = ''
endif
if !exists("g:ltyc_shelloptions")
    " further options passed to yalafi.shell
    let g:ltyc_shelloptions = ''
endif
if !exists("g:ltyc_showsuggestions")
    " if set to 1: show LT's replacement suggestions
    let g:ltyc_showsuggestions = 0
endif

"   check installation components
"
let s:pref = 'In order to use the ltyc compiler, please '
if !executable('python')
    echoerr s:pref . 'install Python.'
    finish
endif
call system('python -c "import yalafi"')
if v:shell_error != 0
    echoerr s:pref . 'install the Python module YaLafi.'
    finish
endif
if !exists("g:ltyc_ltcommand")
    " alternative LT command
    let g:ltyc_ltcommand = ''
endif
let s:ltyc_ltcommand = ''
if g:ltyc_server != 'lt'
    if !executable('java')
        echoerr s:pref . 'install Java.'
        finish
    endif
    if g:ltyc_ltcommand != ''
        if !executable(g:ltyc_ltcommand)
            echoerr s:pref . 'set g:ltyc_ltcommand correctly.'
            finish
        else
            let s:ltyc_ltcommand = g:ltyc_ltcommand
        endif
    else
        if !filereadable(fnamemodify(g:ltyc_ltdirectory . '/languagetool-commandline.jar', ':p'))
            echoerr s:pref . 'set g:ltyc_ltdirectory to the'
                        \ . ' path of LanguageTool.'
            finish
        else
            let s:ltyc_ltcommand = 'java -jar ' . fnamemodify(g:ltyc_ltdirectory . '/languagetool-commandline.jar', ':p:S')
        endif
    endif
endif

" Guess language if it is not defined
if !exists('g:ltyc_language')
    let spelllangs = split(&spelllang, ',')
    if len(spelllangs) > 1
        echohl WarningMsg | echo 'Please select one of the &spelllang language codes numbered 0,1,...' | echohl None
        let spelllang = spelllangs[inputlist(spelllangs)]
    else
        let spelllang = &spelllang
    endif
    let g:ltyc_language = substitute(spelllang, '_', '-', 'g')
endif

if empty(g:ltyc_language)
    echohl WarningMsg
    echomsg 'Please set g:ltyc_language to enable more accurate'
    echomsg 'checks by LanguageTool. Reverting to --autoDetect.'
    echohl None
    let s:ltyc_language = ' --autoDetect'
else
    let g:ltyc_language = substitute(g:ltyc_language, '_', '-', '')
    let s:ltyc_language = ' --language ' . g:ltyc_language
    if !exists('s:list')
        silent let s:list = split(
                    \ system(s:ltyc_ltcommand . ' --list NOFILE'),
                    \ '[[:space:]]')
    endif
    if !empty(s:list)
        if match(s:list, '\c^' . g:ltyc_language . '$') == -1
            echohl WarningMsg
            echomsg "Language '" . g:ltyc_language . "'"
                        \ . " not listed in output of the command "
                        \ . "'" . s:ltyc_ltcommand . " --list'! "
                        \ . "Please check its output!"
            echohl None
            if match(g:ltyc_language, '-') != -1
                let g:ltyc_language = matchstr(g:ltyc_language, '\v^[^-]+')
                echohl WarningMsg
                echomsg "Trying '" . g:ltyc_language . "' instead."
                echohl None
            else
                echohl WarningMsg
                echomsg "Trying '" . g:ltyc_language . "' anyway."
                echohl None
            endif
        endif
    endif
endif

let &l:makeprg =
        \ 'python -m yalafi.shell'
        \ . ' --lt-command "' . g:ltyc_ltcommand . '"'
        \ . (g:ltyc_ltcommand != '' ?
                    \ '' : ' --lt-directory ' . g:ltyc_ltdirectory)
        \ . (g:ltyc_server == '' ? 
                    \ '' : ' --server ' . g:ltyc_server)
        \ . ' --encoding ' . (g:ltyc_encoding ==# 'auto'
        \    ? (empty(&l:fileencoding) ? &l:encoding : &l:fileencoding)
        \    : g:ltyc_encoding)
        \ . s:ltyc_language
        \ . ' --disable "' . g:ltyc_disable . '"'
        \ . ' --enable "' . g:ltyc_enable . '"'
        \ . ' --disablecategories "' . g:ltyc_disablecategories . '"'
        \ . ' --enablecategories "' . g:ltyc_enablecategories . '"'
        \ . ' ' . g:ltyc_shelloptions
        \ . ' %:S'

let &l:errorformat = '%I=== %f ===,%C%*\d.) Line %l\, column %v\, Rule ID:%.%#,'
if g:ltyc_showsuggestions == 0
  " final duplicated '%-G%.%#': compatibility with vim-dispatch;
  " see issue #199 of vim-dispatch and issue #1854 of vimtex
  let &l:errorformat .= '%ZMessage: %m,%-G%.%#,%-G%.%#'
else
  let &l:errorformat .= '%CMessage: %m,%Z%m,%-G%.%#,%-G%.%#'
endif

silent CompilerSet makeprg
silent CompilerSet errorformat

let &cpo = s:cpo_save
unlet s:cpo_save

