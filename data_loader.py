import pandas as pd
import numpy as np
from collections import Counter

class DataLoader:

    def __init__(self):
        pass
        
    def load_csv(self, csv_file):
        try:
            df = pd.read_csv(csv_file, header=None)
            return df
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            raise
            
    def load_demographic_data(self, df):

        try:

            questions_row = df.iloc[1]

            col_indices = {}
            for i, question in enumerate(questions_row):
                if not isinstance(question, str):
                    continue
                
                question = question.lower()
                if 'year were you born' in question:
                    col_indices['birthYear'] = i
                elif 'nationality' in question:
                    col_indices['nationality'] = i
                elif 'do you have children' in question:
                    col_indices['childrenYesNo'] = i
                elif 'how many children' in question:
                    col_indices['childrenCount'] = i
                elif 'marital status' in question:
                    col_indices['maritalStatus'] = i
                elif 'disability' in question:
                    col_indices['disability'] = i
                elif 'year did you begin your doctorate' in question:
                    col_indices['doctoralYear'] = i
                elif 'confident are you that you will achieve' in question:
                    col_indices['confidenceLevel'] = i

            responses = df.iloc[4:].copy()
            

            data = []
            for i, row in responses.iterrows():
                try:
                    birth_year = int(row[col_indices['birthYear']]) if pd.notna(row[col_indices['birthYear']]) else None
                    if birth_year and (birth_year < 1900 or birth_year > 2025):
                        birth_year = None
                except (ValueError, TypeError):
                    birth_year = None
                    
                try:
                    children_count = int(row[col_indices['childrenCount']]) if pd.notna(row[col_indices['childrenCount']]) else 0
                except (ValueError, TypeError):
                    children_count = 0
                    
                try:
                    doctoral_year = int(row[col_indices['doctoralYear']]) if pd.notna(row[col_indices['doctoralYear']]) else None
                    if doctoral_year and (doctoral_year < 1950 or doctoral_year > 2025):
                        doctoral_year = None
                except (ValueError, TypeError):
                    doctoral_year = None
                
                disability_value = str(row[col_indices['disability']]).strip() if pd.notna(row[col_indices['disability']]) else 'No'
                
                respondent = {
                    'id': i - 3,
                    'birthYear': birth_year,
                    'nationality': str(row[col_indices['nationality']]).strip() if pd.notna(row[col_indices['nationality']]) else '',
                    'hasChildren': str(row[col_indices['childrenYesNo']]) == 'Yes',
                    'childrenCount': children_count,
                    'maritalStatus': str(row[col_indices['maritalStatus']]).strip() if pd.notna(row[col_indices['maritalStatus']]) else '',
                    'disabilityStatus': disability_value,
                    'doctoralYear': doctoral_year,
                    'confidenceLevel': str(row[col_indices['confidenceLevel']]).strip() if pd.notna(row[col_indices['confidenceLevel']]) else ''
                }
                data.append(respondent)
                
            return data
            
        except Exception as e:
            print(f"Error loading demographic data: {e}")
            return []
    
    def get_demographic_chart_data(self, data, data_type):

        if data_type == 'children':
            children_counts = [r['childrenCount'] for r in data if r['hasChildren'] and r['childrenCount'] > 0]
            count_frequency = Counter(children_counts)
            return [{'name': f"{count}", 'value': frequency} 
                  for count, frequency in sorted(count_frequency.items())]
            
        elif data_type == 'birthYear':
            valid_birth_years = [r['birthYear'] for r in data 
                               if r['birthYear'] is not None and 1900 <= r['birthYear'] <= 2025]
            year_counts = Counter(valid_birth_years)
            return [{'name': str(year), 'value': count} for year, count in sorted(year_counts.items())]
            
        elif data_type == 'maritalStatus':
            status_count = {}
            for r in data:
                if r['maritalStatus']:
                    status_count[r['maritalStatus']] = status_count.get(r['maritalStatus'], 0) + 1
            return [{'name': name, 'value': value} for name, value in status_count.items()]
            
        elif data_type == 'disability':
            disability_count = {'Yes': 0, 'No': 0, 'Unsure': 0}
            for r in data:
                status = r['disabilityStatus']
                if status not in disability_count:
                    status = 'No'
                disability_count[status] += 1
            
            ordered_results = []
            for category in ['Yes', 'Unsure', 'No']:
                if disability_count[category] > 0:
                    ordered_results.append({'name': category, 'value': disability_count[category]})
            return ordered_results
            
        elif data_type == 'doctoralYear':
            valid_doctoral_years = [r['doctoralYear'] for r in data 
                                  if r['doctoralYear'] is not None and 1950 <= r['doctoralYear'] <= 2025]
            year_counts = Counter(valid_doctoral_years)
            return [{'name': str(year), 'value': count} for year, count in sorted(year_counts.items())]
            
        return []
            
    def extract_unique_subjects(self, df, subject_cols):

        unique_subjects = set()
        

        for i in range(4, len(df)):
            for col_index in subject_cols:
                if col_index >= len(df.columns):
                    continue
                    
                subject_value = df.iloc[i][col_index]
                if pd.notna(subject_value) and subject_value:

                    subjects = str(subject_value).split(',')
                    
                    for subject in subjects:
                        subject = subject.strip()
                        if subject and subject != "Other (Specify Below)":
                            unique_subjects.add(subject)
        

        return sorted(list(unique_subjects))

    def standardize_subject(self, subject, all_subjects):


        subject = subject.strip()
        

        if subject in all_subjects:
            return subject
                

        for std_subject in all_subjects:
            if subject.lower() == std_subject.lower():
                return std_subject
                

        for std_subject in all_subjects:
            if subject.lower() in std_subject.lower() or std_subject.lower() in subject.lower():

                return std_subject
                

        return "Other"
        
    def process_subject_data(self, df, row_index, subject_col_index, subject_dict, other_count, all_subjects, other_text_col=None):

        if subject_col_index >= len(df.columns):
            return other_count
            
        subject_value = df.iloc[row_index][subject_col_index]
        if pd.notna(subject_value) and subject_value:

            subjects = str(subject_value).split(',')
            
            for subject in subjects:
                subject = subject.strip()
                if subject:
                    if subject == "Other (Specify Below)" and other_text_col is not None:
                        if row_index < len(df) and other_text_col < len(df.columns) and pd.notna(df.iloc[row_index][other_text_col]):
                            other_subject = str(df.iloc[row_index][other_text_col]).strip()
                            if other_subject:
                                std_subject = self.standardize_subject(other_subject, all_subjects)
                                if std_subject == "Other":
                                    other_count += 1
                                else:
                                    subject_dict[std_subject] = subject_dict.get(std_subject, 0) + 1
                    else:
                        std_subject = self.standardize_subject(subject, all_subjects)
                        if std_subject == "Other":
                            other_count += 1
                        else:
                            subject_dict[std_subject] = subject_dict.get(std_subject, 0) + 1
                            
        return other_count

    def load_education_data(self, df):

        try:

            questions_row = df.iloc[1]
            undergrad_col = None
            masters_col = None
            doctoral_col = None
            
            for i, question in enumerate(questions_row):
                if not isinstance(question, str):
                    continue
                
                question = question.lower()
                if 'what was the subject area' in question and 'first degree' in str(df.iloc[0][i]).lower():
                    undergrad_col = i
                elif 'what was the subject area' in question and 'master' in str(df.iloc[0][i]).lower():
                    masters_col = i
                elif 'what subject area' in question and ('doctoral' in str(df.iloc[0][i]).lower() or 'doctorate' in question or 'phd' in question):
                    doctoral_col = i
            

            undergrad_col_index = undergrad_col if undergrad_col is not None else 36
            masters_col_index = masters_col if masters_col is not None else 42
            doctoral_col_index = doctoral_col if doctoral_col is not None else 51
            

            subject_cols = [undergrad_col_index, masters_col_index, doctoral_col_index]
            all_subjects = self.extract_unique_subjects(df, subject_cols)
            

            undergraduate_subjects = {}
            masters_subjects = {}
            doctoral_subjects = {}
            

            other_count_ug = 0
            other_count_ma = 0
            other_count_doc = 0
            

            for subject in all_subjects:
                undergraduate_subjects[subject] = 0
                masters_subjects[subject] = 0
                doctoral_subjects[subject] = 0
            

            for i in range(4, len(df)):

                other_count_ug = self.process_subject_data(
                    df, i, undergrad_col_index, undergraduate_subjects, 
                    other_count_ug, all_subjects, undergrad_col_index + 1
                )
                

                other_count_ma = self.process_subject_data(
                    df, i, masters_col_index, masters_subjects, 
                    other_count_ma, all_subjects, masters_col_index + 1
                )
                

                other_count_doc = self.process_subject_data(
                    df, i, doctoral_col_index, doctoral_subjects, 
                    other_count_doc, all_subjects, doctoral_col_index + 1
                )
            

            if other_count_ug > 0:
                undergraduate_subjects["Other"] = other_count_ug
            if other_count_ma > 0:
                masters_subjects["Other"] = other_count_ma
            if other_count_doc > 0:
                doctoral_subjects["Other"] = other_count_doc
            

            education_data = {}
            education_data['undergraduate_subjects'] = [
                {'name': subject, 'value': count} 
                for subject, count in sorted(undergraduate_subjects.items())
                if count > 0
            ]
            
            education_data['masters'] = [
                {'name': subject, 'value': count} 
                for subject, count in sorted(masters_subjects.items())
                if count > 0
            ]
            
            education_data['doctoral'] = [
                {'name': subject, 'value': count} 
                for subject, count in sorted(doctoral_subjects.items())
                if count > 0
            ]
            
            return all_subjects, education_data
            
        except Exception as e:
            print(f"Error processing education data: {e}")
            return [], {}
    
    def load_gender_employment_data(self, df):

        try:

            male_total = 0
            female_total = 0
            male_fulltime = 0
            female_fulltime = 0
            

            gender_col = 18  
            employment_col = 84  
            
 
            for i in range(4, len(df)):
                if gender_col >= len(df.columns) or employment_col >= len(df.columns):
                    break
                

                gender_value = str(df.iloc[i][gender_col]).strip() if pd.notna(df.iloc[i][gender_col]) else ""
                gender_value = gender_value.lower()
                

                if "female" in gender_value or gender_value == "f":
                    female_total += 1
                elif "male" in gender_value or gender_value == "m":
                    male_total += 1
                

                employment_value = str(df.iloc[i][employment_col]).strip() if pd.notna(df.iloc[i][employment_col]) else ""
                employment_value = employment_value.lower()
                

                if "full" in employment_value and "time" in employment_value:

                    if "female" in gender_value or gender_value == "f":
                        female_fulltime += 1
                    elif "male" in gender_value or gender_value == "m":
                        male_fulltime += 1
            

            male_percentage = (male_fulltime / male_total * 100) if male_total > 0 else 0
            female_percentage = (female_fulltime / female_total * 100) if female_total > 0 else 0
            

            gender_employment_data = {}
            

            gender_employment_data['fulltime_by_gender'] = [
                {'name': 'Female', 'value': round(female_percentage, 1)},
                {'name': 'Male', 'value': round(male_percentage, 1)}
            ]
            

            gender_employment_data['fulltime_counts'] = {
                'female_total': female_total,
                'male_total': male_total,
                'female_fulltime': female_fulltime,
                'male_fulltime': male_fulltime
            }
            

            fixed_term_col = 88
            female_with_fixed_term = 0
            male_with_fixed_term = 0
            

            for i in range(4, len(df)):
                if gender_col >= len(df.columns) or fixed_term_col >= len(df.columns):
                    break
                

                gender_value = str(df.iloc[i][gender_col]).strip() if pd.notna(df.iloc[i][gender_col]) else ""
                gender_value = gender_value.lower()
                

                fixed_term_value = df.iloc[i][fixed_term_col]
                has_fixed_term = False
                
                try:

                    fixed_term_count = int(fixed_term_value) if pd.notna(fixed_term_value) else 0
                    has_fixed_term = fixed_term_count > 0
                except (ValueError, TypeError):

                    if isinstance(fixed_term_value, str):
                        fixed_term_text = fixed_term_value.lower()

                        if fixed_term_text and fixed_term_text != "none" and fixed_term_text != "no" and fixed_term_text != "0":
                            import re
                            numeric_parts = re.findall(r'\d+', fixed_term_text)
                            if numeric_parts:
                                fixed_term_count = int(numeric_parts[0])
                                has_fixed_term = fixed_term_count > 0
                            else:
                                has_fixed_term = True

                if has_fixed_term:
                    if "female" in gender_value or gender_value == "f":
                        female_with_fixed_term += 1
                    elif "male" in gender_value or gender_value == "m":
                        male_with_fixed_term += 1
            

            female_fixed_term_percentage = (female_with_fixed_term / female_total * 100) if female_total > 0 else 0
            male_fixed_term_percentage = (male_with_fixed_term / male_total * 100) if male_total > 0 else 0
            

            gender_employment_data['fixed_term_by_gender'] = [
                {'name': 'Female', 'value': round(female_fixed_term_percentage, 1)},
                {'name': 'Male', 'value': round(male_fixed_term_percentage, 1)}
            ]
            

            gender_employment_data['fixed_term_counts'] = {
                'female_with_fixed_term': female_with_fixed_term,
                'male_with_fixed_term': male_with_fixed_term
            }
            
            return gender_employment_data
            
        except Exception as e:
            print(f"Error processing gender and employment data: {e}")
            return {}
    
    def process_barriers_data(self, df):

        try:

            barrier_categories = {
                "Work-life balance": ["work life", "work-life", "balance", "family", "personal life","fixed term"],
                "Childcare responsibilities": ["child", "children", "parenting", "maternity", "baby", "infant","kids"],
                "Limited funding": ["fund", "money", "financial", "budget", "grant", "resource","low-payment","funding","poor"],
                "Lack of mentoring": ["mentor","mentoring", "guidance", "supervision", "support", "advising"],
                "Gender bias": ["gender", "bias", "discrimination", "sexism", "woman", "female", "equality"],
                "Heavy workload": ["workload", "overwork", "busy", "time", "burden", "pressure", "stress", "admin"],
                "Lack of flexibility": ["rigid", "flex", "schedule", "hours", "remote", "accommodat"],
                "Field competition": ["compet", "crowd", "saturated", "job market", "position", "limited openings","competing"],
                "Health issues": ["health", "illness", "medical", "mental health", "burnout", "depression", "anxiety"],
                "Geographic limitations": ["location", "geograph", "mobility", "relocate", "move", "travel"]
            }
            

            barrier_counts = {key: 0 for key in barrier_categories.keys()}
            total_valid_responses = 0

            gender_col = 18
            

            barriers_col = 113
            
            if barriers_col >= len(df.columns) or gender_col >= len(df.columns):
                print(f"Error: Column index out of range. The dataset only has {len(df.columns)} columns.")
                return {}

            for i in range(4, len(df)):

                gender_value = str(df.iloc[i][gender_col]).strip().lower() if pd.notna(df.iloc[i][gender_col]) else ""
                is_female = "female" in gender_value or gender_value == "f"
                

                if not is_female:
                    continue

                barrier_value = df.iloc[i][barriers_col]
                

                if pd.isna(barrier_value) or str(barrier_value).strip().lower() in ['', 'n/a', 'none', 'no', 'not applicable']:
                    continue
                    

                total_valid_responses += 1

                barrier_text = str(barrier_value).lower()
                

                matched_category = False
                for category, keywords in barrier_categories.items():

                    if any(keyword.lower() in barrier_text for keyword in keywords):
                        barrier_counts[category] += 1
                        matched_category = True
                

                if not matched_category:
                    if "Other" not in barrier_counts:
                        barrier_counts["Other"] = 0
                    barrier_counts["Other"] += 1
            

            if total_valid_responses > 0:
                barrier_percentages = {
                    category: (count / total_valid_responses) * 100
                    for category, count in barrier_counts.items()
                }
            else:
                barrier_percentages = barrier_counts
            

            barriers_data = {}
            barriers_data['career_barriers'] = [
                {'name': name, 'value': round(percentage, 1)} 
                for name, percentage in sorted(barrier_percentages.items())
            ]
            

            barriers_data['raw_counts'] = barrier_counts
            barriers_data['total_valid_responses'] = total_valid_responses
            
            print(f"Processed {total_valid_responses} valid responses for female researcher career barriers")
            
            return barriers_data
            
        except Exception as e:
            print(f"Error processing barriers data: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def process_confidence_data(self, df):

        try:

            confidence_col = 114 
            gender_col = 18      
            
            if confidence_col >= len(df.columns) or gender_col >= len(df.columns):
                print(f"Error: Column index out of range. The dataset only has {len(df.columns)} columns.")
                return {}
        except Exception as e:
            print(f"Error setting up confidence data columns: {e}")
            return {}
            
        try:
            

            female_confidence_count = {}
            male_confidence_count = {}
            

            for i in range(4, len(df)):

                gender_value = str(df.iloc[i][gender_col]).strip().lower() if pd.notna(df.iloc[i][gender_col]) else ""
                is_female = "female" in gender_value or gender_value == "f"
                is_male = "male" in gender_value or gender_value == "m"

                if not (is_female or is_male):
                    continue
                    

                confidence_value = df.iloc[i][confidence_col]
                

                if pd.isna(confidence_value) or str(confidence_value).strip() == '':
                    continue
                    

                confidence_level = str(confidence_value).strip()
                

                if confidence_level.lower() in ['very confident', 'extremely confident']:
                    confidence_level = 'Very Confident'
                elif confidence_level.lower() in ['confident', 'fairly confident', 'quite confident']:
                    confidence_level = 'Confident'
                elif confidence_level.lower() in ['somewhat confident', 'moderately confident']:
                    confidence_level = 'Somewhat Confident'
                elif confidence_level.lower() in ['not very confident', 'slightly confident', 'a little confident']:
                    confidence_level = 'Not Very Confident'
                elif confidence_level.lower() in ['not confident', 'not at all confident']:
                    confidence_level = 'Not Confident'
                

                if is_female:
                    female_confidence_count[confidence_level] = female_confidence_count.get(confidence_level, 0) + 1
                elif is_male:
                    male_confidence_count[confidence_level] = male_confidence_count.get(confidence_level, 0) + 1
            

            confidence_order = [
                'Very Confident',
                'Confident',
                'Somewhat Confident',
                'Not Very Confident',
                'Not Confident'
            ]
            

            female_data = []
            for level in confidence_order:
                if level in female_confidence_count and female_confidence_count[level] > 0:
                    female_data.append({'name': level, 'value': female_confidence_count[level], 'gender': 'Female'})
            

            male_data = []
            for level in confidence_order:
                if level in male_confidence_count and male_confidence_count[level] > 0:
                    male_data.append({'name': level, 'value': male_confidence_count[level], 'gender': 'Male'})
            

            for level, count in female_confidence_count.items():
                if level not in confidence_order and count > 0:
                    female_data.append({'name': level, 'value': count, 'gender': 'Female'})
                    
            for level, count in male_confidence_count.items():
                if level not in confidence_order and count > 0:
                    male_data.append({'name': level, 'value': count, 'gender': 'Male'})
            

            confidence_data = {'confidenceLevel': female_data + male_data}
            

            print(f"Processed confidence data from column 115 by gender")
            print(f"Female confidence data: {len(female_data)} categories")
            print(f"Male confidence data: {len(male_data)} categories")
            
            return confidence_data
            
        except Exception as e:
            print(f"Error processing confidence data: {e}")
            import traceback
            traceback.print_exc()
            return {}