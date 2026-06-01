# Aircraft Autopilot (altitude & attitude hold)

A flight autopilot shown through a real artificial horizon (attitude indicator).
The plane keeps getting knocked around by turbulence, and a PID autopilot holds
the target altitude and keeps the wings level — exactly like the "altitude hold"
mode on a real aircraft.

Press UP / DOWN to change the target altitude and watch the autopilot fly the
plane back to it.

## what's inside

- artificial horizon that banks and pitches with the plane
- altitude-hold PID (error → elevator → climb/descent)
- wing-leveler PID that fights the turbulence
- live altitude / vertical-speed / bank readout

## run

```bash
pip install pygame
python sim.py
```

tags: ai, control, pid, aviation, autopilot, simulation, pygame

the artificial horizon rotating while the autopilot fixes it is really satisfying.
