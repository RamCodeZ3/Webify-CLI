# webify

A fast CLI tool to convert images into web-optimized formats. Supports batch conversion from `png`, `jpg`, and `jpeg` to `webp` — with favicon generation coming soon.

---

## Features

- Converts `png`, `jpg`, and `jpeg` images to `webp`
- Batch conversion — processes all images in a directory at once
- Uses the current directory by default (no need to pass a path)
- Optional flag to keep or delete original images after conversion
- Favicon generation _(coming soon)_

---

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) — recommended for installation

---

## Installation

### Using uv (recommended)

```bash
git clone https://github.com/your-username/CLI-webp.git
cd CLI-webp
uv tool install .
```

After installation, the `webify` command is available globally in your terminal — no virtual environment activation needed.

### Verify installation

```bash
webify --help
```

---

## Usage

### Convert images in the current directory

```bash
webify wc
```

### Convert images in a specific directory

```bash
webify wc /path/to/images
```

### Convert without deleting original images

```bash
webify wc --no-delete
webify wc /path/to/images --no-delete
```

---

## Commands

| Command | Description |
|---------|-------------|
| `wc [PATH]` | Convert images to webp in the given path or current directory |

### Options for `wc`

| Option | Default | Description |
|--------|---------|-------------|
| `--delete/--no-delete` | `--delete` | Whether to delete original images after conversion |
| `--help` | | Show help message |

---

## Project Structure

```
CLI-webp/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── commands/
│   │   ├── __init__.py
│   │   └── converter_webp.py
│   └── core/
│       ├── __init__.py
│       └── converter.py
├── pyproject.toml
└── README.md
```

---

## Roadmap

- [x] Convert `png`, `jpg`, `jpeg` → `webp`
- [x] Batch conversion by directory
- [ ] Favicon generation from image
- [ ] Recursive directory conversion
- [ ] Output directory option

---

## License

MIT
