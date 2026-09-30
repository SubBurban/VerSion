Modern, lightweight Version Detector data pack with minimal footprint and actual pack format detection. Intended as a dependency for all sorts of other packs.

## VerSion

In Minecraft Vanilla, there is no simple command (or any source, that is) providing the currently running Minecraft Version or [data pack format](https://minecraft.wiki/w/Pack_format) to datapacks.

VerSion addresses this issue and may be used as an API by other datapacks to get the current pack format. Using overlays, VerSion achieves this goal in an inexpensive, light-weight and future-proof manner.

In contrast to existing alternatives, VerSion covers way more formats, does not throw faulty errors (when in reality, everything's working) or display excessive amounts of notices, and thus may be used elegantly and in any form of datapack project you plan to implement. Of course, it is free of charge and open-source forever.

### How to use

Functions:
* `function ver:sion`, returns current pack format as an int (available 23w44a and later)
* `function ver:load` to reload version info (runs automatically on world startup and `/reload`)
* `function ver:print` to print current version info to the executor

On every reload, VerSion stores the current pack format as an Integer and the name of the (last) Minecraft version using that format as a String inside a [data storage](https://minecraft.wiki/w/Command_storage). If lost, this information may always be refetched by running `/function ver:load`.

```mcfunction
#get the pack format
data get storage ver:sion Format

#get the version
data get storage ver:sion Name
```

To make use of that information in your pack, use `execute store ... run data get storage ver:sion Format` or `data modify ... from storage ver:sion (Format|Name)`.

**For formats beginning with 23 (versions 23w44a and later), the most convenient way to get the pack format is `function ver:sion` which simply returns the current pack format.**

### Supported versions

If the datapack is marked as being for an older/newer version when investigated, that means no correct version info will be supplied. Due to the way VerSion works out the current pack format, only version 1.20.2 and later (specifically, beginning 23w31a) may be detected. For simplicity, only the major format number is taken into account.

Currently, all versions up to 26.3 – pack format 121 – are detected, however this will be quickly expanded when Minecraft updates progress further.
