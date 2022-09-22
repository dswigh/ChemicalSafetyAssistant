

class CompoundInfo:
    
    def __init__(self, name, mol_wt, cas_number, density, hazard_codes, 
                 hazard_code_descriptions, hazard_image_urls):
        self.name = name
        self.mol_wt = mol_wt
        self.cas_number = cas_number
        self.density = density 
        self.hazard_codes=hazard_codes
        self.hazard_code_descriptions = hazard_code_descriptions
        self.hazard_image_urls = hazard_image_urls


