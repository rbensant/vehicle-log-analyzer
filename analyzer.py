import os
import re
import time
import argparse
import glob

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

def count_event(events, key):
    events[key] = events.get(key, 0) + 1

def log_session(current_state, session, line, line_num):
    if "-- BEGIN:" in line:
        new_state = "started"

    elif "-- END:" in line:
        new_state = "ended"

    else:
        return current_state
    
    if new_state != current_state:
        print(f"[    INFO    ] Log session #{session} {new_state} --- Line:{line_num:,}")
        current_state = new_state
    
    return current_state

def reg_state_change(current_state, line, line_num):
    if "Network registration:" in line:
        if "NW_STATE_REGISTERED" in line:
            new_state = "registered to network"

        elif "NW_STATE_SEARCHING" in line:
            new_state = "searching for network"

        elif "NW_STATE_NOT_REGISTERED" in line:
            new_state = "not registered to network"
    
        else:
            return current_state

    else: 
        return current_state
    
    if new_state != current_state:
        print(f"[*N/W CHANGE*] {extract_timestamp(line)} Device {new_state}  ---  Line:{line_num:,}")
        current_state = new_state

    return current_state

def conn_state_change(conn, current_state, line, line_num):  
    if f"conn:{conn} state:CONNECTED" in line:
        new_state = "CONNECTED"

    elif f"conn:{conn} state:CONNECTING" in line:
        new_state = "CONNECTING"

    elif f"conn:{conn} state:DISCONNECTING" in line:
        new_state = "DISCONNECTING"

    elif f"conn:{conn} state:DISCONNECTED" in line:
        new_state = "DISCONNECTED"

    elif f"conn:{conn} state:UNKNOWN" in line:
        new_state = "UNKNOWN"

    else:
        return current_state

    if new_state != current_state:
        if conn == "primary":
            print(f"[*PRI. CHANGE] {extract_timestamp(line)} Primary conn. state: {new_state}  ---  Line:{line_num:,}")

        else:
            print(f"[*SEC. CHANGE] {extract_timestamp(line)} Secondary conn. state: {new_state}  ---  Line:{line_num:,}")

        current_state = new_state

    return current_state

def ecall_state_change(current_state, line, line_num):
    if "eCall Trigger" in line:
        new_state = "eCall started"

    elif "Callback Trigger" in line:
        new_state = "eCall callback started"

    elif "eCall Timer Started" in line:
        new_state = "eCall ended"
    
    else:
        return current_state

    if new_state != current_state:
        print(f"[ECALL CHANGE] {extract_timestamp(line)} {new_state}  ---  Line:{line_num:,}")
        current_state = new_state

    return current_state

def edata_state_change(current_state, line, line_num):
    if "EmergencyDataManager" in line:
        if "Setting Emergency Data" in line: 
            new_state = "Setting Emergency Data"

        elif "Updating Emergency Data" in line: 
            new_state = "Updating Emergency Data"

        elif "Data delivered" in line:
            new_state = "Data Delivered"

        else:
            return current_state

    else:
        return current_state
    
    if new_state != current_state:
        print(f"[*DATA UPDATE] {extract_timestamp(line)} {new_state}  ---  Line:{line_num:,}")
        current_state = new_state
        
    return current_state

def ignition_cycle(current_state, line, line_num):
    if "ignition = on" in line:
        new_state = "Ignition ON"

    elif "ignition = off" in line:
        new_state = "Ignition OFF"

    else:
        return current_state

    if new_state != current_state:
        print(f"[IGNI. CHANGE] {extract_timestamp(line)} {new_state}  ---  Line:{line_num:,}")
        current_state = new_state

    return current_state

def sec_conn_allowed(current_state, line, line_num):
    if "SecondaryConnAllowed" in line:
        if "allowed:true" in line:
            new_state = "Secondary conn. state: allowed"
        
        elif "allowed:false" in line:
            new_state = "Secondary conn. state: not allowed"
        else:
            return current_state

    else: 
        return current_state
    
    if new_state != current_state:
        print(f"[*SEC. CHANGE] {extract_timestamp(line)} {new_state}  ---  Line:{line_num:,}")
        current_state = new_state

    return current_state

def modem_reset(current_state, line, line_num):
    if "modem subsystem failure" in line:
        new_state = "MODEM CRASH detected"

    else:
        return current_state
    
    if new_state != current_state:
        print(f"[***RESET!***] {extract_timestamp(line)} {new_state}  ---  Line:{line_num:,}")
        current_state = new_state

    return current_state

def sys_reset(current_state, line, line_num):
    if "SYS_RESET" in line:
        new_state = "SYS_RESET detected"

    elif "sysReset" in line:
        new_state = "SYS_RESET detected"
    
    elif "executeSystemReset" in line:
        new_state = "SYS_RESET triggered"

    else:
        return current_state
    
    if new_state != current_state:
        print(f"[***RESET!***] {extract_timestamp(line)} {new_state}  ---  Line:{line_num:,}")
        current_state = new_state

    return current_state

def extract_timestamp(line):
    pattern = (
    r"(?P<date>\d{2}\.\d{2}\.\d{4})\s+"       # Matches date, e.g. 13.04.2026
    r"(?P<time>\d{2}:\d{2}:\d{2}\.\d{3}).*?"  # Matches time, e.g. 20:56:27.466
    )
    match = re.search(pattern, line)

    if match:
        return f"[PDT] {match.group('date')}, {match.group('time')},"
    
    return "Timestamp missing"
    
def main():

    total_start_time = time.perf_counter()
    args = parse_args()
    log_files = collect_log_files(args.path)
    total_line_num = 0
    log_num = 1

    for log_file in log_files:
        events = {"modem subsystem failure": 0,
                  "SYS_RESET": 0,
                  "conn:primary state:DISCONNECTED": 0,
                  "conn:secondary state:DISCONNECTED": 0}

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
            print(f"\n ========================= NEW LOG ('Log #{log_num}')============================ \n")
            print(f"Log file:\n{log_file}")
            print(f"\n -------------------------- Log #{log_num} ANALYSIS ----------------------------- \n")

            # Count events
            for line in file:
                for key in events:
                    if key in line:
                        count_event(events, key)

                # Track state changes
                reg_state = reg_state_change(reg_state, line, line_num)
                pri_state = conn_state_change("primary", pri_state, line, line_num)
                sec_state = conn_state_change("secondary", sec_state, line, line_num)
                ecall_state = ecall_state_change(ecall_state, line, line_num)
                edata_state = edata_state_change(edata_state, line, line_num)
                modem_state = modem_reset(modem_state, line, line_num)
                sys_state = sys_reset(sys_state, line, line_num)
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
            print(f"{count}x '{log}' log msgs")

        # Per-file performance
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"{line_num:,} log lines analyzed in {elapsed_time:.1f}s \n")
        log_num += 1

    # Total performance (for multiple log files)
    total_end_time = time.perf_counter()
    total_time = total_end_time - total_start_time
    print(f"Total of {total_line_num:,} log lines analyzed in {total_time:.1f}s \n")

if __name__ == "__main__":
    main()