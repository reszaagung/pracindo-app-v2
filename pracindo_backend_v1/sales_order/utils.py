def get_bulan_romawi(bulan):
    romawi = {
        1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI',
        7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'
    }
    return romawi.get(bulan, 'I')

def generate_nomor_so_dinamis(model_class, entitas, tanggal):
    kode_entitas = entitas.kode if entitas and hasattr(entitas, 'kode') else 'UMUM'
    tahun = tanggal.strftime('%Y')
    bulan_romawi = get_bulan_romawi(tanggal.month)
    
    prefix = f"SO/{kode_entitas}/{tahun}/{bulan_romawi}/"
    
    last_obj = model_class.objects.filter(
        nomor_so__startswith=prefix
    ).order_by('nomor_so').last()
    
    if last_obj and last_obj.nomor_so:
        try:
            last_number = int(last_obj.nomor_so.split('/')[-1])
            new_number = last_number + 1
        except (ValueError, IndexError):
            new_number = 1
    else:
        new_number = 1
        
    return f"{prefix}{new_number:03d}"