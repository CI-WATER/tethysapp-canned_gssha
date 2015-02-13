# Put your persistent store models in this file
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from lib.scenario_selector import ScenarioSelector
from utilities import get_persistent_store_engine, decimal_year_to_datetime

# DB Engine, sessionmaker, and base
engine = get_persistent_store_engine('canned_scenarios_db')
SessionMaker = sessionmaker(bind=engine)
Base = declarative_base()

# Data model definition


class CannedScenario(Base):
    """
    SQLAlchemy data model for canned scenario params
    """

    __tablename__ = 'canned_scenarios'

    # Columns
    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer)
    param1 = Column(Float)
    param2 = Column(Float)
    param3 = Column(Float)
    param4 = Column(Float)
    param5 = Column(Float)
    param6 = Column(Float)
    param7 = Column(Float)

    def __init__(self, scenario_id, param1, param2, param3, param4, param5, param6, param7):
        """
        Constructor for canned scenario
        """
        self.scenario_id = scenario_id
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.param4 = param4
        self.param5 = param5
        self.param6 = param6
        self.param7 = param7

    def as_list(self, normalized=False):
        """
        Return parameters as list
        """

        param_list = [self.param1, self.param2, self.param3, self.param4, self.param5, self.param6, self.param7]

        if not normalized:
            return param_list
        else:
            return CannedScenario.normalize_params(param_list)


    @classmethod
    def get_min_max(cls):
        """
        Get the min and max
        """
        # Make a session
        session = SessionMaker()

        # Get min and max for each param
        mins = session.query(func.min(cls.param1), func.min(cls.param2), func.min(cls.param3), func.min(cls.param4),
                             func.min(cls.param5), func.min(cls.param6), func.min(cls.param7)).all()
        maxes = session.query(func.max(cls.param1), func.max(cls.param2), func.max(cls.param3), func.max(cls.param4),
                              func.max(cls.param5), func.max(cls.param6), func.max(cls.param7)).all()

        # Stitch together as list of lists
        stitched = zip(mins[0], maxes[0])

        return stitched

    @classmethod
    def get_scenario_params(cls):
        """
        Get the scenario list of lists
        """
        # Make a session
        session = SessionMaker()

        # Query db
        scenario_params = session.query(cls.param1, cls.param2,  cls.param3, cls.param4,
                                        cls.param5, cls.param6, cls.param7).\
                                  order_by(cls.scenario_id).\
                                  all()

        return scenario_params

    @classmethod
    def normalize_params(cls, param_list):
        """
        Normalize parameter list. Parameters must be in same order as listed in db.
        """

        # Get mins and maxes
        min_max = cls.get_min_max()

        normalized_param_list = []

        # Calculate the normalized values
        for param, pmin_pmax in zip(param_list, min_max):
            z = (param - pmin_pmax[0]) / (pmin_pmax[1] - pmin_pmax[0])
            normalized_param_list.append(z)

        return normalized_param_list

    @classmethod
    def denormalize_params(cls, normalized_param_list):
        """
        Denormalize parameter list.. Parameters must be in same order as listed in db.
        """

        # Get mins and maxes
        min_max = cls.get_min_max()

        denormalized_param_list = []

        # Calculate the denormalized values
        for param, pmin_pmax in zip(normalized_param_list, min_max):
            x = param * (pmin_pmax[1] - pmin_pmax[0]) + pmin_pmax[0]
            denormalized_param_list.append(x)

        return denormalized_param_list

    @classmethod
    def match(cls, param_list, param_list_is_normalized=False, return_normalized_match=False):
        """
        Match params given to the closest in db
        """
        # Make a session
        session = SessionMaker()

        # Denormalize if parameter list is noramalized
        if param_list_is_normalized:
            param_list = cls.denormalize_params(param_list)

        # Get the mins and maxes
        min_max = cls.get_min_max()

        # Get scenarios params
        scenario_params = cls.get_scenario_params()

        # Instantiate scenario selector
        scenario_selector = ScenarioSelector(param_list,
                                             scenario_params,
                                             min_max)

        # Use scenario selector to find match
        match_id = scenario_selector.getClosest()

        # Get the match parameters
        match_params = session.query(cls).filter(cls.scenario_id == match_id).one()

        # Close the connection
        session.close()

        return {"scenario_id": match_id,
                "parameters": match_params.as_list(normalized=return_normalized_match)}


class CannedResult(Base):
    """
    Data model for storing all the result datasets
    """
    __tablename__ = 'canned_results'

    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer)
    hydrograph = Column(String)

    def __init__(self, scenario_id, hydrograph):
        """
        Constructor for canned result
        """
        self.scenario_id = scenario_id
        self.hydrograph = hydrograph

    @classmethod
    def get_hydrograph_by_id(cls, scenario_id):
        """
        Get the hydrograph by scenario id
        """

        # Create session
        session = SessionMaker()

        # Assemble path to hydrograph file
        raw_data_string = session.query(cls.hydrograph).\
                                  filter(cls.scenario_id == scenario_id).\
                                  one()

        # Close the connection
        session.close()

        # Split
        lines = raw_data_string[0].splitlines()

        data = []

        for line in lines:
            point = map(float, line.strip().split())
            point[0] = decimal_year_to_datetime(point[0])
            data.append(point)

        return data

