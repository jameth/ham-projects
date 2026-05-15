# FT-710 ft710ctl v1 Smoke Test

Date: 2026-05-15
Firmware: (record MAIN/DISPLAY/DSP/SDR versions from [SOFT VERSION])
Host OS: (uname -a)
USB cable: (model)
/dev/ttyUSB* device: /dev/ttyUSB0

## Boot sequence
- [ ] `lsmod | grep cp210x` shows the driver is loaded
- [ ] `/dev/ttyUSB0` and `/dev/ttyUSB1` exist after USB plug-in
- [ ] `.venv/bin/ft710ctl --port /dev/ttyUSB0` starts without error
- [ ] http://localhost:8710/ loads in browser
- [ ] Banner shows green "connected" within 3 seconds

## Scope panel
- [ ] Set span 1 kHz; verify radio display
- [ ] Set span 2 kHz; verify radio display
- [ ] Set span 5 kHz; verify radio display
- [ ] Set span 10 kHz; verify radio display
- [ ] Set span 20 kHz; verify radio display
- [ ] Set span 50 kHz; verify radio display
- [ ] Set span 100 kHz; verify radio display
- [ ] Set span 200 kHz; verify radio display
- [ ] Set span 500 kHz; verify radio display
- [ ] Set span 1 MHz; verify radio display
- [ ] Set reference level +00.0
- [ ] Set reference level -30.0
- [ ] Set reference level +30.0
- [ ] Set reference level -15.5
- [ ] Set mode 3DSS_CENTER
- [ ] Set mode 3DSS_CURSOR
- [ ] Set mode 3DSS_FIX
- [ ] Set mode WF_CENTER_NORMAL
- [ ] Set mode WF_CENTER_EXPAND
- [ ] Set mode WF_CURSOR_NORMAL
- [ ] Set mode WF_CURSOR_EXPAND
- [ ] Set mode WF_FIX_NORMAL
- [ ] Set mode WF_FIX_EXPAND

## Tuning panel
- [ ] VFO A → 14.250 MHz
- [ ] VFO B → 7.074 MHz
- [ ] Swap VFOs
- [ ] Mode cycle: USB / LSB / CW-U / CW-L / FM / AM / DATA-U
- [ ] Band cycle: 160m → 10m via UI
- [ ] Split on / off
- [ ] CLAR on / off

## RX DSP panel
- [ ] Preamp IPO → AMP1 → AMP2
- [ ] Attenuator OFF → 6 dB → 12 dB → 18 dB
- [ ] AGC OFF / FAST / MID / SLOW / AUTO (confirm AUTO_FAST/MID/SLOW
      shown back when AUTO is set)
- [ ] NB on/off + level 0-10
- [ ] NR on/off + level 1-15
- [ ] Auto notch on/off
- [ ] Manual notch on/off + frequency
- [ ] Contour on/off + frequency
- [ ] APF on/off + frequency
- [ ] IF shift slider through range
- [ ] Filter width dropdown

## Meters
- [ ] S-meter updates as I tune across an HF signal
- [ ] AF gain slider audible
- [ ] RF gain slider observable

## Multi-client sync
- [ ] Open UI in a second browser tab
- [ ] Change span in tab 1
- [ ] Tab 2 updates within ~200 ms

## Disconnect/reconnect
- [ ] Unplug USB → red banner appears within 5 s
- [ ] Replug USB → green banner returns
- [ ] UI mirrors current radio state after reconnect

## Issues found

(use this section to record anything unexpected)
