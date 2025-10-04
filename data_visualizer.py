import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataVisualizer:

    def __init__(self, chart_frame, colors):

        self.chart_frame = chart_frame
        self.COLORS = colors
        

        plt.style.use('ggplot')
        
    def create_color_legend(self, color_frame, num_colors):

        for widget in color_frame.winfo_children():
            widget.destroy()
        
        for i in range(min(num_colors, len(self.COLORS))):
            color_box = ttk.Frame(color_frame, width=15, height=15)
            color_box.grid(row=0, column=i*2, padx=2)
            color_box.configure(style=f"Color{i}.TFrame")
            
            style = ttk.Style()
            style.configure(f"Color{i}.TFrame", background=self.COLORS[i])
            
            ttk.Label(color_frame, text=f"Data {i+1}").grid(row=0, column=i*2+1, padx=2)
    
    def create_chart(self, chart_data, chart_type, title, topic_type, color_frame):


        fig, ax = plt.subplots(figsize=(10, 8), dpi=100)
        

        if topic_type == "Confidence in Achieving Career Goals":
            self._create_confidence_chart(fig, ax, chart_data)
        else:

            names = [item['name'] for item in chart_data]
            values = [item['value'] for item in chart_data]

            colors = [self.COLORS[i % len(self.COLORS)] for i in range(len(names))]
            

            if chart_type == 'bar':
                self._create_bar_chart(ax, names, values, colors, topic_type)
            elif chart_type == 'line':
                self._create_line_chart(ax, names, values, colors, topic_type)
            elif chart_type == 'pie':
                self._create_pie_chart(ax, names, values, colors)
        

        plt.title(title, fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        

        if topic_type != "Confidence in Achieving Career Goals":
            self.create_color_legend(color_frame, min(len(names), 8))
        
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _create_confidence_chart(self, fig, ax, chart_data):

        unique_levels = sorted(set([item['name'] for item in chart_data]), 
                            key=lambda x: ['Very Confident', 'Confident', 'Somewhat Confident', 
                                            'Not Very Confident', 'Not Confident'].index(x) 
                                    if x in ['Very Confident', 'Confident', 'Somewhat Confident', 
                                            'Not Very Confident', 'Not Confident'] else 999)
        
        female_data = [item for item in chart_data if item['gender'] == 'Female']
        male_data = [item for item in chart_data if item['gender'] == 'Male']
        
        female_values = []
        male_values = []
        
        for level in unique_levels:
            female_match = next((item for item in female_data if item['name'] == level), None)
            male_match = next((item for item in male_data if item['name'] == level), None)
            
            female_values.append(female_match['value'] if female_match else 0)
            male_values.append(male_match['value'] if male_match else 0)
        
        x = np.arange(len(unique_levels))
        width = 0.35
        
        bar1 = ax.bar(x - width/2, female_values, width, label='Female', color=self.COLORS[0])
        bar2 = ax.bar(x + width/2, male_values, width, label='Male', color=self.COLORS[1])
        
        ax.set_xticks(x)
        ax.set_xticklabels(unique_levels)
        ax.legend()
        
        for i, v in enumerate(female_values):
            if v > 0:
                ax.text(i - width/2, v, str(v), ha='center', va='bottom', fontweight='bold')
        
        for i, v in enumerate(male_values):
            if v > 0:
                ax.text(i + width/2, v, str(v), ha='center', va='bottom', fontweight='bold')
                
        ax.set_xlabel('Confidence Level', fontweight='bold')
        ax.set_ylabel('Number of Respondents', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
    
    def _create_bar_chart(self, ax, names, values, colors, topic_type):


        bars = ax.bar(names, values, color=colors)
        

        ax.set_xlabel('Category', fontweight='bold')
        

        if topic_type == "Barriers to Career Goals":
            ax.set_ylabel('Percentage (%)', fontweight='bold')
            ax.set_ylim(0, 50)
            ax.set_yticks([0, 10, 20, 30, 40, 50])
        else:
            ax.set_ylabel('Value', fontweight='bold')
            

        plt.xticks(rotation=45, ha='right')
        

        for i, v in enumerate(values):

            if topic_type == "Barriers to Career Goals":
                ax.text(i, v, f"{v}%", ha='center', va='bottom', fontweight='bold')
            else:
                ax.text(i, v, str(v), ha='center', va='bottom', fontweight='bold')
    
    def _create_line_chart(self, ax, names, values, colors, topic_type):


        if topic_type != "Education":
            sorted_data = sorted(zip(names, values, colors))
            plot_names = [item[0] for item in sorted_data]
            plot_values = [item[1] for item in sorted_data]
            plot_colors = [item[2] for item in sorted_data]
        else:
            plot_names = names
            plot_values = values
            plot_colors = colors
        

        ax.plot(range(len(plot_values)), plot_values, marker='o', linestyle='-', linewidth=2, color=plot_colors[0])
        

        ax.set_xticks(range(len(plot_names)))
        ax.set_xticklabels(plot_names)
        

        ax.grid(True, linestyle='--', alpha=0.7)
        

        ax.set_xlabel('Category', fontsize=12, fontweight='bold')
        

        if topic_type == "Barriers to Career Goals":
            ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')

            ax.set_ylim(0, 100)
            ax.set_yticks([0, 20, 40, 60, 80, 100])
        else:
            ax.set_ylabel('Value', fontsize=12, fontweight='bold')
            

        plt.xticks(rotation=45, ha='right')
        

        if min(plot_values) >= 0 and topic_type != "Barriers to Career Goals":
            ax.set_ylim(bottom=0)
    
    def _create_pie_chart(self, ax, names, values, colors):

        if len(names) > 10:
            sorted_data = sorted(zip(names, values, colors), key=lambda x: x[1], reverse=True)
            
            top_names = [item[0] for item in sorted_data[:9]]
            top_values = [item[1] for item in sorted_data[:9]]
            top_colors = [item[2] for item in sorted_data[:9]]
            
            other_value = sum(item[1] for item in sorted_data[9:])
            if other_value > 0:
                top_names.append("Other")
                top_values.append(other_value)
                top_colors.append('#999999') 
            
            names = top_names
            values = top_values
            colors = top_colors
        
        ax.pie(
            values, 
            labels=names, 
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'fontsize': 9}
        )
        ax.axis('equal')