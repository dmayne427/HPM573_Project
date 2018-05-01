import HW11.ParameterClasses as P
import HW11.MarkovModelFilm as MarkovFilm
import HW11.MarkovModelDigital as MarkovDigital
import HW11.SupportMarkovModel as SupportMarkov

# FILM
# create a cohort
cohort_film = MarkovFilm.Cohort(id=0, therapy=P.Therapies.NONE)
simOutputs_film = cohort_film.simulate()

# DIGITAL
# create a cohort
cohort_digital = MarkovDigital.Cohort(id=1, therapy=P.Therapies.NONE)
simOutputs_digital = cohort_digital.simulate()

# draw survival curves and histograms
SupportMarkov.draw_survival_curves_and_histograms(simOutputs_film, simOutputs_digital)

# print the estimates
SupportMarkov.print_outcomes(simOutputs_film, "Film")
SupportMarkov.print_outcomes(simOutputs_digital, "Digital")

# print comparative outcomes
SupportMarkov.print_comparative_outcomes(simOutputs_film, simOutputs_digital)

# report the CEA results
SupportMarkov.report_CEA_CBA(simOutputs_film, simOutputs_digital)


