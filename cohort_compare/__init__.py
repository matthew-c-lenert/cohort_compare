import numpy as np
import pandas as pd
import sklearn.metrics.pairwise as metric
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import geopandas as gp
import os

def score_county(cohort_avgs,county_avgs):
    cohort_array=[]
    county_score=[]
    for key in cohort_avgs.keys():
        cohort_array.append(cohort_avgs[key])
    for i in range(len(county_avgs["State_FIPS_Code"])):
        county_array=[]
        for key in cohort_avgs.keys():
            county_array.append(county_avgs[key][i])
        if len(county_array)==1:
            county_score.append(np.abs(county_array[0]-cohort_array[0]))
        else:
            county_score.append(np.asscalar(metric.cosine_similarity(np.array(cohort_array).reshape(1, -1),np.array(county_array).reshape(1, -1))))
    return(pd.DataFrame({"State_FIPS_Code":county_avgs["State_FIPS_Code"],"County_FIPS_Code":county_avgs["County_FIPS_Code"],"Similarity":county_score}))

def find_multi_conditional_score(criterion,incl_criteria,incl_corr_matrix,compare_corr_dict,row):
    compare_inclusion_cov_vector=[]
    inclusion_cov_matrix=[]
    inclusion_value_vector=[]
    inclusion_mean_vector=[]
    for incl_var in incl_criteria:
        compare_inclusion_cov_vector.append(compare_corr_dict[criterion+"_"+incl_var]*row[criterion+"_Standard_Error"]*row[incl_var+"_Standard_Error"])
        matrix_row=[]
        for incl_var2 in incl_criteria:
            if incl_var==incl_var2:
                matrix_row.append(row[incl_var+"_Standard_Error"]**2)
            else:
                matrix_row.append(row[incl_var+"_Standard_Error"]*row[incl_var2+"_Standard_Error"]*incl_corr_matrix.loc[incl_var,incl_var2])
        inclusion_cov_matrix.append(matrix_row)
        inclusion_value_vector.append(row[incl_var])
        inclusion_mean_vector.append(row[incl_var]-((row[incl_var]+row[incl_var+"2"])*0.5))

    compare_inclusion_cov_vector=np.array(compare_inclusion_cov_vector).reshape(1,len(incl_criteria))
    inclusion_cov_matrix=np.mat(inclusion_cov_matrix)
    inclusion_value_vector=np.array(inclusion_value_vector).reshape(len(incl_criteria),1)
    inclusion_mean_vector=np.array(inclusion_mean_vector).reshape(len(incl_criteria),1)
    conditional_value=row[criterion]+np.asscalar(compare_inclusion_cov_vector*inclusion_cov_matrix.I*(inclusion_value_vector-inclusion_mean_vector))
    if conditional_value < 0:
        conditional_value=0
    elif conditional_value>1:
        conditional_value=1
    return(conditional_value)

def find_single_conditional_score(county_comp_value,county_comp_var,corr,inclu_1,inclu_2,var_inclu):
    conditional_value=county_comp_value+corr*county_comp_var/var_inclu*(inclu_1-((inclu_1+inclu_2)/2.0))
    if conditional_value < 0:
        conditional_value=0
    elif conditional_value>1:
        conditional_value=1
    return(conditional_value)


