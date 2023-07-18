import matplotlib.pyplot as plt

# Plotting graph
def plot_graph(num_positive, num_negative, num_neutral):
    fig, ax = plt.subplots()
    bar = ax.bar(['Positive', 'Negative', 'Neutral'], [num_positive, num_negative, num_neutral], width = 0.5, align = 'center', color='#FAFAFA')
    ax.set_title('Sentiment Analysis')
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Count')
    ax.set_facecolor('#0E1117')
    ax.tick_params(axis='x', colors='#0E1117') 
    ax.tick_params(axis='y', colors='#0E1117') 
    for rect in bar:
        height = rect.get_height()
        ax.annotate(f'{height}', xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', va='bottom', color = '#FAFAFA', fontsize = 8)
        
    return fig

# Driver function
def execute(num_positive, num_negative, num_neutral):
    graph = plot_graph(num_positive, num_negative, num_neutral)
    return graph