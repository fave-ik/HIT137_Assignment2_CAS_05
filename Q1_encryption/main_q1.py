from pathlib import Path

RAW = Path(__file__).parent / "raw_text.txt"
OUT_DIR = Path(__file__).parent / "outputs"
ENC = OUT_DIR / "encrypted_text.txt"
DEC = OUT_DIR / "decrypted_text.txt"

ALPH_LO = "abcdefghijklmnopqrstuvwxyz"
ALPH_UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def shift_char(c: str, shift: int, alphabet: str) -> str:
    i = alphabet.find(c)
    if i == -1:
        return c
    return alphabet[(i + shift) % len(alphabet)]

def encrypt_text(s: str, shift1: int, shift2: int) -> str:
    out = []
    for ch in s:
        if ch.islower():
            if ch in ALPH_LO[:13]:
                out.append(shift_char(ch, shift1 * shift2, ALPH_LO))
            elif ch in ALPH_LO[13:]:
                out.append(shift_char(ch, -(shift1 + shift2), ALPH_LO))
            else:
                out.append(ch)
        elif ch.isupper():
            if ch in ALPH_UP[:13]:
                out.append(shift_char(ch, -shift1, ALPH_UP))
            elif ch in ALPH_UP[13:]:
                out.append(shift_char(ch, shift2 ** 2, ALPH_UP))
            else:
                out.append(ch)
        else:
            out.append(ch)
    return "".join(out)

def decrypt_text(s: str, shift1: int, shift2: int) -> str:
    # Build enc->orig map by simulating encryption once, then invert (guaranteed inverse)
    def encrypt_char(ch: str) -> str:
        if ch.islower():
            if ch in ALPH_LO[:13]:
                return shift_char(ch, shift1 * shift2, ALPH_LO)
            elif ch in ALPH_LO[13:]:
                return shift_char(ch, -(shift1 + shift2), ALPH_LO)
            return ch
        if ch.isupper():
            if ch in ALPH_UP[:13]:
                return shift_char(ch, -shift1, ALPH_UP)
            elif ch in ALPH_UP[13:]:
                return shift_char(ch, shift2 ** 2, ALPH_UP)
            return ch
        return ch

    decrypt_map = {}
    for ch in (ALPH_LO + ALPH_UP):
        decrypt_map[encrypt_char(ch)] = ch

    return "".join(decrypt_map.get(ch, ch) for ch in s)

def encrypt_file(src: Path, dst: Path, shift1: int, shift2: int) -> None:
    text = src.read_text(encoding="utf-8")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(encrypt_text(text, shift1, shift2), encoding="utf-8")

def decrypt_file(src: Path, dst: Path, shift1: int, shift2: int) -> None:
    text = src.read_text(encoding="utf-8")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(decrypt_text(text, shift1, shift2), encoding="utf-8")

def verify_files(original: Path, decrypted: Path) -> bool:
    return original.read_text(encoding="utf-8") == decrypted.read_text(encoding="utf-8")

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        shift1 = int(input("Enter shift1 (int): ").strip())
        shift2 = int(input("Enter shift2 (int): ").strip())
    except ValueError:
        print("Please enter integer values for shift1 and shift2.")
        return
    if not RAW.exists():
        print(f"Could not find {RAW}. Place raw_text.txt in the Q1_encryption folder.")
        return

    encrypt_file(RAW, ENC, shift1, shift2)
    decrypt_file(ENC, DEC, shift1, shift2)
    ok = verify_files(RAW, DEC)
    print("Verification:", "Successful ✅" if ok else "FAILED ❌")
    if ok:
        print(f"Wrote {ENC.name} and {DEC.name} to {OUT_DIR}")
    else:
        print("Decrypted text differs from the original. Re-check your logic.")

if __name__ == "__main__":
    main()
