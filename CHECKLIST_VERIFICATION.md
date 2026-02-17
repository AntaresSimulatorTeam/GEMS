# ✅ YAML Dynamic Loader - Complete Checklist

## 🎯 Objective

Verify that the YAML Dynamic Loader solution is correctly installed and functional.

---

## 📋 Phase 1: System Files

### Step 1.1: JavaScript and CSS Files

- [ ] File exists: `doc/javascripts/yaml-loader.js`
  - [ ] Contains `function loadYAML`
  - [ ] Contains `validateYAMLStructure`
  - [ ] Contains `parseYAML`
  - [ ] Contains `renderYAMLContent`

- [ ] File exists: `doc/stylesheets/yaml-loader.css`
  - [ ] Contains `.yaml-loader-container`
  - [ ] Contains `.yaml-loader-button`
  - [ ] Responsive styles present
  - [ ] Dark mode (@media dark) present

### Step 1.2: Documentation Files

- [ ] File exists: `YAML_LOADER_README.md`
- [ ] File exists: `YAML_LOADER_QUICKSTART.md`
- [ ] File exists: `INDEX_YAML_LOADER.md`
- [ ] File exists: `IMPLEMENTATION_SUMMARY.md`
- [ ] File exists: `doc/YAML_LOADER_TECHNICAL.md`
- [ ] File exists: `doc/3_User_Guide/yaml_loader_guide.md`
- [ ] File exists: `doc/3_User_Guide/yaml_loader_integration_example.md`

### Step 1.3: Test Files

- [ ] File exists: `resources/yaml-loader-example.yaml`
- [ ] File exists: `check-yaml-loader-installation.sh`
- [ ] Script is executable: `chmod +x check-yaml-loader-installation.sh`

---

## ⚙️ Phase 2: MkDocs Configuration

### Step 2.1: JavaScript Configuration

Open `mkdocs.yml` and verify:

- [ ] Section `extra_javascript` exists
- [ ] Contains: `https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js`
- [ ] Contains: `javascripts/yaml-loader.js`
- [ ] Correct order: js-yaml **before** yaml-loader.js

### Step 2.2: CSS Configuration

- [ ] Section `extra_css` exists
- [ ] Contains: `stylesheets/yaml-loader.css`

**Code to verify in mkdocs.yml:**
```yaml
extra_javascript:
  - https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js
  - javascripts/yaml-loader.js

extra_css:
  - stylesheets/yaml-loader.css
```

---

## 🧪 Phase 3: Functional testing

### Step 3.1: Installation verification

```bash
# Run the verification script
bash check-yaml-loader-installation.sh
```

Expected result:
```
✓ File found: doc/javascripts/yaml-loader.js
✓ File found: doc/stylesheets/yaml-loader.css
✓ Content found in: mkdocs.yml
...
✓ Installation successful!
```

- [ ] Script returns exit code 0
- [ ] All files are found
- [ ] All checks pass

### Step 3.2: Local testing

```bash
# Navigate to GEMS folder
cd /home/gmaistre/Documents/GEMS/GEMS

# Launch MkDocs server
mkdocs serve
```

Expected result:
```
INFO    -  Building documentation...
...
INFO    -  Started server process [XXXXXX]
INFO    -  Uvicorn running on http://127.0.0.1:8000
```

- [ ] No errors in logs
- [ ] Page accessible at http://localhost:8000

### Step 3.3: Browser testing

1. Open http://localhost:8000
2. Go to a page with content
3. Verify that resources load:

**Browser console (F12):**

- [ ] No 404 errors for `yaml-loader.js`
- [ ] No 404 errors for `yaml-loader.css`
- [ ] js-yaml is loaded: `console.log(typeof jsyaml)` → "object"

---

## 🎨 Phase 4: Content testing

### Step 4.1: Create a test file

Temporarily create `test.md` in `doc/`:

```markdown
# Test YAML Dynamic Loader

<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/main/resources/yaml-loader-example.yaml"></div>

Click the buttons above.
```

- [ ] File created

### Step 4.2: Add to navigation

In `mkdocs.yml`, add to the `nav` section:

```yaml
nav:
  # ... other entries ...
  - Test YAML Loader: test.md
```

- [ ] Entry added

### Step 4.3: Refresh and test

1. Refresh http://localhost:8000
2. Navigate to "Test YAML Loader"
3. Verify there are no errors

**Expected:**

- [ ] 4 buttons display:
  - "Basic configuration"
  - "Advanced options"
  - "Network configuration"
  - "Additional documentation"

- [ ] Clicking a button displays content
- [ ] Content is raw text
- [ ] No error messages

### Step 4.4: Cleanup

```bash
# Delete test file
rm doc/test.md

# Restore mkdocs.yml (undo nav addition)
```

- [ ] File deleted
- [ ] mkdocs.yml cleaned

---

## 📱 Phase 5: Compatibility testing

### Step 5.1: Different browsers

Test on each available browser:

- [ ] Chrome/Chromium - Works
- [ ] Firefox - Works
- [ ] Safari - Works
- [ ] Edge - Works

**What to verify:**
- Buttons appear
- Clicks change displayed content
- No JavaScript errors

### Step 5.2: Responsive design

Test by resizing the window:

- [ ] Desktop (> 1200px) - Buttons well aligned
- [ ] Tablet (~768px) - Buttons in line
- [ ] Mobile (< 480px) - Buttons stacked

