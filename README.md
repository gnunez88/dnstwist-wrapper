# DNSTwist Wrapper

A [`dnswrapper`](https://github.com/elceef/dnstwist) to automate some tasks.

## Why?

Since I use [`dnstwist`](https://github.com/elceef/dnstwist) from time to time, I keep forgetting
what options I like to use it with.

I also like to save the output into a file, so I do not need to run it again, within a short
period of time. Nevertheless, the output format I prefer is **JSON**, which is quite versatile,
but it is sometimes a pain in the neck to parse or remember what [`jq`]() options to leverage.

### I do not get it, why?

When you programme more often you feel the need to automate almost anything. The more you
automate the less you will have to work later.

As once I have read: *thrive to be lazy*.

#### Seriously, why?

Stop it! And read on!

## Usage

Get DNSTwist results:
```bash
./dnstwist.sh <domain>
```

Parse DNSTwist JSON results:
```bash
./parse-info.sh
```
**Note 1**: We can specify a single file: `./parse-info.sh <json-file>`
**Note 2**: We can specify a folder, every JSON file within it will be parsed: `./parse-info.sh <dir>`


## Dependencies

The installation methods for any repository are in Debian-based distros.

Since there are `bash` scripts, there is the need of using some tools, namely
- `column` (it should be preinstalled, if not: `sudo apt install -y bsdextrautils`)
- `grep` (it should be preinstalled, if not: `sudo apt install -y grep`)
- `jq` (`sudo apt install -y jq`)
- `virtualenv` (`sudo apt install -y python3-virtualenv`)
- `dnstwist.py` (clone this repo with the `--recurse-submodules` flag)

## TODO

- [x] Include an option to show more fields
- [ ] Parse better when there are Banners with blank spaces (because of `column`)
