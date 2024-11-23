import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):

    prob = 1

    for key,value in people.items():

        if value["mother"] == None and value["father"] == None:

            temp_prob = 1
            temp_prob2 = 1

            if key in one_gene:
                temp_prob *= PROBS["gene"][1]
                num_gens = 1
            elif key in two_genes:
                temp_prob *= PROBS["gene"][2] 
                num_gens = 2
            else:
                temp_prob *= PROBS["gene"][0]   
                num_gens = 0

            if key in have_trait:
                temp_prob2 *= PROBS["trait"][num_gens][True]
            else:
                temp_prob2 *= PROBS["trait"][num_gens][False]

            prob = prob * temp_prob * temp_prob2   

        else:

            if value["mother"] in one_gene:
                number_genes_mother = 1
            elif value["mother"] in two_genes:
                number_genes_mother = 2
            else:
                number_genes_mother = 0

            if value["father"] in one_gene:
                number_genes_father = 1
            elif value["father"] in two_genes:
                number_genes_father = 2
            else:
                number_genes_father = 0  

            if key in one_gene:
  
                #case gets the gene from his mother and not his father   
                if number_genes_mother == 0:
                    temp_prob3 = PROBS["mutation"]   
                elif number_genes_mother == 2:
                    temp_prob3 = 1 - PROBS["mutation"]
                elif number_genes_mother == 1:
                    temp_prob3 = 0.5 

                if number_genes_father == 0:
                    temp_prob4 = 1 - PROBS["mutation"]   
                elif number_genes_father == 2:
                    temp_prob4 = PROBS["mutation"]
                elif number_genes_father == 1:
                    temp_prob4 = 0.5 

                #case gets the gene from his father and not his mother                                                       

                if number_genes_father == 0:
                    temp_prob5 = PROBS["mutation"]   
                elif number_genes_father == 2:
                    temp_prob5 = 1 - PROBS["mutation"]
                elif number_genes_father == 1:
                    temp_prob5 = 0.5    

                if number_genes_mother == 0:
                    temp_prob6 = 1 - PROBS["mutation"]   
                elif number_genes_mother == 2:
                    temp_prob6 = PROBS["mutation"]
                elif number_genes_mother == 1:
                    temp_prob6 = 0.5 

                prob_one_gene = (temp_prob3 * temp_prob4) + (temp_prob5*temp_prob6)


                if key in have_trait:

                    temp_prob_trait = PROBS["trait"][1][True]    

                else:

                    temp_prob_trait = PROBS["trait"][1][False]  

                prob *= prob_one_gene * temp_prob_trait


            elif key not in one_gene and key not in two_genes:  

                #case not gets the gene from  his father
                if number_genes_father == 0:
                    temp_prob7 = 1 - PROBS["mutation"]   
                elif number_genes_father == 2:
                    temp_prob7 = PROBS["mutation"]
                elif number_genes_father == 1:
                    temp_prob7 = 0.5   

                #case not gets the gene from  his mother    
                if number_genes_mother == 0:
                    temp_prob8 = 1 - PROBS["mutation"]   
                elif number_genes_mother == 2:
                    temp_prob8 = PROBS["mutation"]
                elif number_genes_mother == 1:
                    temp_prob8 = 0.5    

                if key in have_trait:

                    temp_prob_trait = PROBS["trait"][0][True]    

                else:

                    temp_prob_trait = PROBS["trait"][0][False]  

                prob *= temp_prob7 * temp_prob8 * temp_prob_trait   


            if key in two_genes: 

                #case gets the gene from his mother    
                if number_genes_mother == 0:
                    temp_prob9 = PROBS["mutation"]   
                elif number_genes_mother == 2:
                    temp_prob9 = 1 - PROBS["mutation"]
                elif number_genes_mother == 1:
                    temp_prob9 = 0.5 

                #case gets the gene from his father                                                        

                if number_genes_father == 0:
                    temp_prob10 = PROBS["mutation"]   
                elif number_genes_father == 2:
                    temp_prob10 = 1 - PROBS["mutation"]
                elif number_genes_father == 1:
                    temp_prob10 = 0.5 

                if key in have_trait:

                    temp_prob_trait = PROBS["trait"][2][True]    

                else:

                    temp_prob_trait = PROBS["trait"][2][False]  

                prob *= temp_prob9 * temp_prob10 * temp_prob_trait                                                                        


    return prob 




def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:

        if person in one_gene:
            probabilities[person]["gene"][1] += p

        elif person in two_genes:
            probabilities[person]["gene"][2] += p  

        elif person not in one_gene and person not in two_genes:
            probabilities[person]["gene"][0] += p              

        if person in have_trait: 
            probabilities[person]["trait"][True] += p   

        elif person not in have_trait: 
            probabilities[person]["trait"][False] += p                  


               

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
