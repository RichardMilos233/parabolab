import Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Independence
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.Topology.ContinuousMap.Bounded.Basic
import Mathlib.Tactic

open MeasureTheory ProbabilityTheory
open scoped BigOperators BoundedContinuousFunction

#check HasGaussianLaw.eval
#check HasGaussianLaw.sum
#check HasGaussianLaw.fun_sum
#check HasGaussianLaw.prodMk
#check HasGaussianLaw.map
#check HasGaussianLaw.map_fun
#check HasGaussianLaw.indepFun_of_covariance_eval
#check HasGaussianLaw.map_eq_gaussianReal
#check iIndepFun.hasGaussianLaw
#check iIndepFun.indepFun
#check iIndepFun.indepFun₀
#check iIndepFun.pairwise_indepFun
#check IndepFun.covariance_eq_zero
#check IndepFun.map_prod_eq_prod_map_map
#check ContinuousLinearMap.proj
#check ContinuousLinearMap.pi
#check ContinuousLinearMap.prod
#check ContinuousLinearMap.fst
#check ContinuousLinearMap.snd
#check covariance_fun_sum_right
#check covariance_fun_sum_left
#check covariance_fun_sum_fun_sum
#check covariance_const_mul_left
#check covariance_const_mul_right
#check covariance_sub_left
#check covariance_sub_right
#check covariance_sub_sub
#check covariance_self
#check variance_nonneg
#check variance_eq_integral
#check integral_finsetSum
#check integral_map
#check Measure.map_map
#check AEMeasurable.map_map_of_aemeasurable
#check BoundedContinuousFunction.integrable
#check Integrable.comp_aemeasurable
#check Integrable.comp_measurable
#check MeasureTheory.Integrable.integral_prod_left
#check MeasureTheory.integral_prod