def get_cohort_similarity_to_counties(cohort_avgs,compare_criteria,incl_criteria):
    this_dir, this_filename = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir,"data","County_Data_after_impute_after_scaling.csv")
    county_data=pd.read_csv(DATA_PATH)

    for incl_var in incl_criteria:
        if incl_var not in ["CKD","Smoker","Obesity","CHD","Hypertension","Stroke","Diabetes"]:
            raise ValueError("Undefined inclusion criteria specified. Please limit inclusion criteria to any combination of: CKD, Smoker, Obesity, CHD, Hypertension, Stroke, Diabetes\n\n Use data_dictionary() to reference variable definitions.")

    for comp_val in compare_criteria:
        if comp_val not in county_data.columns.values:
            raise ValueError("Undefined comparison criteria specified. Please pick any combination of: Poverty, Age_19_Under, Age_19_64, Age_65_84, Age_85_and_Over, White, Black, Native_American, Asian, Hispanic, CKD, Smoker, Obesity, Hypertension, CHD, Stroke, Diabetes, Avg_Drug_Deaths, LBW, VLBW, Premature, Under_18, Over_40, Unmarried, Late_Care, Brst_Cancer, Col_Cancer, Lung_Cancer, Suicide, Total_Deaths, FluB_Rpt, HepA_Rpt, HepB_Rpt, Meas_Rpt, Pert_Rpt, CRS_Rpt, Syphilis_Rpt, No_Exercise\n\n Use data_dictionary() to reference variable definitions.")

    for key in cohort_avgs.keys():
        if key not in county_data.columns.values:
            raise ValueError("Undefined cohort average specified. Please pick any combination of: Poverty, Age_19_Under, Age_19_64, Age_65_84, Age_85_and_Over, White, Black, Native_American, Asian, Hispanic, CKD, Smoker, Obesity, Hypertension, CHD, Stroke, Diabetes, Avg_Drug_Deaths, LBW, VLBW, Premature, Under_18, Over_40, Unmarried, Late_Care, Brst_Cancer, Col_Cancer, Lung_Cancer, Suicide, Total_Deaths, FluB_Rpt, HepA_Rpt, HepB_Rpt, Meas_Rpt, Pert_Rpt, CRS_Rpt, Syphilis_Rpt, No_Exercise\n\n Use data_dictionary() to reference variable definitions.")

    conditioned_criteria={}
    if len(incl_criteria)==0:
        for criterion in compare_criteria:
            conditioned_criteria[criterion]=county_data[criterion]

    elif len(incl_criteria)==1:
        incl_criterion=incl_criteria[0]
        for criterion in compare_criteria:
            corr_y=pearsonr(county_data[criterion],county_data[incl_criteria[0]])[0]
            conditioned_criteria[criterion]=county_data.apply(lambda row: find_single_conditional_score(row[criterion],row[criterion+"_Standard_Error"],corr_y,row[incl_criterion],row[incl_criterion+"2"],row[incl_criterion+"_Standard_Error"]),1)

    else:
        inclusion_corr=county_data[incl_criteria].corr()
        for criterion in compare_criteria:
            corr_dict={}
            for incl_var in incl_criteria:
                corr_dict[criterion+"_"+incl_var]=pearsonr(county_data[criterion],county_data[incl_var])[0]
            conditioned_criteria[criterion]=county_data.apply(lambda row: find_multi_conditional_score(criterion,incl_criteria,inclusion_corr,corr_dict,row),1)

    conditioned_criteria["State_FIPS_Code"]=county_data["State_FIPS_Code"]
    conditioned_criteria["County_FIPS_Code"]=county_data["County_FIPS_Code"]

    return(score_county(cohort_avgs,conditioned_criteria))

