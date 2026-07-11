# Console-based-text-editor-with-Vim-like-commands
A minimal text editor implemented in Python, supporting cursor movement, insert/append, delete word/char, copy/paste lines, undo/redo, and more. Designed for learning and practicing command parsing, state management, and terminal UI.

# Vim-Style Text Editor

A simple text editor running in the terminal, supporting common Vim‑like commands. Ideal for learning command parsing, state management, and undo/redo mechanisms.

## Features

- **Cursor Movement** – `h` (left), `l` (right), `j` (up), `k` (down), `^` (beginning), `$` (end)
- **Word Navigation** – `w` (next word), `b` (previous word)
- **Insert & Append** – `i` (insert before cursor), `a` (append after cursor)
- **Deletion** – `x` (delete char), `dw` (delete word), `dd` (delete entire line)
- **Copy & Paste** – `yy` (copy line), `p` (paste below), `P` (paste above)
- **Undo & Repeat** – `u` (undo), `r` (repeat last command)
- **Insert Empty Lines** – `o` (below), `O` (above)
- **Visual Help** – `?` to show all commands
- **Show Content** – `s` to display current text with cursor position highlighted (green background)
- **Quit** – `q`

## Usage

```bash
python editor.py
