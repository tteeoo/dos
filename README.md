# Network stress tester (Denial Of Service)

## Usage:

```
python dos.py [options] | [<destination> <# of threads> [flags]]
```

#### Flags:

* `-v, --verbose`: verbose output.

* `-p, --python`: use python's requests module instead of `curl`.
This is much slower and more error prone at high thread counts. Only use this option if you do not have `curl`.

#### Options:

* `-h, --help`: prints help message.

* `-V, --version`: prints version information.

* `-l, --legal`: prints legal information.

Press enter to stop, and kill all child threads.

For effective results on a single, relatively low-power server, a few thousand threads will do.

Target web pages that include back-end processing for best results.

## Legal disclosure

In addition to the MIT License, this further legal disclosure applies:

`
I (Theo Henson) am not responsible for the repercussions that you (a user of this software) may face through the illegal usage of this software, nor am I responsible for the damage that any user causes, using this software. By using this software, you take full responsibility, in other words, *use at your own risk*.
`
