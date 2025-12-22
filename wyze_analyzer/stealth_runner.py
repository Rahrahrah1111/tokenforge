#!/usr/bin/env python3
"""
Stealth Process Runner
Hides cursor processes with password protection
"""

import sys
import os
import subprocess
import getpass
import hashlib
import tempfile
import shutil
from pathlib import Path
import argparse
import signal
import time

# Password hash for empty string (SHA256)
PASSWORD_HASH = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

def verify_password(password: str) -> bool:
    """Verify password against hash"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return password_hash == PASSWORD_HASH

def hide_process_name(new_name: str = "systemd"):
    """Attempt to hide process name by renaming"""
    try:
        # Try to rename process (Linux specific)
        if sys.platform == 'linux':
            # Create a symlink or use exec to rename
            # Note: This is limited - process name is usually read-only
            # But we can use exec to start with a different name
            pass
    except:
        pass

def run_stealth(command: list, password: str = '', 
                hide_output: bool = True, 
                background: bool = False,
                log_file: str = None):
    """Run command in stealth mode"""
    
    # Verify password
    if not verify_password(password):
        print("Access denied")
        sys.exit(1)
    
    # Create hidden log file if needed
    if log_file is None:
        log_file = os.path.join(tempfile.gettempdir(), 
                               f".{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}.log")
    
    # Prepare output destinations
    if hide_output:
        stdout_dest = open(log_file, 'w')
        stderr_dest = subprocess.STDOUT
    else:
        stdout_dest = sys.stdout
        stderr_dest = sys.stderr
    
    # Get script directory for stealth_wrapper.sh
    script_dir = Path(__file__).parent
    stealth_wrapper = script_dir / 'stealth_wrapper.sh'
    venv_python = script_dir / 'venv' / 'bin' / 'python3'
    venv_activate = script_dir / 'venv' / 'bin' / 'activate'
    
    # Use venv python if available, otherwise system python
    python_cmd = str(venv_python) if venv_python.exists() else 'python3'
    
    # Prepare command with process name hiding
    if sys.platform == 'linux' and stealth_wrapper.exists():
        try:
            if background:
                # Use stealth_wrapper.sh to rename process
                # Build command with proper venv activation
                import shlex
                cmd_parts = [python_cmd] + command
                if venv_activate.exists():
                    # Set environment to use venv properly
                    venv_bin = script_dir / 'venv' / 'bin'
                    venv_lib = script_dir / 'venv' / 'lib'
                    # Find the python version directory
                    python_dirs = list(venv_lib.glob('python*')) if venv_lib.exists() else []
                    python_site_packages = python_dirs[0] / 'site-packages' if python_dirs else None
                    
                    env = os.environ.copy()
                    env['PATH'] = str(venv_bin) + ':' + env.get('PATH', '')
                    env['VIRTUAL_ENV'] = str(script_dir / 'venv')
                    if python_site_packages and python_site_packages.exists():
                        current_pythonpath = env.get('PYTHONPATH', '')
                        env['PYTHONPATH'] = str(python_site_packages) + (':' + current_pythonpath if current_pythonpath else '')
                    full_cmd = [str(stealth_wrapper), python_cmd] + command
                    process = subprocess.Popen(
                        ['nohup'] + full_cmd,
                        stdout=stdout_dest,
                        stderr=stderr_dest,
                        stdin=subprocess.DEVNULL,
                        preexec_fn=os.setsid if hasattr(os, 'setsid') else None,
                        env=env,
                        cwd=str(script_dir)
                    )
                else:
                    full_cmd = [str(stealth_wrapper), python_cmd] + command
                    process = subprocess.Popen(
                        ['nohup'] + full_cmd,
                        stdout=stdout_dest,
                        stderr=stderr_dest,
                        stdin=subprocess.DEVNULL,
                        preexec_fn=os.setsid if hasattr(os, 'setsid') else None
                    )
                print(f"Process started in background (PID: {process.pid})")
                if hide_output:
                    print(f"Log file: {log_file}")
                return process
            else:
                # Foreground execution with renamed process
                if venv_activate.exists():
                    import shlex
                    cmd_parts = [python_cmd] + command
                    full_cmd_str = f'source {venv_activate} && {str(stealth_wrapper)} {" ".join([shlex.quote(str(c)) for c in cmd_parts])}'
                    process = subprocess.Popen(
                        ['bash', '-c', full_cmd_str],
                        stdout=stdout_dest,
                        stderr=stderr_dest,
                        stdin=sys.stdin,
                        cwd=str(script_dir)
                    )
                else:
                    full_cmd = [str(stealth_wrapper), python_cmd] + command
                    process = subprocess.Popen(
                        full_cmd,
                        stdout=stdout_dest,
                        stderr=stderr_dest,
                        stdin=sys.stdin
                    )
                return process.wait()
        except (FileNotFoundError, OSError) as e:
            # Fallback to standard approach
            if background:
                process = subprocess.Popen(
                    ['nohup', python_cmd] + command,
                    stdout=stdout_dest,
                    stderr=stderr_dest,
                    stdin=subprocess.DEVNULL,
                    preexec_fn=os.setsid if hasattr(os, 'setsid') else None
                )
                print(f"Process started in background (PID: {process.pid})")
                if hide_output:
                    print(f"Log file: {log_file}")
                return process
            else:
                return subprocess.run([python_cmd] + command).returncode
    else:
        # Non-Linux or wrapper not found - use standard approach
        if background:
            process = subprocess.Popen(
                ['nohup', python_cmd] + command,
                stdout=stdout_dest,
                stderr=stderr_dest,
                stdin=subprocess.DEVNULL,
                preexec_fn=os.setsid if hasattr(os, 'setsid') else None
            )
            print(f"Process started in background (PID: {process.pid})")
            if hide_output:
                print(f"Log file: {log_file}")
            return process
        else:
            return subprocess.run([python_cmd] + command).returncode

def main():
    # Parse stealth runner arguments first
    stealth_args = []
    script_args = []
    script_name = None
    password = ''
    background = False
    show_output = False
    log_file = None
    
    i = 0
    while i < len(sys.argv[1:]):
        arg = sys.argv[i + 1]
        if arg in ['--password', '-p']:
            if i + 1 < len(sys.argv) - 1:
                password = sys.argv[i + 2]
                i += 2
            else:
                i += 1
        elif arg in ['--background', '-b']:
            background = True
            i += 1
        elif arg == '--show-output':
            show_output = True
            i += 1
        elif arg == '--log-file':
            if i + 1 < len(sys.argv) - 1:
                log_file = sys.argv[i + 2]
                i += 2
            else:
                i += 1
        elif script_name is None:
            script_name = arg
            i += 1
        else:
            script_args.append(arg)
            i += 1
    
    if script_name is None:
        print("Error: Script name required")
        print("Usage: stealth_runner.py <script> [script_args...] [--password PASSWORD] [--background] [--show-output] [--log-file FILE]")
        sys.exit(1)
    
    # Build command
    command = [script_name] + script_args
    
    # Run in stealth mode
    result = run_stealth(
        command,
        password=password,
        hide_output=not show_output,
        background=background,
        log_file=log_file
    )
    
    if not background:
        sys.exit(result if isinstance(result, int) else 0)

if __name__ == '__main__':
    main()

