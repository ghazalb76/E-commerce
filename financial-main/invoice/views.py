from rest_framework.viewsets import ReadOnlyModelViewSet

from invoice.models import Invoice, InvoiceItem
from invoice.serializers import InvoiceSerializer, InvoiceItemSerializer


class InvoiceViewset(ReadOnlyModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        user_id = self.request.data.get('user_id')
        return Invoice.objects.filter(account_id__user_id=user_id)
