# DESIGN NOTES

## Q1
- Clear separation into functions: encrypt_file, decrypt_file, verify_files.
- Exactly follow shifting rules by case and alphabet half.
- Preserve all non-letters unchanged.

## Q2
- Load all CSVs dynamically from `temperatures/`.
- Melt months to long format → map months to Australian seasons.
- Ignore NaNs by dropping them before calculations.
- Ties are written fully (one line per station).

## Q3
- Koch-like indentation applied recursively on each edge.
- Parameters validated (sides >= 3, depth >= 0, length > 0).
