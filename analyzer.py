import os
import re
import time
import argparse
import glob
from colorama import Fore, Style, init

init()

COLORS = {
    "error": Fore.RED,
    "warning": Fore.YELLOW,
    "success": Fore.GREEN,
    "info": Fore.MAGENTA,
    "call": Fore.CYAN,
    "log": Fore.WHITE,
    "banner": Fore.LIGHTCYAN_EX
}

TIMESTAMP_PATTERN = re.compile(
    r"(?P<date>\d{2}\.\d{2}\.\d{4})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2}\.\d{3}).*?"
)

def parse_args():
    parser = argparse.ArgumentParser(description="This CLI tool analyzes vehicle connectivity .txt and/or .log files for connectivity events, state changes, resets, and emergency calls")
    parser.add_argument("path", help="This is the path to a single log file or the directory containing log files")

    return parser.parse_args()

def collect_log_files(path):
    if os.path.isfile(path):
        return [path]
    
    elif os.path.isdir(path):
        logs = glob.glob(os.path.join(path, "*.log"))
        txts = glob.glob(os.path.join(path, "*.txt"))
        return sorted(logs + txts)
    
    elif not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    raise ValueError("Path exists, but is not a file or directory")

def color_text(text, color):
    return color + text + Style.RESET_ALL

def count_event(events, key):
    events[key] = events.get(key, 0) + 1

def handle_state_change(msg, current_state, new_state, state_color, line_num):
    if new_state != current_state:
        print(color_text(f"{msg} | Line:{line_num}", state_color))
        current_state = new_state

    return current_state

def log_session(current_state, session, line, line_num):
    state_color = COLORS["log"]

    if "-- BEGIN:" in line:
        new_state = "started"

    elif "-- END:" in line:
        new_state = "ended"

    else:
        return current_state
    
    msg = f"[    INFO    ] Log session #{session} {new_state}"

    return handle_state_change(msg, current_state, new_state, state_color, line_num)

def reg_state_change(current_state, events, line, line_num):
    if "Network registration:" in line:
        if "NW_STATE_REGISTERED" in line:
            new_state = "Device registered to network"
            state_color = COLORS["success"]

        elif "NW_STATE_SEARCHING" in line:
            new_state = "Device searching for network"
            state_color = COLORS["warning"]

        elif "NW_STATE_NOT_REGISTERED" in line:
            new_state = "Device not registered to network"
            state_color = COLORS["error"]
            count_event(events, "Device not registered to network")
    
        else:
            return current_state

    else: 
        return current_state
    
    timestamp = extract_timestamp(line)
    msg = f"[*N/W CHANGE*] {timestamp} {new_state}"

    return handle_state_change(msg, current_state, new_state, state_color, line_num)

def conn_state_change(conn, current_state, events, line, line_num):  
    if f"conn:{conn} state:CONNECTED" in line:
        new_state = "CONNECTED"
        state_color = COLORS["success"]

    elif f"conn:{conn} state:CONNECTING" in line:
        new_state = "CONNECTING"
        state_color = COLORS["warning"]

    elif f"conn:{conn} state:DISCONNECTING" in line:
        new_state = "DISCONNECTING"
        state_color = COLORS["warning"]

    elif f"conn:{conn} state:DISCONNECTED" in line:
        new_state = "DISCONNECTED"
        state_color = COLORS["error"]

        if conn == "primary":
            count_event(events, "Primary connection disconnected")
        else:
            count_event(events, "Secondary connection disconnected")

    elif f"conn:{conn} state:UNKNOWN" in line:
        new_state = "UNKNOWN"
        state_color = COLORS["error"]

        if conn == "primary":
            count_event(events, "Primary connection unknown")
        else:
            count_event(events, "Secondary connection unknown")

    else:
        return current_state
    
    timestamp = extract_timestamp(line)
    if conn == "primary":
        msg = f"[*PRI. CHANGE] {timestamp} Primary conn. state: {new_state}"
    else:
        msg = f"[*SEC. CHANGE] {timestamp} Secondary conn. state: {new_state}"

    return handle_state_change(msg, current_state, new_state, state_color, line_num)

def ecall_state_change(current_state, events, line, line_num):
    state_color = COLORS["call"]

    if "eCall Trigger" in line:
        new_state = "eCall started"
        count_event(events, "eCall triggered")

    elif "Callback Trigger" in line:
        new_state = "eCall callback started"
        count_event(events, "eCall callback")

    elif "eCall Timer Started" in line:
        new_state = "eCall ended"
    
    else:
        return current_state

    timestamp = extract_timestamp(line)
    msg = f"[ECALL CHANGE] {timestamp} {new_state}"
    
    return handle_state_change(msg, current_state, new_state, state_color, line_num)

def edata_state_change(current_state, events, line, line_num):
    state_color = COLORS["call"]

    if "EmergencyDataManager" in line:
        if "Setting Emergency Data" in line: 
            new_state = "Setting Emergency Data"

        elif "Updating Emergency Data" in line: 
            new_state = "Updating Emergency Data"

        elif "Data delivered" in line:
            new_state = "Data Delivered"
            count_event(events, "Emergency data delivered")

        else:
            return current_state

    else:
        return current_state
    
    timestamp = extract_timestamp(line)
    msg = f"[*DATA UPDATE] {timestamp} {new_state}"
    
    return handle_state_change(msg, current_state, new_state, state_color, line_num)

