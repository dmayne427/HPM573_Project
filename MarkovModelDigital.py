import scr.SamplePathClasses as PathCls
import scr.StatisticalClasses as StatCls
import scr.RandomVariantGenerators as rndClasses
import scr.EconEvalClasses as EconCls
import HW11.ParameterClasses as P
import HW11.InputDataDigital as Data


class Patient:
    def __init__(self, id, parameters):
        """ initiates a patient
        :param id: ID of the patient
        :param parameters: parameter object
        """

        self._id = id
        self._rng = None
        self._param = parameters
        self._stateMonitor = PatientStateMonitor(parameters)
        self._delta_t = parameters.get_delta_t()
        self._TestSens = Data.TEST_SENS_DIGITAL
        #self._currentState = parameters.get_initial_health_state()

    def simulate(self, sim_length):
        """ simulate the patient over the specified simulation length """
        # random number generator for this patient
        self._rng = rndClasses.RNG(self._id)  # from now on use random number generator from support library
        k = 0

        while self._stateMonitor.get_if_alive() and k*self._delta_t < sim_length:
            trans_prob = self._param.get_transition_prob(self._stateMonitor.get_current_state())
            empirical_dist = rndClasses.Empirical(trans_prob)
            new_state_index = empirical_dist.sample(self._rng)


            self._stateMonitor.update(k, P.HealthStats(new_state_index), self._rng)

            k += 1


    def get_survival_time(self):
        return self._stateMonitor.get_survival_time()

    # def get_number_of_strokes(self):
     #   return self._stateMonitor.get_num_of_strokes()

    def get_total_discounted_cost(self):
        return self._stateMonitor.get_total_discounted_cost()

    def get_total_discounted_utility(self):
        return self._stateMonitor.get_total_discounted_utility()


class PatientStateMonitor:
    def __init__(self, parameters):
        self._currentState = parameters.get_initial_health_state()
        self._delta_t = parameters.get_delta_t()
        self._survivalTime = 0
        self._ifDevelopedStroke = False
        self._strokeCount = 0
        self._costUtilityOutcomes = PatientCostUtilityMonitor(parameters)
        self._TestSens = Data.TEST_SENS_DIGITAL


    def update(self, k, next_state, rng):
        if not self.get_if_alive():
            return

        if next_state in [P.HealthStats.DEAD]:
            self._survivalTime = (0.5+k) * self._delta_t  # k is number of steps its been, delta t is length of time
            # step, the 0.5 is a half cycle correction

        if k % (1 / self._delta_t) == 0:
            if self._currentState in [P.HealthStats.DETECTABLE, P.HealthStats.DYING]:
                # if the mammogram detects tumor:
                if rng.random_sample() < self._TestSens:
                    next_state = P.HealthStats.TREATMENT

                # if the mammogram does not detect tumor:
                else:
                    next_state = P.HealthStats.DYING

        # update the number of strokes experienced
       # if self._currentState == P.HealthStats.STROKE:
           # self._ifDevelopedStroke = True
           # self._strokeCount += 1

        # collect cost and utility outcomes
        self._costUtilityOutcomes.update(k, self._currentState, next_state)

        # update current health state
        self._currentState = next_state

    def get_if_alive(self):
        result = True
        if self._currentState in [P.HealthStats.DEAD]:
            result = False
        return result

    def get_current_state(self):
        return self._currentState

    def get_survival_time(self):
        """ returns the patient survival time """
        # return survival time only if the patient has died
        if not self.get_if_alive():
            return self._survivalTime
        else:
            return None

     # def get_num_of_strokes(self):
        # return self._strokeCount

    def get_total_discounted_cost(self):
        """:returns total discounted cost"""
        return self._costUtilityOutcomes.get_total_discounted_cost()

    def get_total_discounted_utility(self):
        """:returns total discounted utility"""
        return self._costUtilityOutcomes.get_total_discounted_utility()


