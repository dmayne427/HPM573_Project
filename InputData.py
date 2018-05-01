

import numpy as np

POP_SIZE = 1000     # cohort population size
SIM_LENGTH = 30    # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate
DELTA_T = 1/5      # years (length of time step, how frequently you look at the patient)
TEST_SENS_FILM = 0.62   # Sensitivity of film mammogram
TEST_SENS_DIGITAL = 0.77  # Sensitivity of digital mammogram


# transition rate matrix
TRANS_MATRIX = [
    [None,  0.04395,     0.0,   0.0,    0.0,    0.0],     # Healthy
    [0.0,   None,  .14286,   0.0,    0.0,    0.0],   # Undetectable
    [0.0,   0.0,     None,   0.0,    0.0,    0.0],     # Detectable
    [1.0,   0.0,     0.0,   None,    0.0,    0.0],      # Treatment
    [0.0,   0.0,     0.0,   0.0,    None,    0.2],      # Dying
    [0.0,   0.0,     0.0,   0.0,    0.0,    None],      # Dead
    ]


# RR of treatment in reducing incidence of stroke and stroke death while in Post-Stroke state
STROKE_RR = 1
# RR of treatment in increasing mortality due to bleeding
BLEEDING_RR = 1

# annual cost of each health state
ANNUAL_STATE_COST = [
    64.3,        # Healthy
    64.3,   # Undetectable
    64.3,    # Detectable
    21277,        # Treatment
    14202.6,         # Dying
    0           # Dead
    ]

# annual health utility of each health state
ANNUAL_STATE_UTILITY = [
    1,         # Healthy
    1,    # Undetectable
    0.944,       # Detectable
    0.731,         # Treatment
    0.352,          # Dying
    0           # Dead
    ]

# annual drug costs
Anticoagulant_COST = 2000.0

# annual probability of background mortality (number per 100,000 PY)
ANNUAL_PROB_BACKGROUND_MORT = 1763.8/100000
