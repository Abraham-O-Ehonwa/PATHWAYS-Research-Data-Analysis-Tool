import tkinter as tk
from tkinter import ttk

class UIManager:

    def __init__(self, root, controller):

        self.root = root
        self.controller = controller
        

        self.setup_ui()
        
    def setup_ui(self):

        self.control_frame = ttk.Frame(self.root, padding="10")
        self.control_frame.pack(fill=tk.X)
        

        ttk.Label(self.control_frame, text="Topic").grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.topic_type = tk.StringVar(value="")
        self.topic_combo = ttk.Combobox(self.control_frame, textvariable=self.topic_type)
        self.topic_combo['values'] = ('Demographic', 'Education', 'Gender and Employment', 'Barriers to Career Goals', 
                                    'Confidence in Achieving Career Goals')
        self.topic_combo.grid(column=1, row=0, padx=5, pady=5)
        self.topic_combo.bind('<<ComboboxSelected>>', self.controller.update_topic_selection)
        

        ttk.Label(self.control_frame, text="Chart Type").grid(column=2, row=0, sticky=tk.W, padx=5, pady=5)
        self.chart_type = tk.StringVar(value="bar")
        self.chart_combo = ttk.Combobox(self.control_frame, textvariable=self.chart_type)
        self.chart_combo['values'] = ('bar', 'line', 'pie')
        self.chart_combo.grid(column=3, row=0, padx=5, pady=5)
        self.chart_combo.bind('<<ComboboxSelected>>', self.controller.update_chart)
        

        self.chart_frame = ttk.Frame(self.root, padding="10")
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        

        info_frame = ttk.LabelFrame(self.root, text="About the Data", padding="10")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info_text = "This visualization shows data from a survey of female researchers in Ireland."
        
        ttk.Label(info_frame, text=info_text, wraplength=780).pack(pady=5)
        

        self.data_summary = ttk.Label(info_frame, text="")
        self.data_summary.pack(pady=5)
        

        self.color_frame = ttk.Frame(info_frame)
        self.color_frame.pack(pady=5)

    def update_topic_ui(self, topic):


        for widget in self.control_frame.grid_slaves(row=1):
            widget.grid_forget()
        

        for widget in self.control_frame.grid_slaves(row=2):
            widget.grid_forget()
        

        if topic == "Demographic":
            ttk.Label(self.control_frame, text="Demographic Data").grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
            self.data_type = tk.StringVar(value="children")
            self.demographic_combo = ttk.Combobox(self.control_frame, textvariable=self.data_type)
            self.demographic_combo['values'] = ('children', 'birthYear', 'maritalStatus', 'disability', 'doctoralYear')
            self.demographic_combo.grid(column=1, row=1, columnspan=3, sticky=tk.W, padx=5, pady=5)
            self.demographic_combo.bind('<<ComboboxSelected>>', self.controller.update_data_type)
            
        elif topic == "Education":
            ttk.Label(self.control_frame, text="Education Data").grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
            self.data_type = tk.StringVar(value="undergraduate_subjects")
            self.education_combo = ttk.Combobox(self.control_frame, textvariable=self.data_type)
            self.education_combo['values'] = ('undergraduate_subjects', 'masters', 'doctoral')
            self.education_combo.grid(column=1, row=1, columnspan=3, sticky=tk.W, padx=5, pady=5)
            self.education_combo.bind('<<ComboboxSelected>>', self.controller.update_education_data)
            
        elif topic == "Gender and Employment":
            ttk.Label(self.control_frame, text="Gender and Employment Data").grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
            self.data_type = tk.StringVar(value="fulltime_by_gender")
            self.gender_employment_combo = ttk.Combobox(self.control_frame, textvariable=self.data_type)
            self.gender_employment_combo['values'] = ('fulltime_by_gender', 'fixed_term_by_gender')
            self.gender_employment_combo.grid(column=1, row=1, columnspan=3, sticky=tk.W, padx=5, pady=5)
            self.gender_employment_combo.bind('<<ComboboxSelected>>', self.controller.update_gender_employment_data)
            
        elif topic == "Barriers to Career Goals":

            self.data_type = tk.StringVar(value="career_barriers")
            

            self.chart_combo['values'] = ('bar',)  
            if self.chart_type.get() != 'bar':
                self.chart_type.set('bar')
            
        elif topic == "Confidence in Achieving Career Goals":

            self.data_type = tk.StringVar(value="confidenceLevel")
            

            self.chart_combo['values'] = ('bar', 'line', 'pie')