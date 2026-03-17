from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from rest_framework.filters import OrderingFilter
from core.utils import api_response
from finance.models import BankAccount, TransactionCategory, Transaction, SelfTransfer
from api.finance.serializers import BankAccountSerializer, TransactionCategorySerializer, TransactionSerializer, SelfTransferSerializer
from api.finance.filters import BankAccountFilter, TransactionCategoryFilter, TransactionFilter, SelfTransferFilter


# --------------------------------------------------
# BANK ACCOUNT LIST & CREATE
# --------------------------------------------------
class BankAccountListView(generics.ListCreateAPIView):
    queryset = BankAccount.active_objects.all()
    serializer_class = BankAccountSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BankAccountFilter
    ordering_fields = ["name", "balance", "date_added"]
    ordering = ["-auto_id"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data

        stats = {
            "total": BankAccount.active_objects.count(),
        }

        return api_response(
            message="Bank accounts retrieved successfully",
            data={"accounts": data, "stats": stats},
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Bank account created successfully",
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return api_response(
                message="Failed to create bank account",
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )


# --------------------------------------------------
# BANK ACCOUNT RETRIEVE, UPDATE & DELETE
# --------------------------------------------------
class BankAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankAccount.active_objects.all()
    serializer_class = BankAccountSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        return api_response(
            message="Bank account retrieved successfully",
            data=self.get_serializer(self.get_object()).data,
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=kwargs.get("partial", False)
        )
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Bank account updated successfully",
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return api_response(
                message="Failed to update bank account",
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return api_response(
            message="Bank account deleted successfully",
            status=status.HTTP_204_NO_CONTENT
        )


# --------------------------------------------------
# TRANSACTION CATEGORY LIST & CREATE
# --------------------------------------------------
class TransactionCategoryListView(generics.ListCreateAPIView):
    queryset = TransactionCategory.active_objects.all()
    serializer_class = TransactionCategorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TransactionCategoryFilter
    ordering_fields = ["name", "date_added"]
    ordering = ["-auto_id"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data

        stats = {
            "total": TransactionCategory.active_objects.count(),
        }

        return api_response(
            message="Transaction categories retrieved successfully",
            data={"categories": data, "stats": stats},
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Transaction category created successfully",
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return api_response(
                message="Failed to create transaction category",
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )


# --------------------------------------------------
# TRANSACTION CATEGORY RETRIEVE, UPDATE & DELETE
# --------------------------------------------------
class TransactionCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransactionCategory.active_objects.all()
    serializer_class = TransactionCategorySerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        return api_response(
            message="Transaction category retrieved successfully",
            data=self.get_serializer(self.get_object()).data,
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=kwargs.get("partial", False)
        )
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Transaction category updated successfully",
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return api_response(
                message="Failed to update transaction category",
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return api_response(
            message="Transaction category deleted successfully",
            status=status.HTTP_204_NO_CONTENT
        )


# --------------------------------------------------
# TRANSACTION LIST & CREATE
# --------------------------------------------------
class TransactionListView(generics.ListCreateAPIView):
    queryset = Transaction.active_objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = ["title", "amount", "date", "date_added"]
    ordering = ["-auto_id"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data

        stats = {
            "total": Transaction.active_objects.count(),
            "total_income": Transaction.active_objects.filter(type="income").aggregate(total=Sum("amount"))["total"]  or 0,
            "total_expense": Transaction.active_objects.filter(type="expense").aggregate(total=Sum("amount"))["total"] or 0,
        }

        return api_response(
            message="Transactions retrieved successfully",
            data={"transactions": data, "stats": stats},
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Transaction created successfully",
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return api_response(
                message="Failed to create transaction",
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )


# --------------------------------------------------
# TRANSACTION RETRIEVE, UPDATE & DELETE
# --------------------------------------------------
class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.active_objects.all()
    serializer_class = TransactionSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        return api_response(
            message="Transaction retrieved successfully",
            data=self.get_serializer(self.get_object()).data,
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=kwargs.get("partial", False)
        )
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Transaction updated successfully",
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return api_response(
                message="Failed to update transaction",
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return api_response(
            message="Transaction deleted successfully",
            status=status.HTTP_204_NO_CONTENT
        )
    

# --------------------------------------------------
# SELF TRANSFER LIST & CREATE
# --------------------------------------------------
class SelfTransferListView(generics.ListCreateAPIView):
    queryset = SelfTransfer.active_objects.all()
    serializer_class = SelfTransferSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SelfTransferFilter
    ordering_fields = ["amount", "date", "date_added"]
    ordering = ["-auto_id"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data

        stats = {
            "total": SelfTransfer.active_objects.count(),
        }

        return api_response(
            message="Self transfers retrieved successfully",
            data={"transfers": data, "stats": stats},
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Self transfer created successfully",
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return api_response(
                message="Failed to create self transfer",
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )


# --------------------------------------------------
# SELF TRANSFER RETRIEVE, UPDATE & DELETE
# --------------------------------------------------
class SelfTransferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SelfTransfer.active_objects.all()
    serializer_class = SelfTransferSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        return api_response(
            message="Self transfer retrieved successfully",
            data=self.get_serializer(self.get_object()).data,
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=kwargs.get("partial", False)
        )
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Self transfer updated successfully",
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return api_response(
                message="Failed to update self transfer",
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return api_response(
            message="Self transfer deleted successfully",
            status=status.HTTP_204_NO_CONTENT
        )