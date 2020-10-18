
import os
import subprocess

tmp_dir = 'tests/test_shell_cmd/tmp/'
lt_exec = tmp_dir + 'lt_exec.sh'
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

    os.system('rm ' + lt_exec + ' ' + shell_in + ' ' + lt_out)
    return out.stdout.decode()

