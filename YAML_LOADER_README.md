# YAML Dynamic Loader - Complete Solution

## 🎯 Objective

Dynamically load public YAML files from GitHub and display them in your MkDocs documentation with an interactive interface.

## ✨ Features

- ✅ **Dynamic Loading** : YAML files loaded from GitHub (raw.githubusercontent.com)
- ✅ **Automatic Validation** : YAML structure validated against a schema
- ✅ **Interactive Interface** : Buttons automatically generated to navigate between sections
- ✅ **Error Handling** : Clear and informative error messages
- ✅ **Client-Side** : No backend required, pure JavaScript technology
- ✅ **Responsive** : Adapted for mobile and desktop devices
- ✅ **Dark Theme** : Automatic support for light/dark modes
- ✅ **Secure** : HTML escaping and strict validation

## 🚀 Quick Start

### 1. Check the `mkdocs.yml` configuration

Your `mkdocs.yml` should include:

```yaml
extra_javascript:
  - https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js
  - javascripts/yaml-loader.js

extra_css:
  - stylesheets/yaml-loader.css
```

✅ **Status** : Already configured in your GEMS project.

### 2. Use in a Markdown file

```html
<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/owner/repo/branch/path/to/file.yaml"></div>
```

### 3. That's it! 🎉

The YAML file will load automatically and display sections as interactive buttons.

## 📦 Files provided

```
📁 doc/
├── 📄 javascripts/yaml-loader.js        ← Main engine
├── 📄 stylesheets/yaml-loader.css       ← Styles
├── 📄 3_User_Guide/yaml_loader_guide.md ← User guide
└── 📄 YAML_LOADER_TECHNICAL.md          ← Technical documentation

📁 resources/
└── 📄 yaml-loader-example.yaml          ← Test file
```

## 🎓 Required YAML Structure

Your YAML files must respect this structure:

```yaml
sections:
  - title: "First section title"
    content: |
      Raw content of the section.
      Can contain multiple lines.
  - title: "Second section title"
    content: |
      Raw content of section 2.
```

## 📚 Documentation

### For users

- [Complete user guide](doc/3_User_Guide/yaml_loader_guide.md) - How to integrate and use the solution
- [Practical examples](doc/3_User_Guide/yaml_loader_guide.md#practical-use-cases) - Real-world use cases

### For developers

- [Technical documentation](doc/YAML_LOADER_TECHNICAL.md) - Architecture, API, troubleshooting
- [Annotated source code](doc/javascripts/yaml-loader.js) - Detailed JavaScript functions

## 🔍 Validation

The system automatically validates the YAML structure:

| Validation | Error message |
|---|---|
| `sections` missing | "The YAML must contain a 'sections' property" |
| `sections` not an array | "The 'sections' property must be an array" |
| `sections` empty | "The 'sections' array cannot be empty" |
| Section without `title` | "Each section must have a 'title' property" |
| Section without `content` | "Each section must have a 'content' property" |
| File not found | "HTTP Error 404: Not Found" |

## ⚡ Complete example

### Markdown file (doc.md)

```markdown
# Model configuration

Here are the available models for your system:

<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/main/libraries/basic_models_library.yml"></div>

Click a button to view the details.
```

### Result

- Interactive buttons: "Basic configuration", "Advanced options", etc.
- Content displayed on click
- Automatic error handling

## 🛠️ Advanced configuration

### Load manually with JavaScript

```javascript
const container = document.getElementById('my-container');
const url = 'https://raw.githubusercontent.com/.../file.yaml';
window.loadYAMLFile(container, url);
```

### Customize styles

Edit [doc/stylesheets/yaml-loader.css](doc/stylesheets/yaml-loader.css):

```css
.yaml-loader-button {
    border-color: #your-color;
    color: #your-color;
}
```

## ⚠️ Limitations

- Public YAML files only (no authentication)
- Internet connection required
- Maximum size: ~100 KB per file
- No button hierarchy (flat structure)

## 🔒 Security

✅ **Security measures implemented:**
- HTML escaping to prevent injections
- Strict YAML structure validation
- Verified CDN usage (jsDelivr)
- No JavaScript code execution from YAML

## 🚨 Quick troubleshooting

| Issue | Solution |
|---|---|
| Nothing appears | Check internet connection and URL |
| js-yaml error | Check mkdocs.yml configuration |
| Infinite loading | Test the URL directly in the browser |
| Non-clickable buttons | Check that CSS is loaded |

For more details: [Technical Documentation - Troubleshooting](doc/YAML_LOADER_TECHNICAL.md#troubleshooting)

## 📊 Performance

- **Load time** : < 2 seconds for a file < 100 KB
- **Cache** : Browser + jsDelivr CDN
- **Requests** : 1 single HTTP request per YAML file

## 🤝 Support

- **Questions** : See the [FAQ](doc/6_Support_Contributing/1_faq.md)
- **Issues** : Open a [GitHub issue](https://github.com/AntaresSimulatorTeam/GEMS/issues)
- **Contact** : [Support team](doc/6_Support_Contributing/2_contact.md)

## 📝 License

MIT License - Free to use and modify

## 🔄 Versions and updates

**Current version** : 1.0.0
**Last update** : February 17, 2026

### History

- v1.0.0 (2026-02-17) - Initial version with full support

## 📖 Resources

- **js-yaml** : [Documentation](https://github.com/nodeca/js-yaml)
- **MkDocs Material** : [Docs](https://squidfunk.github.io/mkdocs-material/)
- **GitHub Pages** : [Documentation](https://pages.github.com/)

---

## 🎬 Useful commands

```bash
# Test locally
cd /home/gmaistre/Documents/GEMS/GEMS
mkdocs serve

# Build the documentation
mkdocs build

# Validate a YAML file
# Use https://www.yamllint.com/ or a CLI tool
```

## 📞 Frequently asked questions

**Q: Can I use private YAML files?**
A: No, only public files are accessible without authentication.

**Q: Which YAML files are supported?**
A: All YAML files that respect the defined structure (sections > title + content).

**Q: Can I customize the appearance?**
A: Yes, modify CSS styles or colors in yaml-loader.css.

**Q: How do I handle large files?**
A: Split them into multiple files < 100 KB.

**Q: Does the solution work offline?**
A: No, an internet connection is required to load files from GitHub.

---

**Need help?** See the [complete documentation](doc/YAML_LOADER_TECHNICAL.md) or write on GitHub.
