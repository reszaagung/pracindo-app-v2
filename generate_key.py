import rsa
import os

# Generate kunci baru 1024 bit
pub, priv = rsa.newkeys(1024)

# Format untuk Frontend (satu baris dengan \n)
pub_env = pub.save_pkcs1().decode().replace('\n', '\\n')

# Format untuk Backend (multiline asli atau pakai \n)
priv_env = priv.save_pkcs1().decode().replace('\n', '\\n')

print("\n" + "="*50)
print("SALIN TEKS DI BAWAH INI KE FILE .env MASING-MASING:")
print("="*50 + "\n")

print("--- 1. UNTUK .ENV BACKEND (DJANGO) ---")
print(f'RSA_PRIVATE_KEY="{priv_env}"\n')

print("--- 2. UNTUK .ENV FRONTEND (VUE - STAFF & RETAIL) ---")
print(f'VITE_RSA_PUBLIC_KEY="{pub_env}"\n')
print("="*50)