import os
from model import Base, engine, CannedScenario, SessionMaker, CannedResult


def init_canned_scenarios_db(first_time):
    """
    Initialize the persistent store
    """

    # Create tables
    Base.metadata.create_all(engine)

    # Initialize database
    session = SessionMaker()

    if first_time:
        # Get path param file
        project_dir = os.path.dirname(os.path.abspath(__file__))
        param_file = os.path.join(project_dir, 'data', 'inputs.txt')

        # Open initial param file
        with open(param_file, 'r') as f:
            for index, line in enumerate(f):
                line = line.strip().split(',')

                canned_scenario = CannedScenario(index,
                                                 float(line[0].strip()),
                                                 float(line[1].strip()),
                                                 float(line[2].strip()),
                                                 float(line[3].strip()),
                                                 float(line[4].strip()),
                                                 float(line[5].strip()),
                                                 float(line[6].strip())
                                                 )

                session.add(canned_scenario)

        # Read each result file into db
        hydrograph_dir = os.path.join(project_dir, 'data', 'hydrograph')

        hydrographs = os.listdir(hydrograph_dir)

        for hydrograph in hydrographs:
            if '__init__' not in hydrograph:
                hydrograph_path = os.path.join(hydrograph_dir, hydrograph)
                scenario_id = int(hydrograph.split('.')[0].replace('base', ''))

                with open(hydrograph_path, 'r') as h:
                    canned_result = CannedResult(scenario_id, h.read())

                    session.add(canned_result)

        # Commit
        session.commit()