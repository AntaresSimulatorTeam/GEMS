# Verifying GEMS Libraries

Users may accidentally modify a [library file](../../user-guide/file-structure/library.md) or download a corrupted version from the [reference libraries](libraries.md). Verifying the file's integrity against an official SHA-256 hash ensures:

- The file has not been modified
- Simulation results are reproducible
- Debugging is simplified by eliminating file inconsistencies

## What is a SHA-256 hash?

A SHA-256 hash is a unique fingerprint of a file. 

- Any change - even a single character - produces a completely different hash. 
- Identical files always produce the same hash.

## Where to find the official hash

Each library's official SHA-256 hash is published alongside the library in the GitHub repository, as a `.sha256` file:

```
libraries/
  basic_models_library.yml
  basic_models_library.yml.sha256   ← official hash is here
  ...
```

Always use the hash corresponding to the exact version you downloaded. You can find the `.sha256` files in the `libraries/` [directory on GitHub](https://github.com/AntaresSimulatorTeam/GEMS/tree/main/libraries).

Example content of `basic_models_library.yml.sha256`:

```
4809d2...  basic_models_library.yml
```

## How to compute the hash locally

> `sha256sum` or `Get-FileHash` are already installed in Linux/macOS and Windows. So, no installation is needed for these commands 

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

Online

1. Download the library file from Github (e.g. ...) as well as the corresponding .sha256 file.

Offline

2. Create your test case offline, manipulating the library and building a system.
3. Consistency check before running the simulation:

    - Compute the hash of your downloaded file using one of the commands above
    - Compare the two hash values :

      | Result | Meaning |
      |--------|---------|
      | Hashes **match** | The file is identical to the official release |
      | Hashes **differ** | The file has been modified, corrupted, or is not the official version |

???+ info "Example verification"

    We can compare the two basic-models-library SHA
    Official: 4809d22d8...
    Local: 4809d22d8...
    Result: Match (file is identical)

