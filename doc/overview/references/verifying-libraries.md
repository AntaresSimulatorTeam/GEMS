<div style="display: flex; justify-content: flex-end;">
  <a href="../../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# Verifying GEMS Libraries

Users may accidentaly modify a library file or download a corrupted version. Verifying the file's integrity against an official SHA-256 hash ensures:

- The file has not been modified
- Simulation results are reproducible
- Debugging is simplified by eliminating file inconsistencies

## What is a SHA-256 hash?

A SHA-256 hash is a unique fingerprint of a file. 
- Any change — even a single character — produces a completely different hash. 
- Identical files always produce the same hash.

## Where to find the official hash

Each library's official SHA-256 hash is published alongside the library in the GitHub repository, as a `.sha256` file:

```
libraries/
  basic_models_library.yml
  basic_models_library.yml.sha256   ← official hash is here
  ...
```

Always use the hash corresponding to the exact version you downloaded. You can find
the `.sha256` files in the
[`libraries/` directory on GitHub](https://github.com/AntaresSimulatorTeam/GEMS/tree/main/libraries).

Example content of `basic_models_library.yml.sha256`:

```
4809d2...  basic_models_library.yml
```

## How to compute the hash locally

**Linux / macOS**

```bash
sha256sum basic_models_library.yml
```

**Windows (PowerShell)**

```powershell
Get-FileHash basic_models_library.yml -Algorithm SHA256
```

**Windows (alternative)**

```cmd
certutil -hashfile basic_models_library.yml SHA256
```

## How to verify the library

1. Download the library file from GitHub (e.g. `basic_models_library.yml`)
2. Open the corresponding `.sha256` file on GitHub to get the official hash
3. Compute the hash of your downloaded file using one of the commands above
4. Compare the two hash values

| Result | Meaning |
|--------|---------|
| Hashes **match** | The file is identical to the official release |
| Hashes **differ** | The file has been modified, corrupted, or is not the official version |

## Example verification

We can compare the two basic-models-library SHA
Official: 4809d22d8...
Local: 4809d22d8...

Result: Match (file is identical)

## Workflow summary

```
1. Download library file from GitHub
         ↓
2. Locate the .sha256 file on GitHub
         ↓
3. Compute the hash locally (sha256sum / Get-FileHash / certutil)
         ↓
4. Compare the two values
         ↓
   Match → OK    |    Differ → re-download or report an issue
```
