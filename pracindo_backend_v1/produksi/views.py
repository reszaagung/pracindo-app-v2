from decimal import Decimal
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from .models import Tangki, Batch, TipeProses
from .serializers import TangkiSerializer, BatchSerializer
from .services import (
    simpan_dan_posting_mixing,
    simpan_dan_posting_blending,
    pratinjau_mixing,
    pratinjau_blending,
    hapus_batch_dan_kembalikan_stok,
    GalatProduksi,
    KonflikBatch,
    _nomor_batch
)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def pratinjau_batch(request):
    jenis = request.data.get("jenis", request.query_params.get("jenis", TipeProses.MIXING)).upper()
    susut_kg = request.data.get("tekor_kg", request.query_params.get("tekor_kg", 0))
    
    if jenis == TipeProses.MIXING:
        baris = request.data.get("materials", [])
        res = pratinjau_mixing(baris=baris, susut_kg=susut_kg)
    elif jenis == TipeProses.BLENDING:
        baris_sumber = request.data.get("wip_sources", [])
        res = pratinjau_blending(baris_sumber=baris_sumber, susut_kg=susut_kg)
    else:
        return Response({"error": f"Jenis proses '{jenis}' tidak dikenal."}, status=status.HTTP_400_BAD_REQUEST)
        
    status_code = status.HTTP_200_OK if res.get("valid") else status.HTTP_422_UNPROCESSABLE_ENTITY
    return Response(res, status=status_code)


class TangkiViewSet(viewsets.ModelViewSet):
    queryset = Tangki.objects.all().order_by("kode")
    serializer_class = TangkiSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    @action(detail=False, methods=["get"])
    def rekap(self, request):
        from .services import saldo_batch 
        
        qs = self.get_queryset()
        data = []
        for t in qs:
            vol = sum((saldo_batch(b).sisa_qty for b in t.batch_set.filter(status="POSTED")), Decimal("0"))
            
            data.append({
                "id": t.id,
                "kode": t.kode,
                "nama": t.nama,
                "kapasitas": str(t.kapasitas_kg) if t.kapasitas_kg else "0",
                "terisi": str(vol),
                "persen": round((float(vol) / float(t.kapasitas_kg)) * 100, 1) if t.kapasitas_kg and t.kapasitas_kg > 0 else 0
            })
        return Response(data)

    @action(detail=True, methods=["get"])
    def saldo(self, request, pk=None):
        tangki = self.get_object()

        saldo_kg = Decimal(str(tangki.saldo_kg or 0))
        saldo_nilai = Decimal(str(tangki.saldo_nilai or 0))

        if saldo_kg > 0:
            harga_per_kg = (
                saldo_nilai / saldo_kg
            ).quantize(Decimal("0.01"))
        else:
            harga_per_kg = Decimal("0.00")

        return Response({
            "id": tangki.id,
            "kode": tangki.kode,
            "nama": str(tangki),
            "saldo_kg": saldo_kg,
            "saldo_nilai": saldo_nilai,
            "sisa_qty": saldo_kg,
            "sisa_nilai": saldo_nilai,
            "harga_per_kg": harga_per_kg,
        })

class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.select_related("tangki", "dibuat_oleh").order_by("-id")
    serializer_class = BatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        jenis = self.request.query_params.get("jenis")
        if jenis:
            qs = qs.filter(jenis=jenis)
        return qs
        
    @action(detail=False, methods=["get"], url_path="nomor-baru")
    def nomor_baru(self, request):
        jenis = request.query_params.get("jenis", TipeProses.MIXING).upper()
        nomor = _nomor_batch(jenis, timezone.localdate())
        return Response({"nomor": nomor})

    def create(self, request, *args, **kwargs):
        try:
            jenis = request.data.get("jenis", TipeProses.MIXING).upper()
            params = {
                "nama_hasil": request.data.get("nama_hasil"),
                "tangki_id": request.data.get("tangki_tujuan"),
                "susut_kg": request.data.get("tekor_kg"),
                "tanggal": timezone.localdate(),
                "user": request.user,
                "nomor_custom": request.data.get("batch") 
            }
            
            if jenis == TipeProses.MIXING:
                params["baris"] = request.data.get("materials", [])
                batch = simpan_dan_posting_mixing(**params)
            else:
                params["baris_sumber"] = request.data.get("wip_sources", [])
                batch = simpan_dan_posting_blending(**params)
                
            return Response(BatchSerializer(batch).data, status=status.HTTP_201_CREATED)
        except (GalatProduksi, KonflikBatch) as e:
            return Response({"detail": str(e)}, status=getattr(e, "http", status.HTTP_400_BAD_REQUEST))
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def hapus_dengan_kembali_stok(self, request, pk=None):
        try:
            hasil = hapus_batch_dan_kembalikan_stok(pk, request.user)
            return Response(hasil, status=200)
        except Exception as e:
            return Response({"pesan": str(e)}, status=400)