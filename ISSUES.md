## 1. Recebemos os seguintes erros ao tentar logar com o email e senah incorretos:

    .-----.   Dev Assistant
    | >_< |   v0.1.29
    '-----'   https://devassistant.tonet.dev

Enter your email: <tonet.dev@gmail.com>
Enter your password:
ERROR:root:Error: The provided credentials are incorrect.
--- Logging error ---
Traceback (most recent call last):
  File "d:\www\dev-assistant-client\dev_assistant_client\main.py", line 56, in start
    await connect()
  File "d:\www\dev-assistant-client\dev_assistant_client\device.py", line 52, in connect
    with open(TOKEN_FILE, "r") as f:
         ^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\Tonet.dev/.dev_assistant_token'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python311\Lib\logging\__init__.py", line 1110, in emit
    msg = self.format(record)
          ^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\logging\__init__.py", line 953, in format
    return fmt.format(record)
           ^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\logging\__init__.py", line 687, in format
    record.message = record.getMessage()
                     ^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\logging\__init__.py", line 377, in getMessage
    msg = msg % self.args
          ~~~~^~~~~~~~~~~
TypeError: not all arguments converted during string formatting
Call stack:
  File "C:\Python311\Scripts\dev-assistant-script.py", line 33, in <module>
    sys.exit(load_entry_point('dev-assistant-client', 'console_scripts', 'dev-assistant')())
  File "d:\www\dev-assistant-client\dev_assistant_client\main.py", line 65, in run
    asyncio.run(main())
  File "C:\Python311\Lib\asyncio\runners.py", line 190, in run
    return runner.run(main)
  File "C:\Python311\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
  File "C:\Python311\Lib\asyncio\base_events.py", line 640, in run_until_complete
    self.run_forever()
  File "C:\Python311\Lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Python311\Lib\asyncio\base_events.py", line 607, in run_forever
    self._run_once()
  File "C:\Python311\Lib\asyncio\base_events.py", line 1922, in _run_once
    handle._run()
  File "C:\Python311\Lib\asyncio\events.py", line 80, in _run
    self._context.run(self._callback, *self._args)
  File "d:\www\dev-assistant-client\dev_assistant_client\main.py", line 49, in main
    await start(args)
  File "d:\www\dev-assistant-client\dev_assistant_client\main.py", line 58, in start
    logging.error("Error:", e)
Message: 'Error:'
Arguments: (FileNotFoundError(2, 'No such file or directory'),)