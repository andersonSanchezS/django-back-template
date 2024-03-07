from apps.authentication.models import Users
from apps.request.models import Solcot
from apps.authentication.enums  import RoleEnum
from apps.request.enums         import ProcessStateEnum


def getBuyer(categoryId):
    # Get a buyer with the category and the role of buyer 
    # also get the first with the lowest amount of solcot

    # Get all buyers with the category and the role of buyer
    buyers = Users.objects.filter(categories=categoryId, roles=RoleEnum.COMPRADOR.value)

    minSolcotsCount = None
    minBuyerId      = None

    # Iterate over the buyers
    for buyer in buyers:
        # Get the amount of solcots of the buyer
        solcotsCount = Solcot.objects.filter(buyer=buyer.id, state=1, process_state__in=[ProcessStateEnum.PENDING.value,ProcessStateEnum.IN_PROCESS.value]).count()
        # If the minSolcotsCount is None or the solcotsCount is less than the minSolcotsCount
        if minSolcotsCount is None or solcotsCount < minSolcotsCount:
            # Set the minSolcotsCount to the solcotsCount
            minSolcotsCount = solcotsCount
            # Set the minBuyerId to the buyer id
            minBuyerId = buyer.id

    # Return the buyer with the minBuyerId
    return Users.objects.get(id=minBuyerId) if minBuyerId else None

