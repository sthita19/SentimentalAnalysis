import matplotlib.pyplot as plt

def plot_graph(sentiment_percentages, non_zero_word_count):
    labels_sentiment = sentiment_percentages.keys()
    sizes_sentiment = sentiment_percentages.values()

    labels_word = non_zero_word_count.keys()
    sizes_word = non_zero_word_count.values()

    # Create 2 Subplots
    fig_bar , (ax1_bar, ax2_bar) = plt.subplots(1, 2)

    fig_bar.set_size_inches(5,3)

    # Plot the First Bar Graph
    bar1 = ax1_bar.bar(labels_sentiment, sizes_sentiment, width = 0.6, align = 'center', color='#FAFAFA')
    ax1_bar.set_facecolor('#0E1117') 
    ax1_bar.tick_params(axis='x', colors='#0E1117')
    ax1_bar.tick_params(axis='y', colors='#0E1117')  
    ax1_bar.set_xticks(range(len(labels_sentiment)))
    ax1_bar.set_xticklabels(labels_sentiment, rotation = 45, ha = 'right')
    ax1_bar.set_ylabel('Percentage')
    ax1_bar.set_xlabel('Words')
    ax1_bar.set_title('Sentiment Percentages')

    # Add values on top of the bars in the first bar graph
    for rect in bar1:
        height = rect.get_height()
        ax1_bar.annotate(f'{height:.2f}%', xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', va='bottom', color = '#FAFAFA', fontsize = 5)

    # Plot the Second Bar Graph
    bar2 = ax2_bar.bar(labels_word, sizes_word, width = 0.5, align = 'center', color='#FAFAFA')
    ax2_bar.set_facecolor('#0E1117')  
    ax2_bar.tick_params(axis='x', colors='#0E1117')  
    ax2_bar.tick_params(axis='y', colors='#0E1117') 
    ax2_bar.set_xticks(range(len(labels_word)))
    ax2_bar.set_xticklabels(labels_word, rotation = 45, ha = 'right')
    ax2_bar.set_ylabel('Percentage')
    ax2_bar.set_xlabel('Sentiment')
    ax2_bar.set_title('Word Count')

    # Add values on top of the bars in the second bar graph
    for rect in bar2:
        height = rect.get_height()
        ax2_bar.annotate(f'{height}', xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', va='bottom', color = '#FAFAFA', fontsize = 5)
        
    plt.subplots_adjust(wspace=0.5)
    return fig_bar

# Driver function
def execute(sentiment_percentages, non_zero_word_count):
    bar_graph = plot_graph(sentiment_percentages, non_zero_word_count)
    return bar_graph