### Step 5.3: Dark mode

Dark mode from browser or theme:

- [ ] Colors adapted to theme
- [ ] Text remains readable
- [ ] No poor contrast

---

## 🔒 Phase 6: Security

### Step 6.1: Security checks

Browser console (F12):

```javascript
// Verify jsyaml is loaded
console.log(typeof jsyaml); // "object"

// Verify loadYAMLFile exists
console.log(typeof window.loadYAMLFile); // "function"
```

- [ ] jsyaml is available
- [ ] loadYAMLFile is available

### Step 6.2: HTML escaping test

Modify the example file with this content:

```yaml
sections:
  - title: "Test <script>"
    content: |
      <div>Test</div>
      "Quotes"
      'Apostrophes'
```

- [ ] Characters `<`, `>`, `"`, `'` are escaped
- [ ] Nothing is executed
- [ ] Correct display of raw text

---

## 📖 Phase 7: Documentation

### Step 7.1: Verify files

- [ ] Each doc file has non-empty content
- [ ] Each file has a title (#)
- [ ] Internal links are valid

### Step 7.2: Verify accessibility

All doc files should be accessible from:

- [ ] `YAML_LOADER_README.md` - Main entry point
- [ ] `YAML_LOADER_QUICKSTART.md` - Quick guide
- [ ] `INDEX_YAML_LOADER.md` - Navigation index
- [ ] `IMPLEMENTATION_SUMMARY.md` - Summary
- [ ] `doc/YAML_LOADER_TECHNICAL.md` - Technical docs
- [ ] `doc/3_User_Guide/` - User guides

---

## 🚀 Phase 8: Advanced features

### Step 8.1: Manual JavaScript loading

Browser console:

```javascript
const container = document.createElement('div');
container.classList.add('yaml-loader-container');
document.body.appendChild(container);

window.loadYAMLFile(container, 'https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/main/resources/yaml-loader-example.yaml');
```

- [ ] Function runs without error
- [ ] Content displays in container

### Step 8.2: Error handling

Test with an invalid URL:

```javascript
window.loadYAMLFile(container, 'https://raw.githubusercontent.com/invalid/url.yaml');
```

- [ ] Error message displays
- [ ] Message is clear and useful

---

## 💾 Phase 9: Deployment

### Step 9.1: Static build

```bash
mkdocs build
```

- [ ] No errors in build
- [ ] Files generated in `site/` folder

### Step 9.2: Verify generated site

Open `site/index.html` in browser:

- [ ] Site displays correctly
- [ ] Static links work
- [ ] CSS/JS resources load

### Step 9.3: GitHub Pages deployment

(If applicable)

- [ ] Site deployed on GitHub Pages
- [ ] Accessible without errors
- [ ] YAML Loader works on live site

---

## 📊 Phase 10: Final verification

### Verification summary

| Phase | Status | Notes |
|-------|--------|-------|
| 1. System files | ☐ | |
| 2. MkDocs configuration | ☐ | |
| 3. Functional testing | ☐ | |
| 4. Content testing | ☐ | |
| 5. Compatibility | ☐ | |
| 6. Security | ☐ | |
| 7. Documentation | ☐ | |
| 8. Advanced features | ☐ | |
| 9. Deployment | ☐ | |

### ✅ All good!

If all checkboxes are checked:

1. **Create a test repository** (optional, for documentation)
   ```bash
   mkdir -p ~/test-yaml-loader
   cd ~/test-yaml-loader
   ```

2. **Start using in your documentation**
   ```html
   <div class="yaml-loader-container" data-yaml-url="..."></div>
   ```

3. **Consult guides** for advanced use cases

---

## 🆘 Problems during verification?

### If a checkbox isn't checked:

1. Check `[doc/YAML_LOADER_TECHNICAL.md#troubleshooting](doc/YAML_LOADER_TECHNICAL.md#troubleshooting)`
2. Run `bash check-yaml-loader-installation.sh` for diagnosis
3. Check browser logs (F12 > Console)
4. Open an issue on GitHub if needed

### Useful commands

```bash
# Verify installation
bash check-yaml-loader-installation.sh

# Launch local server
mkdocs serve

# Build documentation
mkdocs build

# Clean generated files
rm -rf site/

# Reset browser cache
Ctrl+Shift+R (Firefox/Chrome) or Shift+Command+R (Safari)
```

---

## 📚 Next steps

Once everything is verified:

1. **Review the guides**
   - [YAML_LOADER_QUICKSTART.md](YAML_LOADER_QUICKSTART.md)
   - [doc/3_User_Guide/yaml_loader_guide.md](doc/3_User_Guide/yaml_loader_guide.md)

2. **Find a YAML file to display**
   - Your own files on GitHub
   - Files from GEMS documentation

3. **Integrate into your documentation**
   - Add HTML containers
   - Test with `mkdocs serve`

4. **Deploy**
   - Publish on GitHub Pages
   - Share with your team

---

## 🎉 Congratulations!

You have successfully installed and verified **YAML Dynamic Loader**!

You can now:
- ✅ Display YAML files dynamically
- ✅ Create interactive documentation
- ✅ Link your documentation to GitHub sources

**Great job!** 🚀

---

**Last check**: February 17, 2026
**Estimated duration**: 30-60 minutes to verify everything
**Expected difficulties**: None, everything is automated!
