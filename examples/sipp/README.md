# Benchmark scenarios

Following tools and libraries are needed in order to run the benchmark:
- `sipp` - a free SIP testing tool. (For MacOS, you can install it using `brew install sipp`.)
- `psrecord` - a Python utility to record the CPU and memory usage of a process. (Install it using `uv pip install psrecord`.)
- `matplotlib` - a Python library for plotting graphs (needed by --plot flag for psrecord). (Install it using `uv pip install matplotlib`.)
- `aiovoip` - You need to install the library in a dev mode: `uv pip install -e .`

You need first run the sip server, for example it could be `examples/call/server.py`:

```bash
python examples/call/server.py
```

Then we need process ID (PID) of the server, which we can get using `ps` command:

```bash
ps aux | grep server.py
```

Having PID we run psrecord to record the CPU and memory usage of the server:

```bash
psrecord <> --interval 1 --log memory_log.txt --plot memory_plot.png
```

Now we can run sipp default scenario:

```bash
sipp -sn uac 127.0.0.1:6000 -m 10000 -r 1000
# m - number of calls to make
# r - rate of calls per second
```

SIPp Results should be printed in the console

```text
----------------------------- Statistics Screen ------- [1-9]: Change Screen --
  Start Time             | 2025-05-25   18:13:52.940302 1748189632.940302         
  Last Reset Time        | 2025-05-25   18:14:06.332710 1748189646.332710         
  Current Time           | 2025-05-25   18:14:06.333082 1748189646.333082         
-------------------------+---------------------------+--------------------------
  Counter Name           | Periodic value            | Cumulative value
-------------------------+---------------------------+--------------------------
  Elapsed Time           | 00:00:13:392000           | 00:00:13:392000          
  Call Rate              |    0.000 cps              |  746.714 cps             
-------------------------+---------------------------+--------------------------
  Incoming calls created |        0                  |        0                 
  Outgoing calls created |        0                  |    10000                 
  Total Calls created    |                           |    10000                 
  Current Calls          |        0                  |                          
-------------------------+---------------------------+--------------------------
  Successful call        |        0                  |    10000                 
  Failed call            |        0                  |        0                 
-------------------------+---------------------------+--------------------------
  Response Time 1        | 00:00:03:010000           | 00:00:03:010000          
  Call Length            | 00:00:03:015000           | 00:00:03:015000          
------------------------------ Test Terminated --------------------------------
```

After the test is finished, we can stop psrecord process using `Ctrl+C` and it will generate a plot image. A log file is also generated, with the memory and CPU usage of the server.

Another more easy way to do memory profiling is to use `memray`, which is a python library for memory profiling. You can install it using `uv pip install memray`.

In this case, you can run the server with `memray` like this:

```bash
memray run -o server.bin server.py
```

Then you can analyze the memory usage with:

```bash
memray flamegraph server.bin
```

This will generate an HTML file which you can open in your browser.
