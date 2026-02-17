# YAML Dynamic Loader - Quick Start

## ⚡ In 30 seconds

Do you want to display a YAML file in your MkDocs documentation? It's barely 1 line of code!

### Step 1️⃣ : Configuration (ALREADY DONE ✓)

Your `mkdocs.yml` is already configured with:
- ✅ js-yaml CDN
- ✅ yaml-loader.js
- ✅ yaml-loader.css

### Step 2️⃣ : Add to your Markdown

```html
<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/owner/repo/branch/path/file.yaml"></div>
```

### Step 3️⃣ : That's it! 🎉

Launch `mkdocs serve` and you'll see the buttons display automatically.

---

## 📋 Required YAML Structure

Your YAML file must respect this structure:

```yaml
sections:
  - title: "My title"
    content: |
      My raw content
      Can be on multiple lines
  - title: "Another section"
    content: |
      Other content
```

---

## 🔥 Complete example

### File : `doc/1_Overview/1_Architecture.md`

```markdown
# GEMS Architecture

Here are the available models:

<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/main/libraries/basic_models_library.yml"></div>

Click a button to see the details.
```

### Result

The buttons appear automatically from the YAML file! 🚀

---

## ❓ Troubleshooting in 10 seconds

| Issue | Cause | Solution |
|----------|-------|----------|
| Nothing appears | Wrong URL | test the URL directly |
| Error 404 | File missing | check the path |
| Invalid YAML | Wrong structure | [https://yamllint.com](https://yamllint.com) |
| js-yaml not found | Config mkdocs.yml | reread `mkdocs.yml` |

---

## 📚 Need more?

- [Complete guide](3_User_Guide/yaml_loader_guide.md) - All the details
- [Practical examples](3_User_Guide/yaml_loader_integration_example.md) - Real-world cases
- [Technical docs](YAML_LOADER_TECHNICAL.md) - For developers
- [Main README](../YAML_LOADER_README.md) - Everything about the solution

---

## 🎓 3 examples from simplest to most complex

### 1️⃣ Simple (recommended)

```html
<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/.../file.yaml"></div>
```

### 2️⃣ With comment

```markdown
## Configuration

<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/.../file.yaml"></div>

[View source file](https://github.com/.../file.yaml)
```

### 3️⃣ Advanced (JavaScript)

```html
<div id="my-yaml" class="yaml-loader-container"></div>
<script>
window.loadYAMLFile(
  document.getElementById('my-yaml'),
  'https://raw.githubusercontent.com/.../file.yaml'
);
</script>
```

---

## 📦 Files provided

```
doc/javascripts/yaml-loader.js       ← Magic code
doc/stylesheets/yaml-loader.css      ← Design
mkdocs.yml                            ← Configuration (modified)
resources/yaml-loader-example.yaml   ← Test file
```

---

## 🚀 Go!

1. Get your YAML URL from GitHub
2. Create a `<div>` with `data-yaml-url`
3. Launch `mkdocs serve`
4. 🎉 Done!

---

**More questions?** Launch the installation checker:

```bash
bash check-yaml-loader-installation.sh
```

Enjoy! 🎈
