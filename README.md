# The cohort_compare Package
A library of functions for comparing clinical cohorts to the populations of US counties

## Package Definitions

The goal of this package is to provide clinical researchers with means for comparing their research cohorts to relevant populations in US counties. Counties with more similar populations to the study cohort should also see similar results. To this end, this package implements methodology from Lenert MC, Mize DE, Walsh CG. X Marks the Spot: Mapping Similarity Between Clinical Trial Cohorts and US Counties. AMIA . Annu Symp proceedings AMIA Symp. 2017;2017:1110-1119.

Comparing your cohort to US Counties requires the researcher to define 2 essential parameters:

1.  Inclusion criteria: prerequisite patient characteristics for participation in your study or trial. These are defined features that separate your study population from the population at large, e.g. the presence of a specific disease. For a full list of supported inclusion criteria, scroll down to the Data Dictionary section.

2.  Comparison criteria: measured variables from your patient cohort that can be compared to county health data. The set of data elements from your research cohort and county heath statistics with similar definitions. For a full list of supported comparison criteria, scroll down to the Data Dictionary section.


## Package Functions and Parameters

### compare_cohort_to_counties(comparison_mappings, cohort_df=pd.DataFrame({'A' : []}), cohort_averages={}, incl_criteria=[], state_list=[], label_counties=False, plot_file_name="", return_similarity_scores=False, print_progress=False, color_scheme='YlGn')

This is the main function of the library and is meant to take you from a cohort to a similarity map. This function can use your cohort dataframe to calculate the similarity of each US county to your cohort based on the comparison criteria and the inclusion criteria. Then it will map the normalized similarity scores to a chloropleth map of all US counties. The parameters for this function are defined below:

comparison_mappings: a dictionary that maps cohort variables to county health statistics. For example, {“does_smoke”:”Smoker”, “is_obese”:”Obesity”}. For a list and definitions of county health statistics scroll down to the Data Dictionary section.

cohort_df: a wide-format (1-row per subject) pandas dataframe of the cohort. The dataframe should have all comparison criteria coded as binary {0,1} variables. The package will find the average rate (the mean) for each comparison criterion to compare against the county average rate. This parameter is optional.

cohort_averages: a dictionary of the central moment (e.g. mean, median, or mode) of cohort comparison variables on the percentage scale [0, 1]. For example: {“does_smoke”: 0.34, “is_obese”: 0.55}. This parameter is optional. The user should specify either the cohort_df OR the cohort_averages.

incl_criteria: a list of variables that define a subpopulation of each county that this package should use to compare against the cohort.  For example, specifying [“Hypertension”] will cause the function to use county residents with hypertension for comparison against your research cohort. This parameter is optional.

state_list: the list of state abbreviations you wish to have mapped. For example [“TN”,”GA”] will create a chloropleth map of cohort similarity to populations of the counties in Tennessee and Georgia. The default, [], will result in all US counties being included in the map. This parameter is optional.

label_counties: a Boolean flag for labeling each county with the county name and state abbreviation. Adding county labels can add minutes to the map building process. The default, False, will result in no labels being included on the map. This parameter is optional.

plot_file_name: a string file path for storing the generated map image. These images can be 10’s of MB, so choose your storage location carefully. The default, “”, will result in no image being saved to disk. This parameter is optional.

return_similarity_scores: a Boolean flag for outputting the pandas dataframe of county identifiers and their corresponding similarity scores (normalized and un-normalized). The default, False, will result in no dataframe being output by the function. This parameter is optional.

print_progress: a Boolean flag for printing to console the different steps the function takes in producing a similarity map. The default, False, will result in no messages being printed to the console. This parameter is optional.

color_scheme: the matplotlib color map used to shade county similarity. See https://matplotlib.org/tutorials/colors/colormaps.html for options. The default is 'YlGn'.

### get_cohort_similarity_to_counties(cohort_avgs, compare_criteria, incl_criteria)

A helper function to calculate the similarity score of US counties to the research cohort centroids (e.g. mean or median), based on the compare criteria and the inclusion criteria. Similarity is measured as the cosine distance from the cohort feature vector to the county feature vector.

cohort_avgs: a mapped dictionary of values representing the centroid of the cohort labeled with the appropriate county variable name. For example, {“Smoker”:0.34, “Obesity”: 0.55}.


### map_similarirty(similarity_df, state_list, label_counties, plot_file_name, color_scheme)

A helper function that turns a data frame of similarity scores into a chloropleth map.

similarity_df: a dataframe that includes the following columns: “State_FIPS_Code”, “County_FIPS_Code”, and “Similarity”.


## Package Data Dictionary

