# Make a class that will allow you to create certain inputs based on user needs

class ShoeInput:
    def __init__(self):
        self.user_input = {}
        self.choice = None
        self.brand = None
        self.price = None
        "self.size = None"

    def input_type(self):
        while True:
            self.choice = int(input("How do you want to query?\n1:brand\n2.price\nAnswer: "))
            if self.choice == 1:
                self.brand_check()
                break
                
            elif self.choice == 2:
                print("You selected price")
                self.price_check()
                break
            else:
                print("Invalid input, please try again.\n")
                continue    
            
    def brand_check(self):
        self.user_input['brand'] = input("What brand do you want to search for?\nAnswer:").strip()
        """
        self.user_input['size'] = float(input("What size are you looking for?\nAnswer:"))
        """
        self.get_search_params()
        
    def price_check(self):
        self.user_input['price'] = float(input("What is your current budget?\nAnswer:$"))
        """
        self.user_input['size'] = float(input("What size are you looking for?\nAnswer:"))
        """
        self.get_search_params()
    
    def get_search_params(self):
        """Return the search parameters dictionary"""
        print(self.user_input)
        return self.user_input




def main():
    shoe_input = ShoeInput()
    shoe_input.input_type()




if __name__ == "__main__":
    main()
















