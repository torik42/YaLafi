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
    let g:ltyc_ltdirectory = '~/lib/LanguageTool'
endif
if !exists("g:ltyc_server")
    let g:ltyc_server = 'my'
endif
if !exists("g:ltyc_language")
    let g:ltyc_language = 'en-GB'
endif
if !exists("g:ltyc_disable")
    let g:ltyc_disable = 'WHITESPACE_RULE'
endif
if !exists("g:ltyc_enable")
    let g:ltyc_enable = ''
endif
if !exists("g:ltyc_disablecategories")
    let g:ltyc_disablecategories = ''
endif
if !exists("g:ltyc_enablecategories")
    let g:ltyc_enablecategories = ''
endif
if !exists("g:ltyc_shelloptions")
    let g:ltyc_shelloptions = ''
endif
if !exists("g:ltyc_showsuggestions")
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
if g:ltyc_server != 'lt'
    if !executable('java')
        echoerr s:pref . 'install Java.'
        finish
    endif
    if !filereadable(fnamemodify(g:ltyc_ltdirectory
                            \ . '/languagetool-commandline.jar', ':p'))
        echoerr s:pref . 'set g:ltyc_ltdirectory to the'
                    \ . ' path of LanguageTool.'
        finish
    endif
endif

let &l:makeprg =
        \ 'python -m yalafi.shell'
        \ . ' --lt-directory ' . g:ltyc_ltdirectory
        \ . (g:ltyc_server == '' ? 
                    \ '' : ' --server ' . g:ltyc_server)
        \ . ' --language ' . g:ltyc_language
        \ . ' --disable "' . g:ltyc_disable . '"'
        \ . ' --enable "' . g:ltyc_enable . '"'
        \ . ' --disablecategories "' . g:ltyc_disablecategories . '"'
        \ . ' --enablecategories "' . g:ltyc_enablecategories . '"'
        \ . ' ' . g:ltyc_shelloptions
        \ . ' %:S'

let &l:errorformat = '%I=== %f ===,%C%*\d.) Line %l\, column %v\, Rule ID:%.%#,'
if g:ltyc_showsuggestions == 0
  let &l:errorformat .= '%ZMessage: %m,%-G%.%#'
else
  let &l:errorformat .= '%CMessage: %m,%Z%m,%-G%.%#'
endif

silent CompilerSet makeprg
silent CompilerSet errorformat

let &cpo = s:cpo_save
unlet s:cpo_save

