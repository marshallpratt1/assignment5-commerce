from models import Listing, User


#simple test script, cannot get it to run
def run():
    
    user = User(username="bill", password="1")
    user.save()

    """title="Bike"
    price="100"
    description="A really nice bike"
    image=False
    category="Bicycles"
    listing = Listing()"""