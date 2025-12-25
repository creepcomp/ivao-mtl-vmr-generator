# IVAO MTL VMR Generator

A small Python script that generates a **vPilot VMR file** (`ivaomtl.vmr`) from the **IVAO MTL** model library for Microsoft Flight Simulator.

## Requirements

- Python **3.8+**
- **IVAO MTL** installed for MSFS.

## How to Use

1. Place the script in:
```
Packages/Community/IVAO_MTL
````

2. Run the script using Python:
```bash
python generate.py
````

3. Wait until the process finishes.

4. The file **`ivaomtl.vmr`** will be created in the same folder as the script.

5. In **vPilot**, select the generated VMR file:

```
Settings → Model Matching (MSFS) → Custom Rules
```

## Notes

* This script supports **IVAO MTL only**.