def map_similarirty(similarity_df,state_list,label_counties,plot_file_name):
    this_dir, this_filename = os.path.split(__file__)
    mod_dir=this_dir.replace("//","/")
    DATA_PATH = os.path.join(mod_dir,"data","us-albers-counties.json")
    usa=gp.read_file(DATA_PATH)
    usa['STATE']=usa['state_fips'].astype('int64')
    usa['COUNTY']=usa['county_fips'].astype('int64')
    similarity_df["Normalized_Similarity"]=100*(similarity_df['Similarity']-min(similarity_df['Similarity']))/(max(similarity_df['Similarity'])-min(similarity_df['Similarity']))
    sim_usa=usa.merge(similarity_df, left_on=['STATE','COUNTY'],right_on=['State_FIPS_Code','County_FIPS_Code'])
    fontsize=3
    fig_size=80
    num_states=len(state_list)
    if num_states>0:
        sim_usa=sim_usa.loc[sim_usa['iso_3166_2'].isin(state_list)]
        if num_states <5:
            fontsize=6
            fig_size=30
        elif num_states <10:
            fontsize=5
            fig_size=40
        elif num_states <20:
            fontsize=4
            fig_size=50
        elif num_states <30:
            fontsize=3
            fig_size=60
        elif num_states <40:
            fontsize=3
            fig_size=70

    plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots(1, figsize=(fig_size, fig_size-10))
    ax.set_axis_off()
    plt.axis('equal')
    sim_usa.plot( column='Normalized_Similarity' ,cmap='YlGn', ax=ax,  edgecolor='grey')

    props = dict(boxstyle='round', facecolor='linen', alpha=0.25)
    if label_counties:
        sim_usa['centroid'] = sim_usa['geometry'].centroid
        for point in sim_usa.iterrows():
            ax.text(point[1]['centroid'].x,
                    point[1]['centroid'].y,
                    point[1]['name']+", "+point[1]['iso_3166_2'],
                    horizontalalignment='center',
                    fontsize=3,
                    bbox=props)
    if plot_file_name!="":
        plt.savefig(plot_file_name,dpi=300,quality=95)

def get_cohort_avgs(cohort_df,comparison_mappings):
    column_means=cohort_df.mean()
    cohort_avgs={}
    for key in comparison_mappings.keys():
        if key not in cohort_df.columns.values:
            raise ValueError("Check comparison mappings. "+str(key)+" column not found in cohort dataframe.")
        else:
            mean_val=column_means.loc[key]
            if (mean_val>1) or (mean_val<0):
                raise ValueError("Please rescale cohort variables to be on the percentage scale [0-1]. Column "+str(key)+" needs rescaling.")
            cohort_avgs[comparison_mappings[key]]=column_means.loc[key]
    return(cohort_avgs)

def map_cohort_avgs(cohort_averages,comparison_mappings):
    cohort_avgs={}
    for key in comparison_mappings.keys():
        if key not in cohort_averages:
            raise ValueError("Check comparison mappings. "+str(key)+" column not found in cohort averages dictionary.")
        else:
            cohort_avgs[comparison_mappings[key]]=cohort_averages[key]
    return(cohort_avgs)

def compare_cohort_to_counties(comparison_mappings,cohort_df=pd.DataFrame({'A' : []}),cohort_averages={},incl_criteria=[],state_list=[],label_counties=False,plot_file_name="",return_similarity_scores=False,print_progress=False):
    cohort_avgs={}
    if len(cohort_averages)==0:
        if cohort_df.empty:
            raise ValueError("There are no cohort observations or averages to compare.")
        else:
            if print_progress:
                print("Calculating cohort averages for comparison criteria\n")
            cohort_avgs=get_cohort_avgs(cohort_df,comparison_mappings)
    else:
        if len(comparison_mappings)>0:
            cohort_avgs=map_cohort_avgs(cohort_averages,comparison_mappings)
        else:
            cohort_avgs=cohort_averages
    if print_progress:
        print("Calculating similarity score to US counties\n")
    similarity_df=get_cohort_similarity_to_counties(cohort_avgs,list(comparison_mappings.values()),incl_criteria)
    if print_progress:
        print("Creating similarity map\n")
    map_similarirty(similarity_df,state_list,label_counties,plot_file_name)
    if return_similarity_scores:
        return(similarity_df)


