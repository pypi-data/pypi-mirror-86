# libgener: Python LibGen helper functions

## installation

```shell script
pip install libgener
```

## usage

### download all torrents

```shell script
libgener-torrents -o torrents/
```

`-o` option specify where torrent files save

If you have a proxy, you can:

```shell script
libgener-torrents -p 'http://localhost:6152' -o torrents/
```

Default LibGen server is `http://libgen.rs/`, if you want to use another server, you can:

```shell script
libgener-torrents -s 'http://gen.lib.rus.ec/' -p 'http://localhost:6152' -o torrents/
```

When you encounter errors, you can enable debug mode:

```shell script
libgener-torrents -s 'http://gen.lib.rus.ec/' -p 'http://localhost:6152' -o torrents/ -v
```