import traceback
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import GenerateStikerBesar, ItemCetak
from .serializers import GenerateStikerBesarInputSerializer, GenerateStikerBesarSerializer
from .services import petakan_template
from .chunking import algoritma_chunking  
from .tasks import task_generate_stiker

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
                hasil = algoritma_chunking(data["items"])

                for item_data, grup in zip(data["items"], hasil["grup_per_item"]):
                    ItemCetak.objects.create(generate=generate_obj, grup=grup, **item_data)

                template = petakan_template(generate_obj, jenis=data["jenis"], pola=hasil["pola"])
                if template is None:
                    raise ValueError(f"Template '{hasil['pola']}' gagal diproses. File tidak ditemukan.")

            return Response(GenerateStikerBesarSerializer(generate_obj).data, status=status.HTTP_201_CREATED)
            
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            # INI DIA DETEKTIFNYA: Menangkap error 500 dan memunculkannya ke Frontend
            error_msg = str(e)
            print(traceback.format_exc()) # Print full error ke terminal docker
            return Response({"detail": f"Backend Crash: {error_msg}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def cetak(self, request, pk=None):
        obj = get_object_or_404(GenerateStikerBesar, pk=pk)
        if obj.alamat_file is None:
            return Response({"detail": "Belum ada template terpasang."}, status=status.HTTP_400_BAD_REQUEST)

        task_generate_stiker.delay(obj.pk)
        return Response({"detail": "Perintah cetak dikirim ke antrean."}, status=status.HTTP_202_ACCEPTED)