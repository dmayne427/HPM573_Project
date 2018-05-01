import HW11.ParameterClasses as P
import HW11.MarkovModelDigital as MarkovCls
import HW11.SupportMarkovModel as SupportMarkov
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs

# create and cohort
cohort = MarkovCls.Cohort(
    id=1,
    therapy=P.Therapies.NONE)

simOutputs = cohort.simulate()

# graph survival curve
PathCls.graph_sample_path(
    sample_path=simOutputs.get_survival_curve(),
    title='Survival Curve of Women Screened via Digital Mammography',
    x_label='Simulation time step',
    y_label='Number of alive patients'
    )

# graph histogram of survival times
Figs.graph_histogram(
    data=simOutputs.get_survival_times(),
    title='Survival Times of Women Screened via Digital Mammography',
    x_label='Survival time (years)',
    y_label='Counts',
    bin_width=2
)

# graph histogram of number of strokes
# Figs.graph_histogram(
 #   data=simOutputs.get_if_developed_stroke(),
   # title='Number of Strokes per Patient',
   # x_label='Strokes',
   # y_label='Counts',
  #  bin_width=1
# )

