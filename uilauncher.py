''' Tk-based UI Launcher for the GPS simulator

Copyright (c) 2013 Wei Li Jiang

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import Tkinter
import tkFont
import collections
import gpssim
import glob
import re
import datetime
import time

try:
    import serial
except:
    print 'Missing package dependency for pySerial'
    raise

# Scan available serial ports
ports = ['']
for i in xrange(256):
    try:
        port = serial.Serial(str(i))
        ports.append(port.portstr)
        port.close()
    except serial.SerialException:
        pass

# pyserial doesn't seem to find USB ports at the moment using the above
# method in Linux, this is a workaround.
usb_ports = glob.glob('/dev/ttyUSB*')
for usb_port in usb_ports:
    try:
        port = serial.Serial(usb_port)
        if usb_port not in ports:
            ports.append(usb_port)
        port.close()
    except serial.SerialException:
        pass

# Return the ports in sorted order to avoid confusion when they are filenames.
try_digit = lambda text: int(text) if text.isdigit() else text
ports.sort(key=lambda key: [try_digit(chunk)
                            for chunk in re.split('([0-9]+)', key)])

root = Tkinter.Tk()

try:
    with open(os.path.join(sys._MEIPASS, 'versionnumberstring')) as file:
        versionnumberstring = ' (' + file.read() + ')'
except:
    versionnumberstring = ' (debug)'

root.title('gpssim' + versionnumberstring)

icon = 'gpssim.ico'
try:
    root.iconbitmap(os.path.join(sys._MEIPASS, icon))
except:
    try:
        root.iconbitmap(icon)
    except:
        pass

textwidth = 60  # text field width
customFont = tkFont.Font(size=10)
smallerFont = tkFont.Font(size=9)

# UI collection
vars = collections.OrderedDict()
labels = collections.OrderedDict()
controls = collections.OrderedDict()
formats = collections.OrderedDict()

# Create default format strings based on library outputs
defaultformatstring = ''
formats = sorted(gpssim.ModelGpsReceiver().supported_output())
for format in formats:
    defaultformatstring += format
    if format != formats[-1]:
        defaultformatstring += ', '

frame = Tkinter.LabelFrame(text='Configuration', padx=5, pady=5)

# Instantiate configuration variables and their respective label/edit fields.
vars['output'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Formats (ordered):')
vars[vars.keys()[-1]].set(defaultformatstring)
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

bgcolor = controls[vars.keys()[-1]].cget('background')

vars['comport'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='COM port (optional):')
controls[vars.keys()[-1]] = Tkinter.OptionMenu(frame,
                                               vars[vars.keys()[-1]], *tuple(ports))

vars['baudrate'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Baud rate:')
vars[vars.keys()[-1]].set(4800)
controls[vars.keys()[-1]] = Tkinter.OptionMenu(frame, vars[vars.keys()[-1]],
                                               *tuple(serial.Serial.BAUDRATES[serial.Serial.BAUDRATES.index(4800):]))

vars['static'] = Tkinter.BooleanVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Static output:')
vars[vars.keys()[-1]].set(False)
controls[vars.keys()[-1]] = Tkinter.Checkbutton(frame,
                                                text='', variable=vars[vars.keys()[-1]])

vars['static'] = Tkinter.BooleanVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Static output:')
vars[vars.keys()[-1]].set(False)
controls[vars.keys()[-1]] = Tkinter.Checkbutton(frame,
                                                text='', variable=vars[vars.keys()[-1]])

vars['interval'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Update Interval (s):')
vars[vars.keys()[-1]].set('1.0')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['step'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Simulation Step (s):')
vars[vars.keys()[-1]].set('1.0')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['heading_variation'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame,
                                        text='Simulated heading variation (deg):')
vars[vars.keys()[-1]].set('')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['fix'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Fix type:')
vars[vars.keys()[-1]].set('SPS_FIX')
controls[vars.keys()[-1]] = Tkinter.OptionMenu(frame,
                                               vars[vars.keys()[-1]], *tuple(gpssim.fix_types.keys()))

vars['solution'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='FAA solution mode:')
vars[vars.keys()[-1]].set('AUTONOMOUS_SOLUTION')
controls[vars.keys()[-1]] = Tkinter.OptionMenu(frame,
                                               vars[vars.keys()[-1]], *tuple(gpssim.solution_modes.keys()))

vars['num_sats'] = Tkinter.IntVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Visible satellites:')
vars[vars.keys()[-1]].set(15)
controls[vars.keys()[-1]] = Tkinter.OptionMenu(frame,
                                               vars[vars.keys()[-1]], *tuple(range(33)))

vars['manual_2d'] = Tkinter.BooleanVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Manual 2-D mode:')
vars[vars.keys()[-1]].set(False)
controls[vars.keys()[-1]] = Tkinter.Checkbutton(frame,
                                                text='', variable=vars[vars.keys()[-1]])

vars['dgps_station'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='DGPS Station ID:')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['last_dgps'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame,
                                        text='Time since DGPS update (s):')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['date_time'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame,
                                        text='Initial ISO 8601 date/time/offset:')
vars[vars.keys()[-1]].set(datetime.datetime.now(gpssim.TimeZone(time.timezone)).isoformat())
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['time_dp'] = Tkinter.IntVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Time precision (d.p.):')
vars[vars.keys()[-1]].set('3')
controls[vars.keys()[-1]] = Tkinter.OptionMenu(frame,
                                               vars[vars.keys()[-1]], *tuple(range(4)))

vars['lat'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Latitude (deg):')
vars[vars.keys()[-1]].set('-45.352354')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['lon'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Longitude (deg):')
vars[vars.keys()[-1]].set('-134.687995')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['altitude'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Altitude (m):')
vars[vars.keys()[-1]].set('-11.442')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['geoid_sep'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Geoid separation (m):')
vars[vars.keys()[-1]].set('-42.55')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['horizontal_dp'] = Tkinter.IntVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame,
                                        text='Horizontal precision (d.p.):')
vars[vars.keys()[-1]].set(3)
controls[vars.keys()[-1]] = Tkinter.OptionMenu(frame,
                                               vars[vars.keys()[-1]], *tuple(range(1, 6)))

vars['vertical_dp'] = Tkinter.IntVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame,
                                        text='Vertical precision (d.p.):')
vars[vars.keys()[-1]].set(1)
controls[vars.keys()[-1]] = Tkinter.OptionMenu(frame,
                                               vars[vars.keys()[-1]], *tuple(range(4)))

vars['kph'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Speed (km/hr):')
vars[vars.keys()[-1]].set('45.61')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['heading'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Heading (deg True):')
vars[vars.keys()[-1]].set('123.56')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['mag_heading'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame,
                                        text='Magnetic heading (deg True):')
vars[vars.keys()[-1]].set('124.67')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['mag_var'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame,
                                        text='Magnetic Variation (deg):')
vars[vars.keys()[-1]].set('-12.33')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['speed_dp'] = Tkinter.IntVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='Speed precision (d.p.):')
vars[vars.keys()[-1]].set(1)
controls[vars.keys()[-1]] = Tkinter.OptionMenu(frame,
                                               vars[vars.keys()[-1]], *tuple(range(4)))

vars['angle_dp'] = Tkinter.IntVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame,
                                        text='Angular precision (d.p.):')
vars[vars.keys()[-1]].set(1)
controls[vars.keys()[-1]] = Tkinter.OptionMenu(frame,
                                               vars[vars.keys()[-1]], *tuple(range(4)))

vars['hdop'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='HDOP:')
vars[vars.keys()[-1]].set('3.0')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['vdop'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='VDOP:')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

vars['pdop'] = Tkinter.StringVar()
labels[vars.keys()[-1]] = Tkinter.Label(frame, text='PDOP:')
controls[vars.keys()[-1]] = Tkinter.Entry(frame, textvar=vars[vars.keys()[-1]])

# Pack the controls
current_row = 0
for item in controls.keys():
    labels[item].config(font=customFont)
    labels[item].grid(row=current_row, sticky=Tkinter.E, column=0)

    if isinstance(controls[item], Tkinter.Entry):
        controls[item].config(width=textwidth, font=customFont)
        controls[item].grid(
            row=current_row, sticky=Tkinter.E + Tkinter.W, column=1)
    elif isinstance(controls[item], Tkinter.OptionMenu):
        controls[item].config(font=smallerFont, relief=Tkinter.SUNKEN,
                              borderwidth=1, activebackground=bgcolor, background=bgcolor)
        controls[item].grid(row=current_row, sticky=Tkinter.W, column=1)
    else:
        controls[item].grid(row=current_row, sticky=Tkinter.W, column=1)
    current_row += 1

# Function that gets called from the UI to start the simulator
sim = gpssim.GpsSim()


def update():
    with sim.lock:
        formatstring = ''
        for format in sim.gps.output:
            formatstring += format
            if format != sim.gps.output[-1]:
                formatstring += ', '

        vars['output'].set(formatstring)
        vars['static'].set(sim.static)
        vars['interval'].set(sim.interval)
        vars['step'].set(sim.step)

        if sim.heading_variation == None:
            vars['heading_variation'].set('')
        else:
            vars['heading_variation'].set(str(sim.heading_variation))

        vars['fix'].set(sim.gps.fix)
        vars['solution'].set(sim.gps.solution)
        vars['num_sats'].set(sim.gps.num_sats)
        vars['manual_2d'].set(sim.gps.manual_2d)

        if sim.gps.dgps_station == None:
            vars['dgps_station'].set('')
        else:
            vars['dgps_station'].set(str(sim.gps.dgps_station))

        if sim.gps.last_dgps == None:
            vars['last_dgps'].set('')
        else:
            vars['last_dgps'].set(str(sim.gps.last_dgps))

        if sim.gps.date_time == None:
            vars['date_time'].set('')
        else:
            vars['date_time'].set(str(sim.gps.date_time.isoformat()))

        vars['time_dp'].set(sim.gps.time_dp)

        if sim.gps._lat == None:
            vars['lat'].set('')
        else:
            vars['lat'].set(str(sim.gps._lat))

        if sim.gps.lon == None:
            vars['lon'].set('')
        else:
            vars['lon'].set(str(sim.gps.lon))

        if sim.gps.altitude == None:
            vars['altitude'].set('')
        else:
            vars['altitude'].set(str(sim.gps.altitude))

        if sim.gps.geoid_sep == None:
            vars['geoid_sep'].set('')
        else:
            vars['geoid_sep'].set(str(sim.gps._lat))

        vars['horizontal_dp'].set(sim.gps.horizontal_dp)
        vars['vertical_dp'].set(sim.gps.vertical_dp)

        if sim.gps.kph == None:
            vars['kph'].set('')
        else:
            vars['kph'].set(str(sim.gps.kph))

        if sim.gps.heading == None:
            vars['heading'].set('')
        else:
            vars['heading'].set(str(sim.gps.heading))

        if sim.gps.mag_heading == None:
            vars['mag_heading'].set('')
        else:
            vars['mag_heading'].set(str(sim.gps.mag_heading))

        if sim.gps.mag_var == None:
            vars['mag_var'].set('')
        else:
            vars['mag_var'].set(str(sim.gps.mag_var))

        vars['speed_dp'].set(sim.gps.speed_dp)
        vars['angle_dp'].set(sim.gps.angle_dp)

        if sim.gps.hdop == None:
            vars['hdop'].set('')
        else:
            vars['hdop'].set(str(sim.gps.hdop))

        if sim.gps.vdop == None:
            vars['vdop'].set('')
        else:
            vars['vdop'].set(str(sim.gps.vdop))

        if sim.gps.vdop == None:
            vars['vdop'].set('')
        else:
            vars['pdop'].set(str(sim.gps.pdop))


def poll():
    if sim.is_running():
        root.after(200, poll)
        update()


def start():
    global sim

    if sim.is_running():
        sim.kill()

    sim = gpssim.GpsSim()

    # Change configuration under lock in case its already running from last
    # time
    with sim.lock:

        # Go through each field and parse them for the simulator
        # If anything invalid pops up revert to a safe value (e.g. None)
        try:
            formats = [x.strip() for x in vars['output'].get().split(',')]
            sim.gps.output = formats
        except:
            raise
            vars['output'].set(defaultformatstring)
            formats = [x.strip() for x in vars['output'].get().split(',')]
            sim.gps.output = formats

        sim.static = vars['static'].get()
        try:
            sim.interval = float(vars['interval'].get())
        except:
            sim.interval = 1.0
            vars['interval'].set('1.0')
        try:
            sim.step = float(vars['step'].get())
        except:
            sim.step = 1.0
            vars['step'].set('1.0')

        try:
            sim.heading_variation = float(vars['heading_variation'].get())
        except:
            sim.heading_variation = None
            vars['heading_variation'].set('')

        sim.gps.fix = vars['fix'].get()
        sim.gps.solution = vars['solution'].get()
        sim.gps.manual_2d = vars['manual_2d'].get()
        sim.gps.num_sats = vars['num_sats'].get()

        try:
            sim.gps.dgps_station = int(vars['dgps_station'].get())
        except:
            sim.gps.dgps_station = None
            vars['dgps_station'].set('')

        try:
            sim.gps.last_dgps = float(vars['last_dgps'].get())
        except:
            sim.gps.last_dgps = None
            vars['last_dgps'].set('')

        dt = vars['date_time'].get()
        if dt == '':
            sim.gps.date_time = None
        else:
            try:
                tz = dt[-6:].split(':')
                dt = dt[:-6]
                utcoffset = int(tz[0]) * 3600 + int(tz[1]) * 60

                sim.gps.date_time = datetime.datetime.strptime(
                    dt, '%Y-%m-%dT%H:%M:%S.%f')
                sim.gps.date_time = sim.gps.date_time.replace(
                    tzinfo=gpssim.TimeZone(utcoffset))
            except:
                sim.gps.date_time = datetime.datetime.now(
                    gpssim.TimeZone(time.timezone))
                vars['date_time'].set(sim.gps.date_time.isoformat())

        sim.gps.time_dp = vars['time_dp'].get()

        try:
            sim.gps._lat = float(vars['lat'].get())
        except:
            sim.gps._lat = None
            vars['lat'].set('')

        try:
            sim.gps.lon = float(vars['lon'].get())
        except:
            sim.gps.lon = None
            vars['lon'].set('')

        try:
            sim.gps.altitude = float(vars['altitude'].get())
        except:
            sim.gps.altitude = None
            vars['altitude'].set('')

        try:
            sim.gps.geoid_sep = float(vars['geoid_sep'].get())
        except:
            sim.gps.geoid_sep = None
            vars['geoid_sep'].set('')

        sim.gps.horizontal_dp = vars['horizontal_dp'].get()

        sim.gps.vertical_dp = vars['vertical_dp'].get()

        try:
            sim.gps.kph = float(vars['kph'].get())
        except:
            sim.gps.kph = None
            vars['kph'].set('')

        try:
            sim.gps.heading = float(vars['heading'].get())
        except:
            sim.gps.heading = None
            vars['heading'].set('')

        try:
            sim.gps.mag_heading = float(vars['mag_heading'].get())
        except:
            sim.gps.mag_heading = None
            vars['mag_heading'].set('')

        try:
            sim.gps.mag_var = float(vars['mag_var'].get())
        except:
            sim.gps.mag_var = None
            vars['mag_var'].set('')

        sim.gps.speed_dp = vars['speed_dp'].get()

        sim.gps.angle_dp = vars['angle_dp'].get()

        try:
            sim.gps.hdop = float(vars['hdop'].get())
        except:
            sim.gps.hdop = None
            vars['hdop'].set('')

        try:
            sim.gps.vdop = float(vars['vdop'].get())
        except:
            sim.gps.vdop = None
            vars['vdop'].set('')

        try:
            sim.gps.pdop = float(vars['pdop'].get())
        except:
            sim.gps.pdop = None
            vars['pdop'].set('')

        sim.comport.baudrate = vars['baudrate'].get()

    # Finally start serving (non-blocking as we are in an asynchronous UI
    # thread)
    port = vars['comport'].get()
    if port == '':
        port = None

    startstopbutton.config(command=stop, text='Stop')
    for item in controls.keys():
        controls[item].config(state=Tkinter.DISABLED)
    sim.serve(port, blocking=False)
    poll()


def stop():
    if sim.is_running():
        sim.kill()

    startstopbutton.config(command=start, text='Start')

    update()

    for item in controls.keys():
        controls[item].config(state=Tkinter.NORMAL)

startstopbutton = Tkinter.Button(root, text='Start', command=start)

def main():
    frame.pack(padx=5, pady=5, side=Tkinter.TOP)
    startstopbutton.pack(padx=5, pady=5, side=Tkinter.RIGHT)

    # Start the UI!
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        sim.kill()

if __name__ == "__main__":
    main()
