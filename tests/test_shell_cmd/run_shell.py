
import os
import subprocess
import time

tmp_dir = 'tests/test_shell_cmd/tmp/'
lt_exec = tmp_dir + 'lt_exec.sh'
lt_in = tmp_dir + 'lt_in.txt'
lt_out = tmp_dir + 'lt_out.txt'
shell_in = tmp_dir + 'shell_in.tex'
msg_header = '=== ' + shell_in + ' ===\n'

#   run yalafi.shell, using an LT emulation called with --lt-command,
#   return stdout as string
#   - otpions: additional options passed to yalafi.shell
#   - latex: LaTeX text, is written to a temp file
#   - encoding: encoding of temp LaTeX file
#   - lt_json_output: JSON output of the LT emulation
#
def run_shell(options, latex, encoding, lt_json_out):

    os.system('mkdir ' + tmp_dir)
    with open(lt_exec, mode='w') as f:
        f.write('#!/bin/bash\n')
        f.write('cat ' + lt_out + '\n')
    os.system('chmod +x ' + lt_exec)

    with open(shell_in, mode='w', encoding=encoding) as f:
        f.write(latex)

    with open(lt_out, mode='w') as f:
        f.write(lt_json_out)

    cmd = ('python -m yalafi.shell --lt-command ' + lt_exec
            + ' ' + options + ' ' + shell_in)
    out = subprocess.run(cmd.split(), stdout=subprocess.PIPE)

    os.system('rm -r ' + tmp_dir)
    return out.stdout.decode()

json_ok = r"""
{"software":{"name":"LanguageTool","version":"4.7","buildDate":"2019-09-28 10:09","apiVersion":1,"premium":false,"premiumHint":"You might be missing errors only the Premium version can find. Contact us at support<at>languagetoolplus.com.","status":""},"warnings":{"incompleteResults":false},"language":{"name":"English (GB)","code":"en-GB","detectedLanguage":{"name":"English (GB)","code":"en-GB","confidence":1.0}},"matches":[]}
"""

#   run yalafi.shell, using an LT emulation called with --lt-command,
#   return input to LT as string
#   - otpions: additional options passed to yalafi.shell
#   - latex: LaTeX text, is written to a temp file
#   - encoding: encoding of temp LaTeX file
#
def get_lt_in(options, latex, encoding):

    os.system('mkdir ' + tmp_dir)
    with open(lt_exec, mode='w') as f:
        f.write('#!/bin/bash\n')
        f.write('echo >> ' + lt_in + '\n')
        f.write('echo $* >> ' + lt_in + '\n')
        f.write('cat >> ' + lt_in + '\n')
        f.write('echo >> ' + lt_in + '\n')
        f.write('cat ' + lt_out + '\n')
    os.system('chmod +x ' + lt_exec)

    with open(lt_out, mode='w') as f:
        f.write(json_ok)

    with open(shell_in, mode='w', encoding=encoding) as f:
        f.write(latex)

    os.system('python -m yalafi.shell --lt-command ' + lt_exec
            + ' ' + options + ' ' + shell_in)

    with open(lt_in) as f:
        txt = f.read()
    os.system('rm -r ' + tmp_dir)

    return txt

#   test of yalafi.shell running as HTTP server
#   - to check the HTML response, we use yalafi.shell --server my
#
def run_as_server(options, latex, json):

    os.system('mkdir ' + tmp_dir)
    with open(lt_exec, mode='w') as f:
        f.write('#!/bin/bash\n')
        f.write('cat ' + lt_out + '\n')
    os.system('chmod +x ' + lt_exec)

    with open(shell_in, mode='w') as f:
        f.write(latex)

    with open(lt_out, mode='w') as f:
        f.write(json)

    cmd = ('python -m yalafi.shell --as-server 8081 --lt-command ' + lt_exec
                    + ' ' + options)
    server = subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)
    time.sleep(10)

    cmd = 'python -m yalafi.shell --plain-input --server my ' + shell_in
    out = subprocess.run(cmd.split(), stdout=subprocess.PIPE)

    server.terminate()
    time.sleep(1)
    os.system('rm -r ' + tmp_dir)

    return out.stdout.decode()

