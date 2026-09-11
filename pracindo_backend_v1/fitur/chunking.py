def algoritma_chunking(items, pola_pilihan=None):
    jumlah = len(items)
    
    if pola_pilihan:
        if pola_pilihan == "AAAA":
            return {"pola": "AAAA", "grup_per_item": ["A"]}
        elif pola_pilihan in ["AABB", "AAAB"]:
            return {"pola": pola_pilihan, "grup_per_item": ["A", "B"]}
        elif pola_pilihan == "AABC":
            return {"pola": "AABC", "grup_per_item": ["A", "B", "C"]}
        elif pola_pilihan == "ABCD":
            return {"pola": "ABCD", "grup_per_item": ["A", "B", "C", "D"]}

    if jumlah == 1:
        return {"pola": "AAAA", "grup_per_item": ["A"]}
    elif jumlah == 2:
        return {"pola": "AABB", "grup_per_item": ["A", "B"]}
    elif jumlah == 3:
        return {"pola": "AABC", "grup_per_item": ["A", "B", "C"]}
    elif jumlah >= 4:
        return {"pola": "ABCD", "grup_per_item": ["A", "B", "C", "D"]}
        
    return {"pola": "AAAA", "grup_per_item": ["A"]}