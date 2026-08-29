from pathlib import Path
import shutil

base_dir = Path(__file__).resolve().parent

category_map = {
    "Civil Engineering & Construction": {
        "IS_17682.json",
        "IS_15833.json",
        "IS_15834.json",
        "IS_4621.json",
        "IS_14912.json",
        "IS_16343.json",
        "IS_3654.json",
        "IS_4992.json",
        "IS_6135.json",
        "IS_14810.json",
        "IS_15351.json",
        "IS_15909.json",
        "IS_16090.json",
        "IS_16654.json",
        "IS_17371.json",
        "IS_10701.json",
        "IS_2191.json",
        "IS_2202.json",
        "IS_4990.json",
        "IS_5509.json",
        "IS_14268.json",
        "IS_1787.json",
    },
    "Electrical & Electrotechnical": {
        "IS_5082.json",
        "IS_12427.json",
        "IS_14255.json",
        "IS_14494.json",
        "IS_17048.json",
        "IS_7098.json",
        "IS_12444.json",
        "IS_1897.json",
    },
    "Mechanical Engineering": {
        "IS_10238.json",
        "IS_6623.json",
        "is_1545.json",
        "IS_13997.json",
        "IS_1783.json",
        "IS_2552.json",
    },
    "Chemical & Petrochemical": {
        "IS_10116.json",
        "IS_11657.json",
        "IS_12084.json",
        "IS_15573.json",
        "IS_16113.json",
        "IS_5158.json",
        "IS_3575.json",
    },
    "Food & Agriculture": {
        "17356.json",
        "IS_16089.json",
        "IS_16390.json",
        "IS_16513.json",
        "IS_16627.json",
        "IS_16718.json",
        "IS_17070.json",
        "IS_17728.json",
        "IS_17731.json",
        "IS_10325.json",
    },
    "Textiles": {
        "IS_10702.json",
        "IS_12254.json",
        "IS_15844.json",
        "IS_16994.json",
        "IS_17043.json",
        "IS_15741.json",
        "IS_16890.json",
        "IS_17051.json",
        "IS_17286.json",
    },
    "Metallurgical Engineering & Metals": {
        "IS_1254.json",
        "IS_16011.json",
        "IS_4171.json",
        "IS_4412.json",
        "IS_2002.json",
        "IS_2062.json",
        "IS_7887.json",
    },
    "Transport Engineering & Automotive": {
        "IS_7902.json",
    },
    "Water Resources & Environmental Engineering": {
        "IS_7092.json",
    },
    "Health & Medical": {
        "IS_19857.json",
        "iIS_17354.json",
        "IS_17349.json",
        "IS_17509.json",
        "IS_17514.json",
        "IS_17630.json",
        "IS_5405.json",
    },
}

old_dirs = [
    "agro-textiles",
    "aluminium-and-aluminium-alloy-products",
    "bolts-nuts-fastners",
    "cables",
    "chemicals-fertilizers-polymers-textiles",
    "copper-products",
    "door-fittings",
    "drums-and-tins",
    "foot-wear",
    "geo-textiles",
    "medical-textiels",
    "plywood-wooden-flush-door-shutter",
    "protective-textiles",
    "steel-iron-product",
]

all_mapped_files = {name for names in category_map.values() for name in names}

# Create destination folders for every non-empty category
for category in category_map:
    (base_dir / category).mkdir(exist_ok=True)

# Move files
moved = 0
for old_dir in old_dirs:
    source_dir = base_dir / old_dir
    if not source_dir.exists():
        continue
    for file_path in sorted(source_dir.iterdir()):
        if not file_path.is_file() or file_path.suffix.lower() != ".json":
            continue
        filename = file_path.name
        matched_category = None
        for category, names in category_map.items():
            if filename in names:
                matched_category = category
                break
        if matched_category is None:
            raise ValueError(f"Unmapped file: {file_path}")
        target = base_dir / matched_category / filename
        if target.exists():
            raise FileExistsError(f"Target already exists: {target}")
        shutil.move(str(file_path), str(target))
        moved += 1

# Remove old empty directories
for old_dir in old_dirs:
    source_dir = base_dir / old_dir
    if source_dir.exists() and not any(source_dir.iterdir()):
        source_dir.rmdir()

# Final summary
print(f"Moved files: {moved}")
for category, names in category_map.items():
    count = len([p for p in (base_dir / category).glob("*.json")])
    print(f"{category}: {count}")
remaining_old_dirs = sorted(p.name for p in base_dir.iterdir() if p.is_dir() and p.name in old_dirs)
print(f"Remaining old directories: {remaining_old_dirs}")
print(f"Expected mapped files: {len(all_mapped_files)}")
