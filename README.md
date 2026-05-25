# Layer Commander

A Krita plugin that lets you control layers using text commands in a dockable widget. Move, rotate, flip, duplicate layers, and draw shapes — all from a command box.

## Features

- **Move layers** by pixels or percentage of canvas size (`moveby`, `moveto`, `movecenterto`)
- **Center layers** in the document (`center`)
- **Duplicate layers** (`duplicate`)
- **Rotate layers** (`rotate`)
- **Flip layers** horizontally or vertically (`fliphorizontal`, `flipvertical`)
- **Draw shapes** — circles and lines — on the active layer (`circle`, `line`)
- Supports percentages for dimensions (e.g. `moveby 50% 50%`)
- Each command has short aliases (e.g. `mvb` for `moveby`, `cen` for `center`)

## Installation

*you can find kritas documentation on installing a plugin here: [Krita plugin installation guide](https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html).*
### Option 1: Manual install (clone & copy)


```bash
git clone https://github.com/Ben-Collett/layer_commander.git
```

Copy the `layer_commander` folder and `layer_commander.desktop` file to your Krita pykrita directory:

- **Linux:** `~/.local/share/krita/pykrita/`
- **Windows:** `%APPDATA%\krita\pykrit\`
- **macOS:** `~/Library/Application Support/krita/pykrita/`

### Option 2: ZIP install (via Krita's Import Python Plugin)

Run the bundled script to create a ZIP archive:

```bash
python make_zip.py
```

This produces `layer_commander.zip`. Then in Krita go to **Tools > Scripts > Import Python Plugin** and select the zip file.

### Enable the plugin

After installing, restart Krita and enable the plugin via **Settings > Configure Krita > Python Plugin Manager**. Check **Layer Commander**, then restart Krita again. The dock widget appears on the right side of the window.

if not then enable the docker by checking **Settings>Dockers>Layer Commander**

## Usage

1. Select a layer in the layer stack.
2. Type commands into the text box in the Layer Commander dock (one command per line).
3. Click **Execute**.

### Commands

| Command | Alias | Description |
|---|---|---|
| `moveby x y` | `mvb` | Move layer by `x`, `y` pixels |
| `moveto x y` | `mvt` | Move layer to absolute position `x`, `y` |
| `movecenterto x y` | `mvc` | Move layer's center to `x`, `y` |
| `center` | `cen` | Center layer in the document |
| `duplicate` | `dup` | Duplicate active layer above itself |
| `rotate deg` | `rot` | Rotate layer by `deg` degrees |
| `fliphorizontal` | `flh` | Flip layer horizontally |
| `flipvertical` | `flv` | Flip layer vertically |
| `circle x y radius_x [radius_y]` | `cir` | Draw a circle (or ellipse) on the layer |
| `line x1 y1 x2 y2` | `lin` | Draw a line on the layer |
| `help` | `h` | Show help with all commands |

All coordinate parameters accept either pixel values or percentages of the canvas size (e.g., `50%`).

## License

This plugin is licensed under [BSD Zero](LICENSE)
