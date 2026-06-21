# webify

A fast CLI tool to convert images into web-optimized formats. Supports batch conversion from `png`, `jpg`, and `jpeg` to `webp`, plus full favicon set generation from a single source image.

---

## Features

- Converts `png`, `jpg`, and `jpeg` images to `webp`
- Convert a single image file or batch convert every image in a directory
- Use `.` to convert all images in the current directory
- Optional flag to keep or delete original images after conversion
- Favicon generation — creates a full favicon set (PNG, SVG, ICO, web manifest) from a single image

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

### Convert all images in the current directory

```bash
webify wc .
```

### Convert all images in a specific directory

```bash
webify wc /path/to/images
```

### Convert a single image file

```bash
webify wc /path/to/image.png
```

### Convert without deleting original images

```bash
webify wc . --no-delete
webify wc /path/to/images --no-delete
webify wc /path/to/image.png --no-delete
```

### Generate a favicon set from an image

```bash
webify favicon /path/to/image.png
```

### Generate a favicon set with a custom app name and destination

```bash
webify favicon /path/to/image.png --name-app "MyApp" --destination /path/to/output
webify favicon /path/to/image.png -name "MyApp" -dest /path/to/output
```

By default, the favicon set is generated inside a `favicon/` folder next to the source image, and the app name defaults to `MyWebSite`.

---

## Commands

| Command | Description |
|---------|-------------|
| `wc PATH` | Convert a single image file, or all images in a directory, to webp. Use `.` for the current directory |
| `favicon PATH` | Generate a full favicon set from a single source image |

### Options for `wc`

| Option | Default | Description |
|--------|---------|-------------|
| `-f` | `--no-delete` | Whether to delete original images after conversion |
| `--help` | | Show help message |

### Options for `favicon`

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--name-app` | `-name` | `MyWebSite` | App name used in the web manifest and meta tags |
| `--destination` | `-dest` | Parent directory of the source image | Output directory where the `favicon/` folder will be created |
| `--help` | | | Show help message |

---

## Project Structure

```
Webify/
├── app/
│   ├── main.py
│   ├── commands/
│   └── core/
│   └── utils/
├── pyproject.toml
└── README.md
```

---

## License

Apache License
