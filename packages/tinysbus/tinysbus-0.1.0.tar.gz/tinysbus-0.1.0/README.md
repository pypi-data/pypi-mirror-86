# Tiny S-BUS

tinysbus is a small Python package for interfacing with SAIA S-Bus devices.

## Usage

```python
import tinysbus

inst = tinysbus.Instrument(serial_port='/dev/ttyUSB0',
                           baurate=38400,
                           address=1)

# Read a single register:
inst.read_register(20)

# Read 4 registers, starting at number 20
inst.read_registers(20, 4)
```