def ignition_cycle(current_state, line, line_num):
    state_color = COLORS["info"]

    if "ignition = on" in line:
        new_state = "Ignition ON"

    elif "ignition = off" in line:
        new_state = "Ignition OFF"

    else:
        return current_state

    timestamp = extract_timestamp(line)
    msg = f"[IGNI. CHANGE] {timestamp} {new_state}"
    
    return handle_state_change(msg, current_state, new_state, state_color, line_num)

def sec_conn_allowed(current_state, line, line_num):
    state_color = COLORS["info"]

    if "SecondaryConnAllowed" in line:
        if "allowed:true" in line:
            new_state = "Secondary conn. state: allowed"
        
        elif "allowed:false" in line:
            new_state = "Secondary conn. state: not allowed"
        else:
            return current_state

    else: 
        return current_state
    
    timestamp = extract_timestamp(line)
    msg = f"[*SEC. CHANGE] {timestamp} {new_state}"
    
    return handle_state_change(msg, current_state, new_state, state_color, line_num)

def modem_reset(current_state, events, line, line_num):
    state_color = COLORS["error"]

    if "modem subsystem failure" in line:
        new_state = "MODEM CRASH detected"
        count_event(events, "Modem crash")

    else:
        return current_state
    
    timestamp = extract_timestamp(line)
    msg = f"[***RESET!***] {timestamp} {new_state}"
    
    return handle_state_change(msg, current_state, new_state, state_color, line_num)

def sys_reset(current_state, events, line, line_num):
    state_color = COLORS["error"]

    if "SYS_RESET" in line:
        new_state = "System RESET detected"
        count_event(events, "System reset")

    elif "sysReset" in line:
        new_state = "System RESET detected"
        count_event(events, "System reset")
    
    elif "executeSystemReset" in line:
        new_state = "System RESET triggered"
        count_event(events, "System reset")

    else:
        return current_state
    
    timestamp = extract_timestamp(line)
    msg = f"[***RESET!***] {timestamp} {new_state}"
    
    return handle_state_change(msg, current_state, new_state, state_color, line_num)

def extract_timestamp(line):
    match = TIMESTAMP_PATTERN.search(line)

    if match:
        return f"[PDT] {match.group('date')}, {match.group('time')}  | "
    
    return "Timestamp missing"
    
def main():

    total_start_time = time.perf_counter()
    args = parse_args()
    log_files = collect_log_files(args.path)
    total_line_num = 0
    log_num = 1

    for log_file in log_files:

        events = {
            "Device not registered to network": 0,
            "Primary connection disconnected": 0,
            "Secondary connection disconnected": 0,
            "Primary connection unknown": 0,
            "Secondary connection unknown": 0,
            "eCall triggered": 0,
            "eCall callback": 0,
            "Emergency data delivered": 0,
            "Modem crash": 0,
            "System reset": 0
            }

        start_time = time.perf_counter()
        log_state = None
        reg_state = None
        pri_state = None
        sec_state = None
        sec_allowed = None
        ecall_state = None
        edata_state = None
        modem_state = None
        sys_state = None
        ignition_state = None
        session = 0
        line_num = 1  # .log/.txt files start at line #1 so output line# will match what the user sees in a txt editor

        with open(log_file, "r") as file:
            print(color_text(f"\n ========================= NEW LOG ('Log #{log_num}')============================ \n", COLORS["banner"]))
            print(color_text(f"Log file:\n{log_file}", COLORS["banner"]))
            print(f"\n -------------------------- Log #{log_num} ANALYSIS ----------------------------- \n")

            for line in file:
                # Track state changes & count events
                reg_state = reg_state_change(reg_state, events, line, line_num)
                pri_state = conn_state_change("primary", pri_state, events, line, line_num)
                sec_state = conn_state_change("secondary", sec_state, events, line, line_num)
                ecall_state = ecall_state_change(ecall_state, events, line, line_num)
                edata_state = edata_state_change(edata_state, events, line, line_num)
                modem_state = modem_reset(modem_state, events, line, line_num)
                sys_state = sys_reset(sys_state, events, line, line_num)
                ignition_state = ignition_cycle(ignition_state, line, line_num)
                sec_allowed = sec_conn_allowed(sec_allowed, line, line_num)
                log_state = log_session(log_state, session, line, line_num)
                if log_state == "ended":
                    session += 1

                line_num += 1
                total_line_num += 1
        
        # Print dict containing event counts
        print(f"\n -------------------------- Log #{log_num} SUMMARY ----------------------------- \n")
        for log, count in events.items():
            if count > 0:
                print(f"{count}x '{log}' log msgs")

        # Per-file performance
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"{line_num:,} log lines in log #{log_num} analyzed in {elapsed_time:.1f}s \n")
        log_num += 1

    # Total performance (for multiple log files)
    total_end_time = time.perf_counter()
    total_time = total_end_time - total_start_time
    print(f"Total of {total_line_num:,} log lines analyzed in {total_time:.1f}s \n")

if __name__ == "__main__":
    main()