class Species:
    """Helper class to handle different pecies of boids"""

    total_boids = 0
    species_list = []
    max_species_ids = []

    def __init__(self, num_boids, color, **kwargs):
        self.ids = range(self.total_boids, self.total_boids + num_boids)
        Species.total_boids += num_boids
        Species.max_species_ids.append(self.total_boids)
        Species.species_list.append(self)

        self.color = color
        self.characteritics = kwargs

    @classmethod
    def get_species(cls, boid_id):
        for species in cls.species_list:
            if boid_id in species.ids:
                return species
        raise IndexError(
            "An error was found while trying to assign species to current boid"
        )
