import traceback
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import GenerateStikerBesar, ItemCetak, GenerateStikerKecil12, ItemCetakKecil12, StikerKecil12
from .serializers import (
    GenerateStikerBesarInputSerializer, GenerateStikerBesarSerializer,
    GenerateStikerKecil12InputSerializer, GenerateStikerKecil12Serializer,
)
from .services import petakan_template
from .chunking import algoritma_chunking, encode_pola, decode_pola
from .printing import generate_docx_saja


class GenerateStikerBesarViewSet(viewsets.ViewSet):
    def list(self, request):
        qs = GenerateStikerBesar.objects.all()
        return Response(GenerateStikerBesarSerializer(qs, many=True).data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(GenerateStikerBesar, pk=pk)
        return Response(GenerateStikerBesarSerializer(obj).data)

    def create(self, request):
        input_serializer = GenerateStikerBesarInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        try:
            with transaction.atomic():
                generate_obj = GenerateStikerBesar.objects.create(total_unit=len(data["items"]))

                pola_pilihan = data.get("pola")
                hasil = algoritma_chunking(data["items"], pola_pilihan)

                for item_data, grup in zip(data["items"], hasil["grup_per_item"]):
                    ItemCetak.objects.create(generate=generate_obj, grup=grup, **item_data)

                template = petakan_template(generate_obj, jenis=data["jenis"], pola=hasil["pola"])
                if template is None:
                    raise ValueError(f"Template jenis '{data['jenis']}' pola '{hasil['pola']}' tidak ditemukan.")

                generate_docx_saja(generate_obj)

            file_path = generate_obj.file_hasil
            if not file_path:
                raise ValueError("Dokumen gagal dibuat oleh sistem.")

            nama_file = f"Stiker_{data['jenis'].replace(' ', '_')}_{hasil['pola']}.docx"
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=nama_file)

        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(traceback.format_exc())
            return Response({"detail": f"Gagal Generate: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def cetak(self, request, pk=None):
        obj = get_object_or_404(GenerateStikerBesar, pk=pk)
        if obj.alamat_file is None:
            return Response({"detail": "Belum ada template terpasang."}, status=status.HTTP_400_BAD_REQUEST)

        generate_docx_saja(obj)
        return FileResponse(open(obj.file_hasil, 'rb'), as_attachment=True, filename="Stiker_CetakUlang.docx")


class TemplateStikerKecil12ViewSet(viewsets.ViewSet):
    """Read-only — daftar pola yang terdaftar di Master Data untuk satu
    jenis. Sumber dropdown pola di frontend; nambah template baru lewat
    Admin otomatis muncul di sini tanpa deploy ulang."""

    def list(self, request):
        jenis = request.query_params.get("jenis")
        if not jenis:
            return Response({"detail": "Parameter 'jenis' wajib diisi."}, status=status.HTTP_400_BAD_REQUEST)

        prefix = f"stiker_{jenis}_"
        qs = StikerKecil12.objects.filter(aktif=True, nama_file__startswith=prefix)

        hasil = [
            {
                "id": t.id,
                "kode": t.nama_file.removeprefix(prefix).removesuffix(".docx"),
                "pola": decode_pola(t.nama_file.removeprefix(prefix).removesuffix(".docx")),
            }
            for t in qs
        ]
        return Response(hasil)


def petakan_template_kecil12(generate_obj, jenis, pola):
    nama_file = f"stiker_{jenis}_{encode_pola(pola)}.docx"
    try:
        template = StikerKecil12.objects.get(nama_file=nama_file, aktif=True)
    except StikerKecil12.DoesNotExist:
        return None
    generate_obj.alamat_file = template
    generate_obj.pola_terdeteksi = pola
    generate_obj.save()
    return template


class GenerateStikerKecil12ViewSet(viewsets.ViewSet):
    def list(self, request):
        qs = GenerateStikerKecil12.objects.all()
        return Response(GenerateStikerKecil12Serializer(qs, many=True).data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(GenerateStikerKecil12, pk=pk)
        return Response(GenerateStikerKecil12Serializer(obj).data)

    def create(self, request):
        input_serializer = GenerateStikerKecil12InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        try:
            with transaction.atomic():
                generate_obj = GenerateStikerKecil12.objects.create(total_unit=len(data["items"]))
                hasil = algoritma_chunking(data["items"], data["pola"])

                for item_data, grup in zip(data["items"], hasil["grup_per_item"]):
                    ItemCetakKecil12.objects.create(generate=generate_obj, grup=grup, **item_data)

                template = petakan_template_kecil12(generate_obj, jenis=data["jenis"], pola=hasil["pola"])
                if template is None:
                    raise ValueError(f"Template jenis '{data['jenis']}' pola '{hasil['pola']}' tidak ditemukan.")

                generate_docx_saja(generate_obj, jumlah_slot=12)

            file_path = generate_obj.file_hasil
            if not file_path:
                raise ValueError("Dokumen gagal dibuat oleh sistem.")

            nama_file = f"StikerKecil12_{data['jenis']}_{hasil['pola']}.docx"
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=nama_file)

        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(traceback.format_exc())
            return Response({"detail": f"Gagal Generate: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)