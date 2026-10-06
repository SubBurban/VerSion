from beet import Context, JsonFile, DataPack, Function
import json
from urllib.request import urlopen


def overlays(ctx: Context):
    entries = []
    with urlopen(
        "https://raw.githubusercontent.com/misode/mcmeta/refs/heads/summary/versions/data.json"
    ) as response:
        data = JsonFile(json.load(response)).data
    for version in data:
        format = version["data_pack_version"]
        if format < 16: # packs before 16 didn't support overlays, lol
            continue
        if any(entry["formats"] == format for entry in entries):
            continue
        
        
        pack = DataPack()
        pack.supported_formats = pack.min_format = pack.max_format = format

        matching_versions = [
            version for version in data
            if version["data_pack_version"] == format
        ]
        stable_versions = [version for version in matching_versions if version.get("stable") is True]
        if stable_versions:
            matching_versions = stable_versions
        name = min(matching_versions, key=lambda version: version["data_version"])["name"]
        
        funcSion = Function([f"return {format}"])
        funcLoad = Function([f"data modify storage ver:sion Current set value {{Format:{format},Name:\"{name}\"}}"])
        
        if format < 45: #for formats <45, "functions" was "function", however beet doesn't seem to support that, so manually it is
            if format >= 23:
                pack.extra["data/ver/functions/sion.mcfunction"] = funcSion
            pack.extra["data/ver/functions/_/overlay_data.mcfunction"] = funcLoad
        else:
            pack.functions["ver:sion"] = funcSion
            pack.functions["ver:_/overlay_data"] = funcLoad
        ctx.data.overlays[f"format_{format}"] = pack
    #ctx.data.mcmeta.data["overlays"]["entries"] = entries

def globals(ctx: Context):
    # load tags & overlay fallback function
    ctx.data.extra["data/minecraft/tags/functions/load.json"] = ctx.data.function_tags["minecraft:load"] = JsonFile({"values": ["ver:load"], "replace": False})
    ctx.data.extra["data/ver/functions/overlay_data.mcfunction"] = ctx.data.functions["ver:overlay_data"] = Function("data modify storage ver:sion Current set value {Format:0,Name:\"Unknown\"}")
    # src function compatibility
    ctx.data.extra["data/ver/functions/load.mcfunction"] = ctx.data.functions["ver:load"]
    ctx.data.extra["data/ver/functions/_/fetch_data.mcfunction"] = ctx.data.functions["ver:_/fetch_data"]
    # pack description
    ctx.data.description = ctx.meta["desc"]
    with urlopen(
			"https://raw.githubusercontent.com/misode/mcmeta/refs/heads/summary/versions/data.json"
		) as response:
            data = JsonFile(json.load(response)).data
    # supported pack format ranges
    ctx.data.min_format = 16 # as macros were also added in 23w31a, we don't do earlier versions
    ctx.data.pack_format = ctx.data.max_format = max(version["data_pack_version"] for version in data)
    ctx.data.supported_formats = {"min_inclusive": ctx.data.min_format, "max_inclusive": ctx.data.max_format}
    # provide data to pack via command storages
    versions_text = json.dumps(data, separators=(",", ":"))
    ctx.data.extra["data/ver/functions/_/version_data.mcfunction"] = ctx.data.functions["ver:_/version_data"] = Function(f"data modify storage ver:sion Data set value {versions_text}")

def print(ctx: Context):
    '''Accounts for the Text Component Overhaul in 1.21.5'''
    pack = DataPack()
    pack.extra["data/ver/functions/print.mcfunction"] = pack.functions["ver:print"] = Function('tellraw @s {"translate":"","fallback":"%s – You are currently running %s","with":[{"text":"VerSion","color":"aqua","clickEvent":{"action":"open_url","value":"https://modrinth.com/datapack/version"}},[{"text":"Minecraft ","hoverEvent":{"action":"show_text","value":["Pack format ",{"nbt":"Current.data_pack_version","storage":"ver:sion"}]}},{"nbt":"Current.name","storage":"ver:sion"}]]}')
    pack.min_format, pack.max_format = 16, 61
    pack.supported_formats = {"min_inclusive":16,"max_inclusive":61}
    ctx.data.overlays["legacy_text_components"] = pack
    
