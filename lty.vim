"
" Author: Matthias Baumann
" Description: LanguageTool with YaLafi as LaTeX filter
"
" possible improvements:
" - pipe buffer content to stdin (currently: temp file)
"   --> yalafi.shell: add reading from stdin
"

call ale#Set('tex_lty_ltdirectory', '~/lib/LanguageTool')
call ale#Set('tex_lty_language', 'en-GB')
call ale#Set('tex_lty_disable', 'WHITESPACE_RULE')
call ale#Set('tex_lty_shelloptions', '')
call ale#Set('tex_lty_server', 'my')
call ale#Set('tex_lty_code', 'LT')      " displayed in status line
 
call ale#Set('tex_lty_executable', 'python')
call ale#Set('tex_lty_options',
    \   ' -m yalafi.shell'
    \ . ' --output json'
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

function! ale_linters#tex#lty#Handle(buffer, lines) abort
    let l:report = json_decode(a:lines[0])
    let l:output = []
    for l:match in l:report['matches']
        let l:lin = l:match['priv']['fromy'] + 1
        let l:col = l:match['priv']['fromx'] + 1
        let l:rule = l:match['rule']['id']
                        \ . (has_key(l:match['rule'], 'subId') ?
                        \ '[' . l:match['rule']['subId'] . ']': '')
        let l:replacements = []
        for l:repl in l:match['replacements']
            call add(l:replacements, l:repl['value'])
        endfor 
        let l:context = l:match['context']
        let l:mark = repeat(' ', l:context['offset'])
                    \ . repeat('^', l:context['length'])
        let l:detail = 'Line ' . l:lin . ', column ' . l:col
                    \ . ', rule ID ' . l:rule . "\n"
                    \ . 'Message: ' . l:match['message'] . "\n"
                    \ . 'Suggestion: ' . join(l:replacements, '; ') . "\n"
                    \ . l:context['text'] . "\n"
                    \ . l:mark . "\n"
        call add(l:output, {
        \   'lnum'    : l:lin,
        \   'col'     : l:col,
        \   'end_lnum': l:match['priv']['toy'] + 1,
        \   'end_col' : l:match['priv']['tox'],
        \   'vcol'    : 1,
        \   'code'    : ale#Var(a:buffer, 'tex_lty_code'),
        \   'text'    : l:match['message'],
        \   'detail'  : l:detail,
        \})
    endfor
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