def data_dictionary():
    print("This package includes county level public health data from the Center for Disease Control and Prevention and the Department for Health and Human Services from 2001-2016. Missing values were imputed using Frank Harrell's multiple imputation implementation in the 'Hmisc' package in the R programming language. All data elements were scaled to represent the basic percentage of the county residents.\n \n #### Inclusion Criteria ####\n CKD: Death due to chronic kidney disease and other forms of kidney disease. ICD-10 codes: N00-N07, N17-N19, N25-N27.\n CHD: Death due to hypertensive heart disease and ischemic heart diseases (acute myocardial infarction, other acute ischemic heart diseases, and other forms of chronic ischemic heart disease), ICD-9 codes: 402, 410-414, and 429.2. ICD-10 codes: I11, I20-I25.\n Diabetes: The percentage of adults who responded 'yes' to the question, 'Have you ever been told by a doctor that you have diabetes?'\n Hypertension: The percentage of adults who responded yes to the question, 'Have you ever been told by a doctor, nurse, or other health professional that you have high blood pressure?'\n Obesity: The calculated percentage of adults at risk for health problems related to being overweight, based on body mass index (BMI). A BMI of 30.0 or greater is considered obese.\n Smoker: The percentage of adults who responded 'yes' to the question, 'Do you smoke cigarettes now?'\n Stroke: Death due to cerebrovascular diseases, ICD-9 codes: 430-438. ICD-10 codes: I60-I69.\n \n \n #### Comparison Criteria ####\n Poverty: The percentage of individuals living below the poverty level in 2008 is data obtained from the 'Small Area Income Poverty Estimates (SAIPE),' U.S. Bureau of the Census and can be obtained at http://www.census.gov/did/www/saipe/data/statecounty/data/index.html.\n Age_19_Under: Age-specific population sizes are from 'Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.'\n Age_19_64: Age-specific population sizes are from 'Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.'\n Age_65_84: Age-specific population sizes are from 'Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.'\n Age_85_and_Over: Age-specific population sizes are from 'Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.'\n Asian: Age-specific population sizes are from 'Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.'\n Black: Age-specific population sizes are from 'Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.'\n Hispanic: Age-specific population sizes are from 'Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.'\n Native_American: Age-specific population sizes are from 'Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.\n 'White: Age-specific population sizes are from 'Annual estimates of the resident population by age, sex, race, and Hispanic origin for counties.'\n CKD: See above\n Smoker: See above\n Obesity: See above\n Hypertension: See above\n CHD: See above\n Stroke: See above\n Diabetes: See above\n Avg_Drug_Deaths: Deaths are classified using the International Classification of Diseases, Tenth Revision (ICD–10). Drug-poisoning deaths are defined as having ICD–10 underlying cause-of-death codes X40–X44 (unintentional), X60–X64 (suicide), X85 (homicide), or Y10–Y14 (undetermined intent).\n LBW: Percentage of all births less than 2,500 grams\n VLBW: Percentage of all births less than 1,500 grams\n Premature: Percentage of births with a reported gestation period of less than 37completed weeks\n Under_18: Percentage of all births to mothers less than 18 years of age\n Over_40: Percentage of all births to mothers 40-54 years of age.\n Unmarried: Percentage of all births to mothers who report not being married.\n Late_Care: Percentage of births to mothers who reported receiving no prenatal care during the first trimester (3 months) of pregnancy, and includes those with no prenatal care\n Brst_Cancer: Death due to malignant neoplasm of the female breast, ICD-9 code: 174. ICD-10 code: C50.\n Col_Cancer: Death due to malignant neoplasm of the colon, rectum and anus, ICD-9 codes: 153 and 154. ICD-10 codes: C18-C21.\n Lung_Cancer: Death due to malignant neoplasm of the trachea, bronchus and lung, ICD-9 code: 162. ICD-10 codes: C33-C34.\n Suicide: Intentional self-harm, ICD-9 codes: E950-E959. ICD-10 codes: *U03, X60-X84, Y87.0.\n Total_Deaths: Mortality from any cause is the period rate for all causes of death, age-adjusted to the year 2010 Standard Population. County-specific data are only reported if there are at least 10 deaths.\n FluB_Rpt: County data, Influenza B reported cases\n HepA_Rpt: County data, Hepatitis A reported cases\n HepB_Rpt: County data, Hepatitis B reported cases\n Meas_Rpt: County data, Measles reported cases\n Pert_Rpt: County data, Pertussis reported cases\n CRS_Rpt: County data, Congenital Rubella Syndrome reported cases\n Syphilis_Rpt: County data, Syphilis reported cases\n No_Exercise: The percentage of adults reporting of no participation in any leisure-time physical activities or exercises in the past month.")


