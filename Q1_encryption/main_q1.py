from pathlib import Path
RAW = Path(__file__).parent/"raw_text.txt"; OUT_DIR = Path(__file__).parent/"outputs"
ENC = OUT_DIR/"encrypted_text.txt"; DEC = OUT_DIR/"decrypted_text.txt"
ALPH_LO="abcdefghijklmnopqrstuvwxyz"; ALPH_UP="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def shift_char(c,s,A): i=A.find(c); return c if i==-1 else A[(i+s)%len(A)]
def encrypt_text(t,a,b):
    o=[]; 
    for ch in t:
        if ch.islower(): o.append(shift_char(ch, a*b if ch in ALPH_LO[:13] else -(a+b), ALPH_LO))
        elif ch.isupper(): o.append(shift_char(ch, -a if ch in ALPH_UP[:13] else b**2, ALPH_UP))
        else: o.append(ch)
    return "".join(o)
def decrypt_text(t,a,b):
    def enc1(ch):
        if ch.islower(): return shift_char(ch, a*b if ch in ALPH_LO[:13] else -(a+b), ALPH_LO)
        if ch.isupper(): return shift_char(ch, -a if ch in ALPH_UP[:13] else b**2, ALPH_UP)
        return ch
    m={}; 
    for ch in (ALPH_LO+ALPH_UP): m[enc1(ch)]=ch
    return "".join(m.get(ch,ch) for ch in t)
def encrypt_file(src,dst,a,b): dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(encrypt_text(src.read_text(encoding="utf-8"),a,b),encoding="utf-8")
def decrypt_file(src,dst,a,b): dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(decrypt_text(src.read_text(encoding="utf-8"),a,b),encoding="utf-8")
def verify_files(p,q): return p.read_text(encoding="utf-8")==q.read_text(encoding="utf-8")
def main():
    OUT_DIR.mkdir(parents=True,exist_ok=True)
    try: a=int(input("Enter shift1 (int): ").strip()); b=int(input("Enter shift2 (int): ").strip())
    except: print("Please enter integer values for shift1 and shift2."); return
    if not RAW.exists(): print(f"Could not find {RAW}. Place raw_text.txt in the Q1_encryption folder."); return
    encrypt_file(RAW,ENC,a,b); decrypt_file(ENC,DEC,a,b)
    ok=verify_files(RAW,DEC); print("Verification:", "Successful ✅" if ok else "FAILED ❌")
if __name__=="__main__": main()
