# Vehicle Log Analyzer
This CLI tool analyzes logs using python by parsing vehicle Telematics Control Unit (TCU) .txt and/or .log files for key connectivity events and state changes.

## Why 
Analyzing and triaging vehicle connectivity logs typically requires engineers to manually search through millions of log lines using slow, keyword-based tools — a process that can take hours for just a single day test drive. This tool automates that first, high-level analysis by scanning one or multiple log files and quickly surfacing key events that accelerate issue identification and target root-cause analysis and triage.

## Features
The following key events are detected and displayed by the analyzer with respective timestamps:
- Start and end points of log sessions
- TCU network registration state changes
- TCU data connection state changes and limitations
- Emergency call and data flows
- Modem and system resets
- Vehicle ignition cycles

## Usage
$ python analyzer.py /path/to/logfile.log
$ python analyzer.py /path/to/log-directory/

## Sample Output
C:\VSCode\vehicle-log-analyzer>py analyzer.py C:\VSCode\vehicle-log-analyzer\samples

 ========================= NEW LOG ('Log #1')============================

Log file:
C:\VSCode\vehicle-log-analyzer-public\samples\sample_log_1.log

 -------------------------- Log #1 ANALYSIS -----------------------------

[    INFO    ] Log session #0 started --- Line:1
[IGNI. CHANGE] [PDT] 14.04.2026, 08:00:01.200, Ignition ON  ---  Line:3
[*N/W CHANGE*] [PDT] 14.04.2026, 08:00:02.050, Device registered to network  ---  Line:4
[*PRI. CHANGE] [PDT] 14.04.2026, 08:00:03.100, Primary conn. state: CONNECTING  ---  Line:5
[*PRI. CHANGE] [PDT] 14.04.2026, 08:00:04.200, Primary conn. state: CONNECTED  ---  Line:6
[*SEC. CHANGE] [PDT] 14.04.2026, 08:00:04.500, Secondary conn. state: allowed  ---  Line:7
[*SEC. CHANGE] [PDT] 14.04.2026, 08:00:05.300, Secondary conn. state: CONNECTING  ---  Line:8
[*SEC. CHANGE] [PDT] 14.04.2026, 08:00:06.100, Secondary conn. state: CONNECTED  ---  Line:9
[    INFO    ] Log session #0 ended --- Line:12
[    INFO    ] Log session #1 started --- Line:13
[*PRI. CHANGE] [PDT] 14.04.2026, 08:15:23.100, Primary conn. state: DISCONNECTING  ---  Line:15
[*PRI. CHANGE] [PDT] 14.04.2026, 08:15:23.500, Primary conn. state: DISCONNECTED  ---  Line:16
[*SEC. CHANGE] [PDT] 14.04.2026, 08:15:23.600, Secondary conn. state: DISCONNECTING  ---  Line:17
[*SEC. CHANGE] [PDT] 14.04.2026, 08:15:23.900, Secondary conn. state: DISCONNECTED  ---  Line:18
[*N/W CHANGE*] [PDT] 14.04.2026, 08:15:24.000, Device searching for network  ---  Line:19
[*N/W CHANGE*] [PDT] 14.04.2026, 08:15:30.200, Device registered to network  ---  Line:20
[*PRI. CHANGE] [PDT] 14.04.2026, 08:15:31.000, Primary conn. state: CONNECTING  ---  Line:21
[*PRI. CHANGE] [PDT] 14.04.2026, 08:15:32.100, Primary conn. state: CONNECTED  ---  Line:22
[*SEC. CHANGE] [PDT] 14.04.2026, 08:15:32.500, Secondary conn. state: not allowed  ---  Line:23
[    INFO    ] Log session #1 ended --- Line:25
[    INFO    ] Log session #2 started --- Line:26
[*SEC. CHANGE] [PDT] 14.04.2026, 09:05:10.300, Secondary conn. state: allowed  ---  Line:27
[*SEC. CHANGE] [PDT] 14.04.2026, 09:05:11.100, Secondary conn. state: CONNECTING  ---  Line:28
[*SEC. CHANGE] [PDT] 14.04.2026, 09:05:12.000, Secondary conn. state: CONNECTED  ---  Line:29
[ECALL CHANGE] [PDT] 14.04.2026, 09:22:44.900, eCall started  ---  Line:32
[*DATA UPDATE] [PDT] 14.04.2026, 09:22:45.050, Setting Emergency Data  ---  Line:33
[*DATA UPDATE] [PDT] 14.04.2026, 09:22:45.200, Updating Emergency Data  ---  Line:34
[*DATA UPDATE] [PDT] 14.04.2026, 09:22:46.300, Data Delivered  ---  Line:35
[ECALL CHANGE] [PDT] 14.04.2026, 09:25:00.100, eCall callback started  ---  Line:37
[ECALL CHANGE] [PDT] 14.04.2026, 09:30:00.500, eCall ended  ---  Line:38
[    INFO    ] Log session #2 ended --- Line:40
[    INFO    ] Log session #3 started --- Line:41
[***RESET!***] [PDT] 14.04.2026, 10:45:00.100, MODEM CRASH detected  ---  Line:42
[***RESET!***] [PDT] 14.04.2026, 10:45:00.200, SYS_RESET detected  ---  Line:43
[*N/W CHANGE*] [PDT] 14.04.2026, 10:45:08.000, Device searching for network  ---  Line:45
[*N/W CHANGE*] [PDT] 14.04.2026, 10:45:10.300, Device registered to network  ---  Line:46
[*PRI. CHANGE] [PDT] 14.04.2026, 10:45:11.000, Primary conn. state: CONNECTING  ---  Line:47
[*PRI. CHANGE] [PDT] 14.04.2026, 10:45:12.100, Primary conn. state: CONNECTED  ---  Line:48
[*SEC. CHANGE] [PDT] 14.04.2026, 10:45:13.000, Secondary conn. state: CONNECTING  ---  Line:49
[*SEC. CHANGE] [PDT] 14.04.2026, 10:45:14.200, Secondary conn. state: CONNECTED  ---  Line:50
[    INFO    ] Log session #3 ended --- Line:52
[    INFO    ] Log session #4 started --- Line:53
[IGNI. CHANGE] [PDT] 14.04.2026, 14:30:00.100, Ignition OFF  ---  Line:54
[*SEC. CHANGE] [PDT] 14.04.2026, 14:30:00.500, Secondary conn. state: DISCONNECTING  ---  Line:55
[*SEC. CHANGE] [PDT] 14.04.2026, 14:30:00.800, Secondary conn. state: DISCONNECTED  ---  Line:56
[*PRI. CHANGE] [PDT] 14.04.2026, 14:30:01.000, Primary conn. state: DISCONNECTING  ---  Line:57
[*PRI. CHANGE] [PDT] 14.04.2026, 14:30:01.300, Primary conn. state: DISCONNECTED  ---  Line:58
[*N/W CHANGE*] [PDT] 14.04.2026, 14:30:01.500, Device not registered to network  ---  Line:59
[    INFO    ] Log session #4 ended --- Line:61

 -------------------------- Log #1 SUMMARY -----------------------------

