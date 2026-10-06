data remove storage ver:sion Current
function ver:_/overlay_data
data modify storage ver:sion Current."data_version" set from entity @p DataVersion
execute if data storage ver:sion Current."data_version" run function ver:_/fetch_data with storage ver:sion Current
