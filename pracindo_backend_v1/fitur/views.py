import traceback
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import GenerateStikerBesar, ItemCetak
from .serializers import GenerateStikerBesarInputSerializer, GenerateStikerBesarSerializer
from .services import petakan_template
from .chunking import algoritma_chunking  
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