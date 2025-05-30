df.set_index('date')['headline'].resample('D').count().plot()
plt.title('Daily Article Publication Frequency')
plt.ylabel('Article Count')
plt.show()