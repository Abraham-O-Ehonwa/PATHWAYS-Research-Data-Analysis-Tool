import tkinter as tk
from ui_manager import UIManager
from data_loader import DataLoader
from data_visualizer import DataVisualizer

class ResearcherController:

    def __init__(self, root, csv_file):

        self.root = root
        self.root.title("Researcher Survey Visualization")
        self.root.geometry("1000x820")
        self.csv_file = csv_file
        
        self.COLORS = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#8884D8', '#82CA9D']
        

        self.data = None
        self.education_data = {}
        self.gender_employment_data = {}
        self.barriers_data = {}
        self.confidence_data = {}
        self.ALL_SUBJECTS = []
        

        self.ui_manager = UIManager(self.root, self)
        

        self.data_loader = DataLoader()
        

        self.data_visualizer = DataVisualizer(self.ui_manager.chart_frame, self.COLORS)
        

        self.sort_method = tk.StringVar(value="alphabetical")
        

        self.load_data()
        

        self.ui_manager.topic_type.set("Gender and Employment")
        self.update_topic_selection()

    def load_data(self):

        try:

            self.df = self.data_loader.load_csv(self.csv_file)
            

            self.data = self.data_loader.load_demographic_data(self.df)
            

            self.ALL_SUBJECTS, self.education_data = self.data_loader.load_education_data(self.df)
            

            self.gender_employment_data = self.data_loader.load_gender_employment_data(self.df)
            

            self.barriers_data = self.data_loader.process_barriers_data(self.df)
            

            self.confidence_data = self.data_loader.process_confidence_data(self.df)
            

            self.update_data_summary()
            
        except Exception as e:
            print(f"Error loading data: {e}")
            tk.Label(self.ui_manager.chart_frame, text=f"Error loading data: {e}", foreground="red").pack(pady=20)

    def update_data_summary(self):
        """Update the data summary displayed in the UI"""
        if not self.data:
            return
            

        valid_birth_years = [r['birthYear'] for r in self.data if r['birthYear'] is not None and 1900 <= r['birthYear'] <= 2025]
        min_year = min(valid_birth_years) if valid_birth_years else "N/A"
        max_year = max(valid_birth_years) if valid_birth_years else "N/A"
        
        summary_text = f"Total respondents: {len(self.data)} | Years represented: {min_year}-{max_year}"
        self.ui_manager.data_summary.config(text=summary_text)

    def update_topic_selection(self, event=None):
        """Handle topic selection changes from the UI"""
        topic = self.ui_manager.topic_type.get()
        

        self.ui_manager.update_topic_ui(topic)
        

        self.update_chart()

    def update_data_type(self, event=None):
        """Handle data type selection changes"""
        self.update_chart()
    
    def update_education_data(self, event=None):
        """Handle education data type selection changes"""
        for widget in self.ui_manager.chart_frame.winfo_children():
            widget.destroy()
            
        education_type = self.ui_manager.data_type.get()
        
        if education_type in self.education_data and self.education_data[education_type]:

            self.ui_manager.chart_combo['values'] = ('bar', 'line', 'pie')
            self.update_chart()
        else:
            tk.Label(self.ui_manager.chart_frame, text=f"No data available for {education_type}").pack(pady=20)
    
    def update_gender_employment_data(self, event=None):
        """Handle gender employment data type selection changes"""
        for widget in self.ui_manager.chart_frame.winfo_children():
            widget.destroy()
            
        data_type = self.ui_manager.data_type.get()
        
        if data_type in self.gender_employment_data and self.gender_employment_data[data_type]:

            self.ui_manager.chart_combo['values'] = ('bar', 'pie')
            

            if self.ui_manager.chart_type.get() == 'line':
                self.ui_manager.chart_type.set('bar')
                
            self.update_chart()
        else:
            tk.Label(self.ui_manager.chart_frame, text=f"No data available for {data_type}").pack(pady=20)

    def get_chart_data(self):
        """Get the data for the currently selected chart"""
        if not hasattr(self.ui_manager, 'data_type'):
            return []
            
        topic = self.ui_manager.topic_type.get()
        data_type = self.ui_manager.data_type.get()
        

        if topic == "Demographic" and self.data:
            return self.data_loader.get_demographic_chart_data(self.data, data_type)
        

        elif topic == "Education":
            education_type = data_type
            if education_type in self.education_data:
                return [item for item in self.education_data[education_type] if item['value'] > 0]
        

        elif topic == "Gender and Employment":
            if data_type in self.gender_employment_data:
                return self.gender_employment_data[data_type]
                

        elif topic == "Barriers to Career Goals":
            if data_type == 'career_barriers' and 'career_barriers' in self.barriers_data:
                return self.barriers_data['career_barriers']
                

        elif topic == "Confidence in Achieving Career Goals":
            if data_type == 'confidenceLevel' and 'confidenceLevel' in self.confidence_data:
                return self.confidence_data['confidenceLevel']
        
        return []
        
    def get_chart_title(self):
        """Get the title for the current chart"""
        if not hasattr(self.ui_manager, 'data_type'):
            return 'Survey Data'
            
        topic = self.ui_manager.topic_type.get()
        data_type = self.ui_manager.data_type.get()
        

        if topic == "Demographic":
            if data_type == 'children':
                return 'Number of Respondents by Children Ever Born'
            elif data_type == 'birthYear':
                return 'Number of Respondents by Birth Year'
            elif data_type == 'maritalStatus':
                return 'Marital Status Distribution'
            elif data_type == 'disability':
                return 'Disability Status Distribution'
            elif data_type == 'doctoralYear':
                return 'Number of Respondents by Doctoral Start Year'
        

        elif topic == "Education":
            if data_type == 'undergraduate_subjects':
                return 'Undergraduate Subject Areas'
            elif data_type == 'masters':
                return 'Masters Subject Areas'
            elif data_type == 'doctoral':
                return 'Doctoral Subject Areas'
        

        elif topic == "Gender and Employment":
            if data_type == 'fulltime_by_gender':
                return 'Percentage of Full-Time Employment by Gender'
            elif data_type == 'fixed_term_by_gender':
                return 'Percentage with Fixed-Term Contracts by Gender'
                

        elif topic == "Barriers to Career Goals":
            return 'Barriers to Career Goals for Female Researchers'
            

        elif topic == "Confidence in Achieving Career Goals":
            return 'Confidence in Achieving Research Career Goals'
        
        return 'Survey Data'
        
    def update_chart(self, event=None):
        """Update the visualization based on current selections"""

        for widget in self.ui_manager.chart_frame.winfo_children():
            widget.destroy()
            

        if not hasattr(self.ui_manager, 'data_type') or not self.ui_manager.topic_type.get():
            tk.Label(self.ui_manager.chart_frame, text="Please select a topic and data type to view visualization").pack(pady=20)
            return
        
        chart_data = self.get_chart_data()
        if not chart_data:
            tk.Label(self.ui_manager.chart_frame, text="No data available for this selection").pack(pady=20)
            return
            

        chart_type = self.ui_manager.chart_type.get()
        

        if self.ui_manager.topic_type.get() == "Barriers to Career Goals":
            chart_type = "bar"
            

        title = self.get_chart_title()

        self.data_visualizer.create_chart(
            chart_data, 
            chart_type, 
            title, 
            self.ui_manager.topic_type.get(),
            self.ui_manager.color_frame
        )