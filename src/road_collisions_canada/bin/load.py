from road_collisions_base import logger

from road_collisions_canada.models.collision import Collisions


def main():
    print('NOTE: Since Canada data is so large, only loading data from 2017')
    collisions = Collisions.load_all(region='canada', year=2017)

    logger.info('Loaded %s collisions', (len(collisions)))
    logger.info('Do something with the data in the variable \'collisions\'...')

    import pdb; pdb.set_trace()

    pass


if __name__ == '__main__':
    main()
