# Switch Mode

- [Switch Mode](#switch-mode)
  - [Overview](#overview)
    - [Current Features](#current-features)
  - [Requirements](#requirements)
  - [Usage](#usage)
    - [Snapshots](#snapshots)
  - [Updates](#updates)
  - [Feature Requests \& BUGs](#feature-requests--bugs)

## Overview

Script that takes in a show tech file and creates an interface similar to the switch CLI for better troubleshooting.

### Current Features

- Switch CLI like user interface
- IPv4 Route lookup

## Requirements

- [Git](https://git-scm.com/download/mac)
  - `brew install git`
- [Python3](https://www.python.org/downloads/macos/)
  - Python3 should be installed by default on MAC
  - `$(which python3) --version`

## Usage

Download this repository, using zip/tar or git clone.

```shell
cd ~/Downloads

git clone https://gitlab.aristanetworks.com/roshan/switch_mode.git

cd switch_mode
```

Once in the repository, we can use the following commands to add the alias to invoke the script.

```shell
echo "alias sw='python3 $PWD/Main.py \$1'" >> ~/.zshrc
echo "alias ew='python3 $PWD/Evpn.py \$1'" >> ~/.zshrc
source ~/.zshrc
```

To run the script, type the following command.

`sw <file-name>`
`ew <file-name>`

### Snapshots

```shell
Eliot:~/Desktop/Logs$ sw showtech.log

Switch#
```

*** Gzip files are now supported ***

```shell
Eliot:~/Desktop/Logs$ sw showtech.log.gz

Switch#
```

- Once into switch mode, just type the commands as you would in a typical switch.

```shell
Switch# show mac address-table
------------- show mac address-table -------------

          Mac Address Table
------------------------------------------------------------------

Vlan    Mac Address       Type        Ports      Moves   Last Move
----    -----------       ----        -----      -----   ---------
   5    001c.73de.cade    DYNAMIC     Vx1        1       104 days, 0:26:19 ago
   5    2cdd.e95a.b9d3    DYNAMIC     Vx1        1       0:01:22 ago
   5    b47a.f1ae.2d00    DYNAMIC     Vx1        1       104 days, 0:26:19 ago
<truncated>
```

- Please do note that as of now the switch mode requires the user to type the full commmand.

- The switch mode also enables linux pipelining.

```shell
Switch# show version detail | head -n 10
------------- show version detail -------------

Arista DCS-7050CX3-32S-F
Hardware version:      11.10
Deviations:
Serial number:         JPE21263009
Hardware MAC address:  2cdd.e97e.e73d
System MAC address:    2cdd.e97e.e73d

Software image version: 4.24.4M
Switch#
```

- In case if you are unsure of the command, you could use "?" and type enter.

```shell
? used immediately after a commmand

Switch# show int?
interfaces
interface
```

```shell
? used after the command with a space in between

Switch# show interfaces ?
status
switchport
phy
counters
transceiver
mac
error-correction
```

```shell
if ?? is used

Switch# show interfaces ??
show interfaces status
show interfaces status errdisabled
show interfaces switchport
show interfaces phy detail
show interfaces counters queue | nz
show interfaces counters queue detail | nz
show interfaces counters discards | nz
show interfaces transceiver detail
show interfaces counters errors
show interfaces mac detail
show interfaces error-correction
show interfaces counters rates | nz
show interfaces switchport vlan mapping
show interfaces transceiver tuning detail
```
- Ip route output supported for per vrf.
```shell
For default vrf

Switch: show ip route
VRF: default
Codes: C - connected, S - static, K - kernel,  +
 +
       O - OSPF, IA - OSPF inter area, E1 - OSPF external type 1,
       E2 - OSPF external type 2, N1 - OSPF NSSA external type 1,
       N2 - OSPF NSSA external type2, B - BGP, B I - iBGP, B E - eBGP,
       R - RIP, I L1 - IS-IS level 1, I L2 - IS-IS level 2,
       O3 - OSPFv3, A B - BGP Aggregate, A O - OSPF Summary,
       NG - Nexthop Group Static Route, V - VXLAN Control Service,
       DH - DHCP client installed default route, M - Martian,
       DP - Dynamic Policy Route, L - VRF Leaked,
       G  - gRIBI, RC - Route Cache Route

Gateway of last resort:
 B E      0.0.0.0/0 [20/0] via 10.53.13.150, Ethernet97 Uplink to Spine-01
                           via 10.53.13.158, Ethernet99 Uplink to Spine-02

 M        0.0.0.0/8 is directly connected, <Internal>
 C        1.1.1.0/30 is directly connected, Vlan4094
 <truncated>
 ```
 ```shell
 For non-deafult vrf

Switch: show ip route vrf management
VRF: management
Codes: C - connected, S - static, K - kernel,  +
 +
       O - OSPF, IA - OSPF inter area, E1 - OSPF external type 1,
       E2 - OSPF external type 2, N1 - OSPF NSSA external type 1,
       N2 - OSPF NSSA external type2, B - BGP, B I - iBGP, B E - eBGP,
       R - RIP, I L1 - IS-IS level 1, I L2 - IS-IS level 2,
       O3 - OSPFv3, A B - BGP Aggregate, A O - OSPF Summary,
       NG - Nexthop Group Static Route, V - VXLAN Control Service,
       DH - DHCP client installed default route, M - Martian,
       DP - Dynamic Policy Route, L - VRF Leaked,
       G  - gRIBI, RC - Route Cache Route

Gateway of last resort:
 S        0.0.0.0/0 [1/0] via 10.53.2.1, Management1 management

 M        0.0.0.0/8 is directly connected, <Internal>
 C        10.53.2.0/24 is directly connected, Management1 management
 M        127.0.0.1/32 is directly connected, <Internal>
 M        127.0.0.0/8 is directly connected, <Internal>
 ```
- SwitchMode also supports IPv4 route look up in default and non-deafult vrf.

```shell
Switch: show ip route 192.168.92.57
VRF: default
B E      192.168.92.56/30 [20/0] via 10.53.13.150, Ethernet97 Uplink to Spine-01
                               via 10.53.13.158, Ethernet99 Uplink to Spine-02
```

```shell
Switch: show ip route vrf management 10.53.2.1
VRF: management
 C        10.53.2.0/24 is directly connected, Management1 management
 ```


## Updates

- Switch mode now supports command shortcuts partially.
- Routing table ouput for per vrf is supported (show ip route vrf x).
- Running config for per interface is supported (sh run int x).
- Per interface output for mac/phy detail is supported.
- Per interface output for 'show interfaces' and 'show interfaces status' is supported.

## Feature Requests & BUGs

Please use [this document](https://docs.google.com/document/d/1Q3eoH3ynrmpqYQKKeLTei0jDfon1XjQioH8IpdOBtZU/edit?usp=sharing) for filing any BUGs or feautre Requests (RFEs).
