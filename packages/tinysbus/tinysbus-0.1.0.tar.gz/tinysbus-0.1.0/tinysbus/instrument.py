import struct
import time
import serial

from .crc import calculate_crc

# Frame Synchronization
FS = 0xB5
ESCAPE_CHAR = 0xC5

# Attributes
AT_REQUEST = 0x00
AT_RESPONSE = 0x01
AT_ACK = 0x02

# S-Bus codes
SC_READ_COUNTER = 0x00
SC_READ_FLAGS = 0x02
SC_READ_INPUT = 0x03
SC_READ_RTC = 0x04
SC_READ_OUTPUT = 0x05
SC_READ_REGISTER = 0x06
SC_READ_TIMER = 0x07
SC_READ_DATA_BLOCK = 0x96
SC_WRITE_COUNTER = 0x0A
SC_WRITE_FLAGS = 0x0B
SC_WRITE_RTC = 0x0C
SC_WRITE_OUTPUT = 0x0D
SC_WRITE_REGISTER = 0x0E
SC_WRITE_TIMER = 0x0F
SC_WRITE_DATA_BLOCK = 0x97

REGISTER_SIZE = 4
MAX_REGISTERS = 10
REQUEST_SIZE = 9

TIMEOUT = 1.0
WAIT_BETWEEN_REQUESTS = 0.1

class Instrument:
    def __init__(self, address, serial_port, timeout=TIMEOUT, async_=False, **kwargs):
        self.address = address
        self.serial = serial.Serial(serial_port, timeout=timeout, **kwargs)
        self.last_request_time = 0.0

    def read_counter(self, register):
        raise NotImplementedError("Reading Counters is not yet implemented.")

    def read_flags(self):
        raise NotImplementedError("Reading Flags is not yet implemented.")

    def read_input(self):
        raise NotImplementedError("Reading Inputs is not yet implemented.")

    def read_rtc(self):
        raise NotImplementedError("Reading RTC is not yet implemented.")

    def read_output(self):
        raise NotImplementedError("Reading Outputs is not yet implemented.")

    def read_register(self, register_address, number_of_decimals=0, signed=False):
        if register_address > 255:
            raise ValueError("Maximum value for register is 255")
        message = [FS, AT_REQUEST, self.address, SC_READ_REGISTER, 0, 0, register_address]
        response_size = 4 + 4
        data = self._perform_request(message, response_size=response_size)
        return self._interpret_result(data, number_of_decimals, signed)

    def read_registers(self, register_address, number_of_registers=1, number_of_decimals=0, signed=False):
        if register_address + number_of_registers > 255:
            raise ValueError("Cannot read registers above number 255.")
        remaining_registers = number_of_registers
        results = []
        while remaining_registers > 0:
            number_of_registers = min(remaining_registers, MAX_REGISTERS)

            message = [FS, AT_REQUEST, self.address, SC_READ_REGISTER, number_of_registers - 1, 0, register_address]
            response_size = 4 + 4 * number_of_registers
            data = self._perform_request(message, response_size=response_size)
            results += self._interpret_result(data, number_of_decimals, signed, always_list=True)

            remaining_registers -= number_of_registers
            start_register += number_of_registers
        return results

    def read_timer(self, timer):
        raise NotImplementedError("Reading Timers is not yet implemented.")

    def read_data_block(self):
        raise NotImplementedError("Reading Data Blocks is not yet implemented.")

    def write_counter(self):
        raise NotImplementedError("Writing Counters is not yet implemented.")

    def write_flags(self):
        raise NotImplementedError("Writing Flags is not yet implemented.")

    def write_rtc(self):
        raise NotImplementedError("Writing RTC is not yet implemented.")

    def write_output(self):
        raise NotImplementedError("Writing Outputs is not yet implemented.")

    def write_register(self):
        raise NotImplementedError("Writing Registers is not yet implemented.")

    def write_timer(self):
        raise NotImplementedError("Writing Timers is not yet implemented.")

    def write_data_block(self):
        raise NotImplementedError("Writing Data Blocks is not yet implemented.")

    def _perform_request(self, message, response_size):
        self._wait_for_next_request()
        message = self._escape_fs_char(message)
        message += calculate_crc(message)
        self.serial.write(message)
        response = self.serial.read(response_size)
        if not response:
            raise TimeoutError("No response received in time")
        self._check_crc(response)
        return response

    def _escape_fs_char(self, message):
        if FS in message[1:]:
            original_message = message
            message = [original_message[0]]
            for char in original_message[1:]:
                message.append(char)
                if char == FS:
                    message.append(ESCAPE_CHAR)
        return message

    def _wait_for_next_request(self):
        now = time.time()
        time_elapsed = now - self.last_request_time
        time.sleep(max(0, WAIT_BETWEEN_REQUESTS - time_elapsed))
        self.last_request_time = now

    def _check_crc(self, message):
        crc = calculate_crc(message[:-2])
        if crc != message[-2:]:
            return False
        return True

    def _interpret_result(self, message, number_of_decimals=0, signed=False, always_list=False):
        if message[0] != FS:
            raise ValueError("Message does not begin with byte 0xB5. Check your baudrate and cable polarity.")

        if message[1] != AT_RESPONSE:
            raise ValueError(f"The response code was: {int(message[1])}, expected: {AT_RESPONSE}")

        register_values = []
        data = message[2:-2]
        number_of_registers = int(len(data)/4)
        if signed:
            format_code = 'l'
        else:
            format_code = 'L'
        if number_of_decimals == 0:
            register_values = [value for value in struct.unpack(f'>{number_of_registers}{format_code}', data)]
        else:
            register_values = [value / 10 ** number_of_decimals for value in struct.unpack(f'>{number_of_registers}{format_code}', data)]

        if not always_list and len(register_values) == 1:
            return register_values[0]
        return register_values

    def _chunk_data(self, data):
        for i in range(len(data)>>2):
            yield data[i*REGISTER_SIZE:(i+1)*REGISTER_SIZE]
