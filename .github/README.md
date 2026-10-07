Modern, lightweight Version Detector data pack with minimal footprint and actual pack format detection. Intended as a dependency for all sorts of other packs.

## VerSion

In Minecraft Vanilla, there is no simple command (or any source, that is) providing the currently running Minecraft [data pack format](https://minecraft.wiki/w/Pack_format) to datapacks.

VerSion addresses this issue and may be used as an API by other datapacks to get the current lots of info about the current version. Using overlays, VerSion achieves this goal in a sturdy and future-proof manner, while most of the time (when a player is online, that is), it obtains exact precision.

In contrast to existing alternatives, VerSion covers way more formats, does not throw faulty errors (when in reality, everything's working) or display excessive amounts of notices, and thus may be used elegantly and in any form of datapack project you plan to implement. Of course, it is free of charge and open-source forever.

> [!NOTE]
> VerSion is automatically built using [beet](https://github.com/mcbeet/beet), which rules out many typo-ish errors but could introduce some Python ones. Please report any unexpected behaviour. Thanks!

### How to use

Functions:
* `function ver:sion`, returns current (major) pack format as an int (available 23w44a and later)
* `function ver:load` to reload version info (runs automatically on world startup and `/reload`)
* `function ver:print` to print current version info to the executor

On every reload, VerSion stores the current pack format as an Integer and the name of the (earliest, or earliest release) Minecraft version using that format as a String inside a [data storage](https://minecraft.wiki/w/Command_storage). If lost, this information may always be refetched by running `/function ver:load`.

Often (e.g. if at least 1 player is inside the world), VerSion also stores the exact version and many other of its available parameters in `storage ver:sion Current`. In particular, this uses the structure of [Misode's mcmeta version data](https://github.com/misode/mcmeta/blob/summary/versions/data.json).

```mcfunction
#always provided: pack format
data get storage ver:sion Current.data_pack_version

#always provided (sometimes most probable is used): version name
data get storage ver:sion Current.name

#might be provided: info about exact version, e.g. resource pack format
data get storage ver:sion Current.resource_pack_version
```

To make use of that information in your pack, use `execute store ... run data get storage ver:sion Current.data_pack_version` or `data modify ... from storage ver:sion (Current.name)`.

**For formats beginning with 23 (versions 23w44a and later), the most convenient way to get the pack format is `function ver:sion` which simply returns the current pack format.**

### Supported versions

If the datapack is marked as being for an older/newer version when investigated, it means no correct version info will be supplied or some functions could fail to load completely. Due to the way VerSion works out the current pack format, only version 1.20.2 and later (specifically, beginning 23w31a) may be detected. For simplicity, only the major format number is taken into account.

Currently, all versions up to 26.4 Snapshot 3 – pack format 123.0 – are detected, however this will be quickly expanded when Minecraft updates progress further.

## Versioning and License

VerSion uses [Semantic Versioning](https://semver.org); in particular, the major version number is changed if (and only if) breaking changes are made regarding some supported use of VerSion. Files inside the `ver:_/...` folder are considered internal and not covered by this.

VerSion is licensed under the [GNU Lesser General Public License](/LICENSE).