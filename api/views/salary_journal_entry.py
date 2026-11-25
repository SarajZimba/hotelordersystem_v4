from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from accounting.models import AccountLedger, AccountSubLedger
from organization.models import Organization
from user.permission import IsAdminMixin

# class LiquidAssetLedgersForPaymentAPIView(IsAdminMixin, APIView):
#     """
#     Simplified API endpoint specifically for payment source selection
#     Returns only essential fields
#     """
    
#     def get(self, request):
#         try:
#             show_zero = request.GET.get('show_zero_ledgers', 'false').lower() == 'true'
            
#             # Get Liquid Asset ledgers
#             liquid_asset_ledgers = AccountLedger.objects.filter(
#                 account_chart__group='Liquid Asset'
#             ).order_by('ledger_name')
            
#             liquid_assets = []
            
#             for ledger in liquid_asset_ledgers:
#                 if not show_zero and ledger.total_value == 0:
#                     continue
                
#                 # Get subledgers
#                 subledgers = AccountSubLedger.objects.filter(ledger_id=ledger.id)
#                 if not show_zero:
#                     subledgers = subledgers.filter(total_value__gt=0.0)
                
#                 subledger_data = [
#                     {
#                         'id': sub.id,
#                         'name': sub.sub_ledger_name,
#                         'total_value': float(sub.total_value)
#                     }
#                     for sub in subledgers
#                 ]
                
#                 liquid_assets.append({
#                     'id': ledger.id,
#                     'name': ledger.ledger_name,
#                     'total_value': float(ledger.total_value),
#                     'subledgers': subledger_data,
#                     'subledger_count': len(subledger_data)
#                 })
            
#             total_balance = sum(asset['total_value'] for asset in liquid_assets)
            
#             return Response({
#                 'success': True,
#                 'data': liquid_assets,
#                 'summary': {
#                     'total': float(total_balance),
#                     'count': len(liquid_assets)
#                 }
#             })
            
#         except Exception as e:
#             return Response({
#                 'success': False,
#                 'error': str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from accounting.models import AccountLedger, AccountSubLedger
from organization.models import Organization

class LiquidAssetLedgersForPaymentAPIView(APIView):
    """
    API endpoint for Liquid Asset ledgers with subledgers
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            branch_id = request.GET.get('branchID')
            if not branch_id:
                return Response(
                    {'success': False, 'error': 'branchID is required.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            show_zero = request.GET.get('show_zero_ledgers', 'false').lower() == 'true'

            org = Organization.objects.first()
            if org:
                show_zero = show_zero or org.show_zero_ledgers

            liquid_asset_ledgers = AccountLedger.objects.filter(
                account_chart__group='Liquid Asset',
                branch_id=branch_id,
            ).order_by('ledger_name')

            liquid_assets = []

            for ledger in liquid_asset_ledgers:
                # if not show_zero and ledger.total_value == 0:
                #     continue

                subledgers = AccountSubLedger.objects.filter(ledger_id=ledger.id)
                # if not show_zero:
                #     subledgers = subledgers.filter(total_value__gt=0.0)

                subledger_data = [
                    {
                        'id': sub.id,
                        'name': sub.sub_ledger_name,
                        'total_value': float(sub.total_value)
                    }
                    for sub in subledgers
                ]

                liquid_assets.append({
                    'id': ledger.id,
                    'name': ledger.ledger_name,
                    'total_value': float(ledger.total_value),
                    'subledgers': subledger_data,
                    'subledger_count': len(subledger_data)
                })

            total_balance = sum(asset['total_value'] for asset in liquid_assets)

            return Response({
                'success': True,
                'data': liquid_assets,
                'summary': {
                    'total': float(total_balance),
                    'count': len(liquid_assets)
                }
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)