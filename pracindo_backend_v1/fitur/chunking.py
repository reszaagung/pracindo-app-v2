# fitur/chunking.py

def algoritma_chunking(items):
    """
    Menentukan pola stiker dan pemetaan grup huruf (A, B, C, D) 
    berdasarkan jumlah item yang dikirim dalam satu batch.
    """
    jumlah = len(items)
    
    if jumlah == 1:
        # Jika hanya ada 1 item, cetak berulang di ke-4 slot
        return {"pola": "AAAA", "grup_per_item": ["A"]}
        
    elif jumlah == 2:
        # Jika ada 2 item, bagi rata (Slot 1 & 2 untuk A, Slot 3 & 4 untuk B)
        return {"pola": "AABB", "grup_per_item": ["A", "B"]}
        
    elif jumlah == 3:
        # Jika ada 3 item, A menempati Slot 1 & 2, sisanya B dan C
        return {"pola": "AABC", "grup_per_item": ["A", "B", "C"]}
        
    elif jumlah >= 4:
        # Jika ada 4 item, masing-masing menempati 1 slot
        return {"pola": "ABCD", "grup_per_item": ["A", "B", "C", "D"]}
        
    # Fallback default
    return {"pola": "AAAA", "grup_per_item": ["A"]}