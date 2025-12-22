# Stealth Runner - Process Hiding Utility

The stealth runner allows you to run Python scripts in a hidden/stealth mode with password protection. The process name is disguised to appear as a system process.

## Features

- **Password Protection**: Requires password (default: empty string '') to run
- **Process Name Hiding**: Process appears as 'systemd' in `ps` output (Linux only)
- **Output Hiding**: All output redirected to hidden log files
- **Background Execution**: Can run processes in the background

## Usage

### Basic Usage

```bash
python3 stealth_runner.py <script> [script_args...] [--password PASSWORD] [--background] [--show-output] [--log-file FILE]
```

### Examples

#### Run transcription in stealth mode (background):
```bash
cd wyze_analyzer
source venv/bin/activate
python3 stealth_runner.py fast_transcribe.py /media/g-spot/B9E9-ABE9/record \
    --max-speed --cpu --start-date 2025-12-06 --end-date 2025-12-07 \
    --password '' --background
```

#### Using the convenience script:
```bash
./run_stealth_transcribe.sh /media/g-spot/B9E9-ABE9/record \
    --max-speed --cpu --start-date 2025-12-06 --end-date 2025-12-07
```

#### Run any script in stealth mode:
```bash
python3 stealth_runner.py your_script.py --arg1 value1 --arg2 value2 \
    --password '' --background
```

## Options

- `--password`, `-p`: Password to verify (default: empty string '')
- `--background`, `-b`: Run process in background
- `--show-output`: Show output instead of hiding (default: hidden)
- `--log-file`: Specify custom log file path (default: auto-generated in /tmp)

## How It Works

1. **Password Verification**: Uses SHA256 hash to verify password (empty string hash is pre-computed)
2. **Process Renaming**: On Linux, uses `exec -a systemd` to rename the process
3. **Output Redirection**: All stdout/stderr redirected to hidden log files in /tmp
4. **Background Execution**: Uses `nohup` and process group separation for background execution

## Security Notes

- The password is verified using SHA256 hash
- Default password is empty string ('')
- Log files are created in /tmp with random names
- Process appears as 'systemd' in process lists (Linux only)

## Checking Running Processes

To check if a stealth process is running:

```bash
# Check for the disguised process
ps aux | grep systemd | grep python

# Check log files
ls -la /tmp/.*.log

# View log file
tail -f /tmp/.<random_hash>.log
```

## Limitations

- Process name hiding only works on Linux systems
- On non-Linux systems, process will run normally but output will still be hidden
- Requires `exec` command for full stealth mode (falls back gracefully if not available)

