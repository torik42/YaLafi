"
" Author: Matthias Baumann
" Description: LanguageTool with YaLafi as LaTeX filter
"
" TODO:
" - use JSON (currently text) interface: better highlighting if length
"   of error in plain text differs from length of corresponding text
"   in LaTeX source
"   --> vimscript has json_decode()
"   --> yalafi.shell: include fields fromx, fromy, tox, toy into JSON output,
"       as for XML output
" - pipe buffer content to stdin (currently: temp file)
"   --> yalafi.shell: add reading from stdin
"

call ale#Set('tex_lty_ltdirectory', '~/lib/LanguageTool')
call ale#Set('tex_lty_language', 'en-GB')
call ale#Set('tex_lty_disable', 'WHITESPACE_RULE')
call ale#Set('tex_lty_shelloptions', '')
call ale#Set('tex_lty_server', 'my')
 
call ale#Set('tex_lty_executable', 'python')
call ale#Set('tex_lty_options',
    \   ' -m yalafi.shell'
    \ . ' --output plain'
    \ . ' --lt-directory ' . g:ale_tex_lty_ltdirectory
    \ . (empty(g:ale_tex_lty_server) ?
                \ '' : ' --server ' . g:ale_tex_lty_server)
    \ . ' --language ' . g:ale_tex_lty_language
    \ . ' --disable ' . g:ale_tex_lty_disable
    \ . ' ' . g:ale_tex_lty_shelloptions
\)

function! ale_linters#tex#lty#GetExecutable(buffer) abort
    return ale#Var(a:buffer, 'tex_lty_executable')
endfunction

function! ale_linters#tex#lty#GetCommand(buffer) abort
    let l:executable = ale_linters#tex#lty#GetExecutable(a:buffer)
    let l:options = ale#Var(a:buffer, 'tex_lty_options')

    return ale#Escape(l:executable)
    \ . (empty(l:options) ? '' : ' ' . l:options) . ' %t'
endfunction

"
"   Parse text report from yalafi.shell.
"   This is taken from autoload/ale/handlers/languagetool.vim
"   Author: Vincent (wahrwolf [at] wolfpit.net)
"
function! ale_linters#tex#lty#Handle(buffer, lines) abort
    " Match lines like:
    " 1.) Line 5, column 1, Rule ID:
    let l:head_pattern = '^\v.+.\) Line (\d+), column (\d+), Rule ID. (.+)$'
    let l:head_matches = ale#util#GetMatches(a:lines, l:head_pattern)

    " Match lines like:
    " Message: Did you forget a comma after a conjunctive/linking adverb?
    let l:message_pattern = '^\vMessage. (.+)$'
    let l:message_matches = ale#util#GetMatches(a:lines, l:message_pattern)

    " Match lines like:
    "   ^^^^^ "
    let l:markers_pattern = '^\v *(\^+) *$'
    let l:markers_matches = ale#util#GetMatches(a:lines, l:markers_pattern)

    let l:output = []


    " Okay tbh I was to lazy to figure out a smarter solution here
    " We just check that the arrays are same sized and merge everything
    " together
    let l:i = 0

    while l:i < len(l:head_matches)
    \   && (
    \       (len(l:head_matches) == len(l:markers_matches))
    \       && (len(l:head_matches) == len(l:message_matches))
    \   )
        let l:item = {
        \   'lnum'    : str2nr(l:head_matches[l:i][1]),
        \   'col'     : str2nr(l:head_matches[l:i][2]),
        \   'end_col' : str2nr(l:head_matches[l:i][2]) + len(l:markers_matches[l:i][1])-1,
        \   'type'    : 'E',
        \   'code'    : l:head_matches[l:i][3],
        \   'text'    : l:message_matches[l:i][1]
        \}
        call add(l:output, l:item)
        let l:i+=1
    endwhile

    return l:output
endfunction

call ale#linter#Define('tex', {
    \   'name': 'lty',
    \   'executable': function('ale_linters#tex#lty#GetExecutable'),
    \   'command': function('ale_linters#tex#lty#GetCommand'),
    \   'output_stream': 'stdout',
    \   'callback': 'ale_linters#tex#lty#Handle',
    \   'lint_file': 0,
    \   'read_buffer': 0,
    \   'read_temporary_file': 1,
\})

