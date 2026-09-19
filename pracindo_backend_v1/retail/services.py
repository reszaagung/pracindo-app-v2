from django.db import transaction
from django.utils import timezone
from .models import PenerimaanBarang, ItemPenerimaan

@transaction.atomic
def buat_penerimaan_dari_do(distribusi):
    """
    Jembatan dari Warehouse ke Retail.
    """
    # 1. Pastikan DO ini ditujukan ke cabang
    if distribusi.jenis_tujuan != 'CABANG' or not distribusi.tujuan_cabang_id:
        return None
        
    # 2. Buat nomor struk penerimaan otomatis
    nomor_rcv = f"RCV/{distribusi.nomor.split('/')[-1]}/{timezone.now().strftime('%H%M%S')}"
    
    penerimaan, created = PenerimaanBarang.objects.get_or_create(
        referensi_logistik=distribusi.nomor,
        defaults={
            'nomor_penerimaan': nomor_rcv,
            'cabang_id': distribusi.tujuan_cabang_id,
            'status': 'DIKIRIM',
            'tanggal_kirim': timezone.now()
        }
    )
    
    if created:
        for item in distribusi.item.all():
            ItemPenerimaan.objects.create(
                penerimaan=penerimaan,
                produk_id=item.produk_id,
                kemasan=item.kemasan,  
                unit_dikirim=item.qty,
                unit_diterima=0
            )
            
    return penerimaan