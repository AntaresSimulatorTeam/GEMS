# 📑 YAML Dynamic Loader - Index and Navigation

## 🎯 Where to start?

### 🚀 I'm in a hurry (5 min)
1. Read [YAML_LOADER_QUICKSTART.md](YAML_LOADER_QUICKSTART.md)
2. Add one HTML line to your Markdown
3. Launch `mkdocs serve`
→ **Time: ~5 minutes**

### 📚 I want to understand (15 min)
1. Read [YAML_LOADER_README.md](YAML_LOADER_README.md)
2. Look at the [practical examples](doc/3_User_Guide/yaml_loader_integration_example.md)
3. Check the [required YAML structure](doc/3_User_Guide/yaml_loader_guide.md#yaml-file-structure)
→ **Time: ~15 minutes**

### 🔧 I'm a developer (30 min)
1. Read the [architecture](doc/YAML_LOADER_TECHNICAL.md#architecture)
2. Explore the [source code](doc/javascripts/yaml-loader.js)
3. Check the [JavaScript API](doc/YAML_LOADER_TECHNICAL.md#api)
4. Troubleshoot with the [technical guide](doc/YAML_LOADER_TECHNICAL.md)
→ **Time: ~30 minutes**

---

## 📖 All documents

### 📌 Starting points
- **[YAML_LOADER_QUICKSTART.md](YAML_LOADER_QUICKSTART.md)** - Ultra-fast guide (recommended)
- **[YAML_LOADER_README.md](YAML_LOADER_README.md)** - Complete overview

### 📚 User documentation
- **[doc/3_User_Guide/yaml_loader_guide.md](doc/3_User_Guide/yaml_loader_guide.md)** - Complete usage guide
- **[doc/3_User_Guide/yaml_loader_integration_example.md](doc/3_User_Guide/yaml_loader_integration_example.md)** - Integrated practical examples
- **[doc/3_User_Guide/yaml-loader-example.yaml](resources/yaml-loader-example.yaml)** - Test YAML file

### 🔧 Technical documentation
- **[doc/YAML_LOADER_TECHNICAL.md](doc/YAML_LOADER_TECHNICAL.md)** - Complete documentation for developers
- **[doc/javascripts/yaml-loader.js](doc/javascripts/yaml-loader.js)** - Annotated source code (~400 lines)
- **[doc/stylesheets/yaml-loader.css](doc/stylesheets/yaml-loader.css)** - CSS styles

### ⚙️ Configuration
- **[mkdocs.yml](mkdocs.yml)** - MkDocs configuration (already modified ✓)

### 🧪 Tools
- **[check-yaml-loader-installation.sh](check-yaml-loader-installation.sh)** - Installation verification script

---

## 📋 Detailed table of contents

### YAML_LOADER_QUICKSTART.md
- ⚡ In 30 seconds
- 📋 Required YAML structure
- 🔥 Complete example
- ❓ Troubleshooting in 10 seconds
- 3 examples from simple to complex

### YAML_LOADER_README.md
- 🎯 Objective
- ✨ Features
- 🚀 Quick start
- 📦 Files provided
- 🎓 Required YAML structure
- ⚡ Complete example
- 🛠️ Advanced configuration
- ⚠️ Limitations
- 🔒 Security
- 🚨 Quick troubleshooting

### doc/3_User_Guide/yaml_loader_guide.md
- 📌 Quick reminder
- 💡 Initial setup
- Required structure
- Using in Markdown (2 methods)
- Automatic validation
- Error handling
- Practical use cases
- Limitations and best practices
- Detailed troubleshooting
- Complete example
- JavaScript API

### doc/3_User_Guide/yaml_loader_integration_example.md
- 📌 Quick reminder
- 💡 Example 1: Display a library
- 💡 Example 2: Display a configuration
- 💡 Example 3: Multiple integration
- Ready-to-use template
- URL references
- Integration checklist
- Common issues
- Best practices

### doc/YAML_LOADER_TECHNICAL.md
- Architecture (with diagrams)
- Load flow
- Installation step by step
- Configuration (JS variables and CSS styles)
- Usage (2 methods)
- Complete API
- Validation (schema and examples)
- Error handling (types and processing)
- Advanced troubleshooting
- Advanced examples
- Performance and optimization
- Support and contribution

---

## 🔍 Quick search

### I want to...

**Display a YAML file in my documentation**
→ [YAML_LOADER_QUICKSTART.md](YAML_LOADER_QUICKSTART.md)

**Understand the required YAML structure**
→ [YAML_LOADER_README.md](YAML_LOADER_README.md#-required-yaml-structure)

**See a complete practical example**
→ [doc/3_User_Guide/yaml_loader_integration_example.md](doc/3_User_Guide/yaml_loader_integration_example.md)

**Customize the appearance (colors, fonts)**
→ [doc/YAML_LOADER_TECHNICAL.md#configuration](doc/YAML_LOADER_TECHNICAL.md#configuration)

**Load a YAML file in JavaScript**
→ [doc/YAML_LOADER_TECHNICAL.md#api](doc/YAML_LOADER_TECHNICAL.md#api)

**Solve an error**
→ [doc/YAML_LOADER_TECHNICAL.md#troubleshooting](doc/YAML_LOADER_TECHNICAL.md#troubleshooting)

**Check that the installation is correct**
→ `bash check-yaml-loader-installation.sh`

**See the annotated source code**
→ [doc/javascripts/yaml-loader.js](doc/javascripts/yaml-loader.js)

**Test with an example YAML file**
→ [resources/yaml-loader-example.yaml](resources/yaml-loader-example.yaml)

---

## 📊 File overview

```
GEMS/
├── 📄 YAML_LOADER_QUICKSTART.md        ← START HERE (5 min)
├── 📄 YAML_LOADER_README.md            ← Main guide
├── 📄 YAML_LOADER_TECHNICAL.md         ← Technical docs
├── 📄 check-yaml-loader-installation.sh ← Check installation
├── 📄 mkdocs.yml                        ← Config (already modified ✓)
│
├── 📁 doc/
│   ├── 📁 javascripts/
│   │   └── 📄 yaml-loader.js           ← Main code
│   ├── 📁 stylesheets/
│   │   └── 📄 yaml-loader.css          ← Styles
│   ├── 📄 YAML_LOADER_TECHNICAL.md
│   └── 📁 3_User_Guide/
│       ├── 📄 yaml_loader_guide.md     ← Complete guide
│       └── 📄 yaml_loader_integration_example.md ← Examples
│
└── 📁 resources/
    └── 📄 yaml-loader-example.yaml     ← Test file
```

---

## ✅ Quick check

Have you modified your `mkdocs.yml`?

Each line must be present:

```yaml
extra_javascript:
  - https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js
  - javascripts/yaml-loader.js

extra_css:
  - stylesheets/yaml-loader.css
```

✅ If yes, you're ready! Start with the [Quick Start](YAML_LOADER_QUICKSTART.md).

---

## 📱 For different devices

### 💻 Desktop / Laptop
→ All documentation works perfectly

### 📱 Smartphone / Tablet
→ Buttons adapt automatically (responsive design)

### 🌐 Online (mkdocs serve)
→ Everything works: `mkdocs serve`

### 🖥️ Static build
→ Everything works: `mkdocs build`

### 📄 MkDocs themes
→ Compatible with Material (current theme)
→ Should work with other themes too

---

## 🤝 Support

### Questions?
1. See the [FAQ](doc/6_Support_Contributing/1_faq.md)
2. Check the [complete troubleshooting](doc/YAML_LOADER_TECHNICAL.md#troubleshooting)
3. Contact the team: [support](doc/6_Support_Contributing/2_contact.md)

### Bug or feature?
→ Open a [GitHub issue](https://github.com/AntaresSimulatorTeam/GEMS/issues)

### Contribution?
→ See [CONTRIBUTING.md](doc/6_Support_Contributing/3_contributing.md)

---

## 🎓 Got a few minutes to test?

Quick command to check that everything works:

```bash
# Check installation
bash check-yaml-loader-installation.sh

# Launch MkDocs
mkdocs serve

# Then: http://localhost:8000
```

---

**Status**: ✅ Complete installation and ready to use!

**Last update**: February 17, 2026

**Questions?** Start with [YAML_LOADER_QUICKSTART.md](YAML_LOADER_QUICKSTART.md) 🚀
