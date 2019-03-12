
def get_colonization_rate(traits):
    colonization_score = traits[colonization_index]
    resistance_score   = traits[resistance_index]
    mutation_score     = traits[mutation_index]
    
    return base_colonization_rate + \
            bonus_colonization_rate*colonization_score + \
            mutation_colonization_rate*mutation_score + \
            resistance_colonization_rate*resistance_score

def get_mutation_magnitude(traits):
    mutation_score = traits[mutation_index]
    return base_mutation_magnitude + bonus_mutation_magnitude*mutation_score

def get_mutation_rate(traits):
    mutation_score = traits[mutation_index]
    return base_mutation_rate + bonus_mutation_rate*mutation_score

def get_resistance_rate(traits,drug):
    exp = 30
    rs = traits[resistance_index]
    return np.power(10**exp,rs)/(np.power(10**exp,rs) + np.power(10**exp,drug-0.15))
    