1x 'modem subsystem failure' log msgs
1x 'SYS_RESET' log msgs
2x 'conn:primary state:DISCONNECTED' log msgs
2x 'conn:secondary state:DISCONNECTED' log msgs
62 log lines analyzed in 0.0s


 ========================= NEW LOG ('Log #2')============================

Log file:
C:\VSCode\vehicle-log-analyzer-public\samples\sample_log_2.log

 -------------------------- Log #2 ANALYSIS -----------------------------

[    INFO    ] Log session #0 started --- Line:1
[IGNI. CHANGE] [PDT] 15.04.2026, 06:30:00.400, Ignition ON  ---  Line:3
[*N/W CHANGE*] [PDT] 15.04.2026, 06:30:01.200, Device registered to network  ---  Line:4
[*PRI. CHANGE] [PDT] 15.04.2026, 06:30:02.300, Primary conn. state: CONNECTING  ---  Line:5
[*PRI. CHANGE] [PDT] 15.04.2026, 06:30:03.100, Primary conn. state: CONNECTED  ---  Line:6
[*SEC. CHANGE] [PDT] 15.04.2026, 06:30:03.500, Secondary conn. state: not allowed  ---  Line:7
[    INFO    ] Log session #0 ended --- Line:9
[    INFO    ] Log session #1 started --- Line:10
[*N/W CHANGE*] [PDT] 15.04.2026, 07:12:33.100, Device searching for network  ---  Line:11
[*PRI. CHANGE] [PDT] 15.04.2026, 07:12:33.400, Primary conn. state: DISCONNECTING  ---  Line:12
[*PRI. CHANGE] [PDT] 15.04.2026, 07:12:33.700, Primary conn. state: DISCONNECTED  ---  Line:13
[*N/W CHANGE*] [PDT] 15.04.2026, 07:12:45.200, Device registered to network  ---  Line:14
[*PRI. CHANGE] [PDT] 15.04.2026, 07:12:46.000, Primary conn. state: CONNECTING  ---  Line:15
[*PRI. CHANGE] [PDT] 15.04.2026, 07:12:46.800, Primary conn. state: CONNECTED  ---  Line:16
[*N/W CHANGE*] [PDT] 15.04.2026, 07:15:10.300, Device searching for network  ---  Line:17
[*PRI. CHANGE] [PDT] 15.04.2026, 07:15:10.600, Primary conn. state: DISCONNECTING  ---  Line:18
[*PRI. CHANGE] [PDT] 15.04.2026, 07:15:10.900, Primary conn. state: DISCONNECTED  ---  Line:19
[*N/W CHANGE*] [PDT] 15.04.2026, 07:15:22.100, Device registered to network  ---  Line:20
[*PRI. CHANGE] [PDT] 15.04.2026, 07:15:23.000, Primary conn. state: CONNECTING  ---  Line:21
[*PRI. CHANGE] [PDT] 15.04.2026, 07:15:23.500, Primary conn. state: CONNECTED  ---  Line:22
[    INFO    ] Log session #1 ended --- Line:24
[    INFO    ] Log session #2 started --- Line:25
[*SEC. CHANGE] [PDT] 15.04.2026, 09:40:15.000, Secondary conn. state: allowed  ---  Line:26
[*SEC. CHANGE] [PDT] 15.04.2026, 09:40:15.800, Secondary conn. state: CONNECTING  ---  Line:27
[*SEC. CHANGE] [PDT] 15.04.2026, 09:40:16.500, Secondary conn. state: CONNECTED  ---  Line:28
[***RESET!***] [PDT] 15.04.2026, 11:22:05.400, SYS_RESET detected  ---  Line:30
[*PRI. CHANGE] [PDT] 15.04.2026, 11:22:16.000, Primary conn. state: CONNECTING  ---  Line:33
[*PRI. CHANGE] [PDT] 15.04.2026, 11:22:16.900, Primary conn. state: CONNECTED  ---  Line:34
[*SEC. CHANGE] [PDT] 15.04.2026, 11:22:18.200, Secondary conn. state: CONNECTING  ---  Line:36
[*SEC. CHANGE] [PDT] 15.04.2026, 11:22:19.000, Secondary conn. state: CONNECTED  ---  Line:37
[    INFO    ] Log session #2 ended --- Line:39
[    INFO    ] Log session #3 started --- Line:40
[ECALL CHANGE] [PDT] 15.04.2026, 13:55:40.300, eCall started  ---  Line:42
[*DATA UPDATE] [PDT] 15.04.2026, 13:55:40.450, Setting Emergency Data  ---  Line:43
[*DATA UPDATE] [PDT] 15.04.2026, 13:55:40.600, Updating Emergency Data  ---  Line:44
[*DATA UPDATE] [PDT] 15.04.2026, 13:55:41.800, Data Delivered  ---  Line:45
[ECALL CHANGE] [PDT] 15.04.2026, 13:58:00.500, eCall ended  ---  Line:47
[    INFO    ] Log session #3 ended --- Line:49
[    INFO    ] Log session #4 started --- Line:50
[IGNI. CHANGE] [PDT] 15.04.2026, 16:10:00.100, Ignition OFF  ---  Line:51
[*SEC. CHANGE] [PDT] 15.04.2026, 16:10:00.400, Secondary conn. state: DISCONNECTING  ---  Line:52
[*SEC. CHANGE] [PDT] 15.04.2026, 16:10:00.700, Secondary conn. state: DISCONNECTED  ---  Line:53
[*PRI. CHANGE] [PDT] 15.04.2026, 16:10:01.000, Primary conn. state: DISCONNECTING  ---  Line:54
[*PRI. CHANGE] [PDT] 15.04.2026, 16:10:01.300, Primary conn. state: DISCONNECTED  ---  Line:55
[*N/W CHANGE*] [PDT] 15.04.2026, 16:10:01.500, Device not registered to network  ---  Line:56
[    INFO    ] Log session #4 ended --- Line:58

 -------------------------- Log #2 SUMMARY -----------------------------

0x 'modem subsystem failure' log msgs
1x 'SYS_RESET' log msgs
3x 'conn:primary state:DISCONNECTED' log msgs
1x 'conn:secondary state:DISCONNECTED' log msgs
59 log lines analyzed in 0.0s

Total of 119 log lines analyzed in 0.1s

## Requirements
Python 3.14.2 (no external dependencies)

## License
MIT