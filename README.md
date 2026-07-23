# Revshells

A terminal UI (TUI) tool for quickly generating, customizing, and copying reverse shell payloads directly inside the terminal. Inspired by [revshells.com](https://www.revshells.com/)

![](./assets/demo.gif)

## Dependencies

(May not required if you are using Kali Linux)

Install `xsel`/`xclip`, or `wl-copy` manually (to copy on button click functionality), or use the script below: 


```
curl -fsSL https://raw.githubusercontent.com/hexadivine/revshells/refs/heads/main/dependency/install.sh | bash
```

## Installation

```
pipx install git+https://github.com/hexadivine/revshells.git
```

## Useage

```
revshells
```

## Features

* Type `revshells` in the terminal to access reverse and bind shells, listeners, and more.
* Automatically detects the IP address from the selected interface, since it runs locally.
* Includes various encodings such as `base32`, `base64`, and multiple types of URL encoding.