This package includes county level public health data from the Center for Disease Control and Prevention and the Department for Health and Human Services from 2001-2016. Missing values were imputed using Frank Harrell’s multiple imputation implementation in the ‘Hmisc’ package in the R programming language. All data elements were scaled to represent the basic percentage of the county residents.

### Inclusion Criteria

CKD: Death due to chronic kidney disease and other forms of kidney disease. ICD-10 codes: N00-N07, N17-N19, N25-N27.

CHD: Death due to hypertensive heart disease and ischemic heart diseases (acute myocardial infarction, other acute ischemic heart diseases, and other forms of chronic ischemic heart disease), ICD-9 codes: 402, 410-414, and 429.2. ICD-10 codes: I11, I20-I25.

Diabetes: The percentage of adults who responded “yes” to the question, “Have you ever been told by a doctor that you have diabetes?”

Hypertension: The percentage of adults who responded yes to the question, “Have you ever been told by a doctor, nurse, or other health professional that you have high blood pressure?”

Obesity: The calculated percentage of adults at risk for health problems related to being overweight, based on body mass index (BMI). A BMI of 30.0 or greater is considered obese.

Smoker: The percentage of adults who responded “yes” to the question, “Do you smoke cigarettes now?”

Stroke: Death due to cerebrovascular diseases, ICD-9 codes: 430-438. ICD-10 codes: I60-I69.


### Comparison Criteria
Poverty: The percentage of individuals living below the poverty level in 2008 is data obtained from the “Small Area Income Poverty Estimates (SAIPE),” U.S. Bureau of the Census and can be obtained at http://www.census.gov/did/www/saipe/data/statecounty/data/index.html.

Age_19_Under: Age-specific population sizes are from “Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.”

Age_19_64: Age-specific population sizes are from “Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.”

Age_65_84: Age-specific population sizes are from “Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.”

Age_85_and_Over: Age-specific population sizes are from “Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.”

Asian: Age-specific population sizes are from “Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.”

Black: Age-specific population sizes are from “Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.”

Hispanic: Age-specific population sizes are from “Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.”

Native_American: Age-specific population sizes are from “Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.”

White: Age-specific population sizes are from “Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.”

CKD: See above

Smoker: See above

Obesity: See above

Hypertension: See above

CHD: See above

Stroke: See above

Diabetes: See above

Avg_Drug_Deaths: Deaths are classified using the International Classification of Diseases, Tenth Revision (ICD–10). Drug-poisoning deaths are defined as having ICD–10 underlying cause-of-death codes X40–X44 (unintentional), X60–X64 (suicide), X85 (homicide), or Y10–Y14 (undetermined intent).

LBW: Percentage of all births less than 2,500 grams

VLBW: Percentage of all births less than 1,500 grams

Premature: Percentage of births with a reported gestation period of less than 37completed weeks

Under_18: Percentage of all births to mothers less than 18 years of age

Over_40: Percentage of all births to mothers 40-54 years of age.

Unmarried: Percentage of all births to mothers who report not being married.

Late_Care: Percentage of births to mothers who reported receiving no prenatal care during the first trimester (3 months) of pregnancy, and includes those with no prenatal care

Brst_Cancer: Death due to malignant neoplasm of the female breast, ICD-9 code: 174. ICD-10 code: C50.

Col_Cancer: Death due to malignant neoplasm of the colon, rectum and anus, ICD-9 codes: 153 and 154. ICD-10 codes: C18-C21.

Lung_Cancer: Death due to malignant neoplasm of the trachea, bronchus and lung, ICD-9 code: 162. ICD-10 codes: C33-C34.

Suicide: Intentional self-harm, ICD-9 codes: E950-E959. ICD-10 codes: *U03, X60-X84, Y87.0.

Total_Deaths: Mortality from any cause is the period rate for all causes of death, age-adjusted to the year 2010 Standard Population. County-specific data are only reported if there are at least 10 deaths.

FluB_Rpt: County data, Influenza B reported cases

HepA_Rpt: County data, Hepatitis A reported cases

HepB_Rpt: County data, Hepatitis B reported cases

Meas_Rpt: County data, Measles reported cases

Pert_Rpt: County data, Pertussis reported cases

CRS_Rpt: County data, Congenital Rubella Syndrome reported cases

Syphilis_Rpt: County data, Syphilis reported cases

No_Exercise: The percentage of adults reporting of no participation in any leisure-time physical activities or exercises in the past month.


## Citing this Package

When using this package for research purposes, please cite “Lenert MC, Mize DE, Walsh CG. X Marks the Spot: Mapping Similarity Between Clinical Trial Cohorts and US Counties. AMIA . Annu Symp proceedings AMIA Symp. 2017;2017:1110-1119.”

