# Line multiplexer - linemux

The command 'linemux' is a simple tool for splitting a file (or piped data)
into different files line-by-line by a *key*.
The key is a portion of the line from the beginning, determined by a regexp.

The command is invoked like this:
```
$ linemux [options] [input-file]
```

Some options are discussed below, full list is available by option `-h`.
When input file is omitted, stdin is read.

## Installation

Linemux is a Python 3.6+ application and will be available from PyPI.
It should work where Python 3 works.
However, currently you must install it from *gitlab*:

    % pip3 install git+https://gitlab.com/cincan/linemux

Use your favorite Python module installation strategy.

## Details

The name of the created file is the key value, but some characters are filtered away.
Accepted characters are "a" - "z", "A" - "Z", "0" - "9", "_", "-", and ".".
If many keys map to same file name, the a postfix is added to the file name.

The default key is "`.*`", so the whole line is the key.
This effectively finds all unique lines and creates a file for each of them.
The file content is the line (as many times as encountered).
You can change the key regexp by `-k` option (Python regexp syntax).

By default the new files are placed to a directory "linemux".
If there already are files in this directory (e.g. from earlier linemux run),
the results are undefined.
The output directory is changed by option `-d`.

When running the command prints out each created file name.

## Example I

Consider the input file "sample.urls" with content:
```
https://www.oulu.fi
https://www.google.com
https://www.oulu.fi
https://www.oulu.fi/
http://www.oulu.fi/university/
https://www.oulu.fi/
https://www.google.com```
```

You can create a file for each unique URL like this:

```
$ linemux sample.urls
```

The resulting directory structure is:
```
$ find .
./linemux/httpswww.oulu.fi
./linemux/httpswww.google.com
./linemux/httpswww.oulu.fi_2
./linemux/httpwww.oulu.fiuniversity
```

## Example II

On this example, we pick a key from middle of the processed line.
As linemux expects key to be the first thing in the line, we use
`awk` to prepare the line for linemux.

The example data we use is a memory dump process list
from command line tool `volatility`
of the [Volatility Foundation](https://www.volatilityfoundation.org/).
It is process list with data columns separated by vertical bars (pipes):

```
>|0x83d3ac58|System|4|0|81|516|-1|0|2019-10-28 15:47:28 UTC+0000|
>|0x844271a0|smss.exe|252|4|3|29|-1|0|2019-10-28 15:47:28 UTC+0000|
>|0x849a77b0|csrss.exe|328|320|8|527|0|0|2019-10-28 15:47:30 UTC+0000|
...
```

The command-line we are using is the following:

```
awk -F"|" '{print $3 "|" $0}' process.lst | linemux -k ".+?\|" -K
```

The awk-part picks 3rd "|"-separated column and copies it to first positon.
The linemux-part directs stdin by the first column identified by regexp `".+?\|"`.
The option `-K` removes the key from output files.

The result is the process listing divided by 3rd column (process name):

```
$ find .
./linemux/lsass.exe
./linemux/VBoxService.ex
./linemux/svchost.exe
./linemux/wininit.exe
...
```

For example the file "svchost.exe" could look like this:

```
$ cat linemux/svchost.exe
>|0x84a995e0|svchost.exe|584|460|15|371|0|0|2019-10-28 15:47:32 UTC+0000|
>|0x84ac49d0|svchost.exe|700|460|13|287|0|0|2019-10-28 15:47:32 UTC+0000|
>|0x84adf6c0|svchost.exe|760|460|21|400|0|0|2019-10-28 15:47:32 UTC+0000|
>|0x84b0d540|svchost.exe|868|460|23|399|0|0|2019-10-28 15:47:33 UTC+0000|
>|0x84b1c030|svchost.exe|908|460|24|376|0|0|2019-10-28 15:47:33 UTC+0000|
```