class PatientCostUtilityMonitor:
    def __init__(self, parameters):

        # model parameters for this patient
        self._param = parameters

        # total cost and utility
        self._totalDiscountedCost = 0
        self._totalDiscountedUtility = 0

    def update(self, k, current_state, next_state):
        """updates the discounted total cost and health utility
        :param k: simulation time step
        :param current_state: current health state
        :param next_state: next health state
        """

        # update cost
        cost = 0.5*(self._param.get_annual_state_cost(current_state)+
                    self._param.get_annual_state_cost(next_state)) * self._param.get_delta_t()

        # update utility
        utility = 0.5*(self._param.get_annual_state_utility(current_state)+
                       self._param.get_annual_state_utility(next_state)) * self._param.get_delta_t()

        # treatment cost (incurred only in post-stroke state)
        if current_state is P.HealthStats.TREATMENT:
            if next_state is [P.HealthStats.DEAD]:
                cost += 0.5 * self._param.get_annual_treatment_cost() * self._param.get_delta_t()
            else:
                cost += 1 * self._param.get_annual_treatment_cost() * self._param.get_delta_t()

        # update total discounted cost and utility (NOT corrected for the half-cycle effect)
        self._totalDiscountedCost += \
            EconCls.pv(cost,self._param.get_adj_discount_rate(), k)
        self._totalDiscountedUtility += \
            EconCls.pv(utility,self._param.get_adj_discount_rate(), k)

    def get_total_discounted_cost(self):
        """ :returns total discounted cost"""
        return self._totalDiscountedCost

    def get_total_discounted_utility(self):
        """ :returns total discounted utility"""
        return self._totalDiscountedUtility


class Cohort:
    def __init__(self, id, therapy):
        """ create a cohort of patients
        :param id: an integer to specify the seed of the random number generator
        """
        self._initial_pop_size = Data.POP_SIZE
        self._patients = []      # list of patients

        # populate the cohort
        for i in range(self._initial_pop_size):
            # create a new patient (use id * pop_size + i as patient id)
            patient = Patient(id * self._initial_pop_size + i, P.ParametersFixed(therapy))
            # add the patient to the cohort
            self._patients.append(patient)

    def simulate(self):
        """ simulate the cohort of patients over the specified number of time-steps
        :returns outputs from simulating this cohort
        """

        # simulate all patients
        for patient in self._patients:
            patient.simulate(Data.SIM_LENGTH)

        # return the cohort outputs
        return CohortOutputs(self)

    def get_initial_pop_size(self):
        return self._initial_pop_size

    def get_patients(self):
        return self._patients


class CohortOutputs:
    def __init__(self, simulated_cohort):
        """ extracts outputs from a simulated cohort
        :param simulated_cohort: a cohort after being simulated
        """

        self._survivalTimes = []        # patients' survival times
        self._times_to_Stroke = []      # patients' times to stroke
        self._count_strokes = []        # patients' number of strokes
        self._costs = []                # patients' discounted total costs
        self._utilities = []            # patients' discounted total utilities

        # survival curve
        self._survivalCurve = \
            PathCls.SamplePathBatchUpdate('Population size over time', id, simulated_cohort.get_initial_pop_size())

        # find patients' survival times
        for patient in simulated_cohort.get_patients():

            # get the patient survival time
            survival_time = patient.get_survival_time()
            if not (survival_time is None):
                self._survivalTimes.append(survival_time)           # store the survival time of this patient
                self._survivalCurve.record(survival_time, -1)       # update the survival curve

           # count_strokes = patient.get_number_of_strokes()
           # self._count_strokes.append(count_strokes)

            # cost and utility
            self._costs.append(patient.get_total_discounted_cost())
            self._utilities.append(patient.get_total_discounted_utility())

        # summary statistics
        self._sumStat_survivalTime = StatCls.SummaryStat('Patient survival time', self._survivalTimes)
        # self._sumState_number_strokes = StatCls.SummaryStat('Time until stroke', self._count_strokes)
        self._sumStat_cost = StatCls.SummaryStat('Patient discounted cost', self._costs)
        self._sumStat_utility = StatCls.SummaryStat('Patient discounted utility', self._utilities)

    def get_if_developed_stroke(self):
        return self._count_strokes

    def get_survival_times(self):
        return self._survivalTimes

    def get_costs(self):
        return self._costs

    def get_utilities(self):
        return  self._utilities

    def get_sumStat_survival_times(self):
        return self._sumStat_survivalTime

    def get_survival_curve(self):
        return self._survivalCurve

    def get_sumStat_count_strokes(self):
        return self._sumState_number_strokes

    def get_sumStat_discounted_cost(self):
        return self._sumStat_cost

    def get_sumStat_discounted_utility(self):
        return self._sumStat_utility
