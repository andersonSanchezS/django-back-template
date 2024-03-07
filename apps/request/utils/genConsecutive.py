from apps.request.models import Solcot


def genConsecutive():
    """
    Generate the consecutive for the solcot
    """
    # Get the last solcot
    lastSolcot = Solcot.objects.all().order_by('-created_at').first()
    # Check if the last solcot exists
    if lastSolcot:
        # Get the last consecutive
        lastConsecutive = lastSolcot.consecutive
        # Split the consecutive
        splitConsecutive = lastConsecutive.split("-")
        # Get the last number
        lastNumber = int(splitConsecutive[1])
        # Increment the last number
        lastNumber += 1
        # Create the new consecutive
        newConsecutive = f"SOLCOT-{lastNumber}"
        return newConsecutive
    else:
        return "SOLCOT-1"