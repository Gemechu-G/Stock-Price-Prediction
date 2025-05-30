import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import gridspec

def plot_correlation_heatmap(df, score_col='rating_score', price_col='price_change'):
    """Plot correlation matrix between sentiment and price features"""
    corr = df[[score_col, price_col, 'volume']].corr()
    
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0,
                annot_kws={'size':12}, vmin=-1, vmax=1)
    plt.title('Feature Correlation Matrix')
    plt.tight_layout()
    plt.savefig('../figures/correlation_heatmap.png')
    return plt

def plot_rating_impact(df, ticker='AAPL'):
    """Plot typical price impact pattern for a given stock"""
    fig = plt.figure(figsize=(14,6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3,1])
    
    # Time series plot
    ax0 = plt.subplot(gs[0])
    for score, group in df.groupby('rating_score'):
        group.groupby('days_from_rating')['close'].mean().plot(
            ax=ax0, label=f'Score={score:.2f}')
    
    ax0.axvline(0, color='black', linestyle='--')
    ax0.set_title(f'{ticker} Typical Price Impact by Rating Score')
    ax0.set_xlabel('Days Relative to Rating')
    ax0.set_ylabel('Normalized Price')
    ax0.legend()
    
    # Bar plot
    ax1 = plt.subplot(gs[1])
    df.groupby('rating_score')['price_change'].mean().plot.bar(ax=ax1)
    ax1.set_title('Average 5-day Return')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
    
    plt.tight_layout()
    plt.savefig(f'../figures/{ticker}_impact.png')
    return plt