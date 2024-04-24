# Marketing Campaign Analysis Using Clustering Techniques

## Overview
This project applies various clustering techniques to analyze customer data from a marketing campaign. It demonstrates the preprocessing, feature engineering, dimensionality reduction, and clustering steps using Python libraries such as Pandas, NumPy, Scikit-Learn, Seaborn, and Yellowbrick.

## Repository Contents
- **marketing_campaign.csv**: Dataset containing the marketing campaign's customer data.
- **analysis_script.py**: Python script for the entire analysis, from data loading to clustering.

## Installation
To run this project, you will need Python and several libraries installed:

1. **Clone the Repository:**
   ```
   git clone https://github.com/your-username/marketing-campaign-clustering.git
   cd marketing-campaign-clustering
   ```

2. **Install Required Libraries**:
   Install the required Python libraries by running:
   ```
   pip install pandas numpy matplotlib seaborn scikit-learn yellowbrick kmodes
   ```

## Usage
- **Data Loading and Cleaning**: The dataset is loaded into a DataFrame, unnecessary columns are removed, and data types are converted appropriately.
- **Feature Engineering**: New features like total spending and days of customer engagement are created.
- **Data Visualization**: Data distributions and relationships are visualized using pair plots and correlation heatmaps.
- **Dimensionality Reduction**: PCA is applied to reduce the dimensions of the dataset while capturing the essential features.
- **Clustering**: Multiple clustering methods (K-Means, Agglomerative Clustering, and DBSCAN) are used to segment the customer base. The optimal number of clusters is determined using the Elbow method visualized with Yellowbrick.

## Key Features
- **Data Preprocessing**: Handling missing values, removing outliers, and encoding categorical features.
- **Data Normalization**: Standardizing the data to prepare for clustering.
- **Cluster Analysis**: Analyzing and visualizing the clusters to uncover insights about different customer segments.

## Detailed Steps
1. **Preprocessing**: The script starts by loading the data and performing initial exploratory data analysis to understand the dataset's structure and content.
2. **Feature Engineering**: Enhancements and modifications to the dataset to better reflect potential customer segments.
3. **Clustering Preparation**: Data is scaled, and dimensionality is reduced using PCA to facilitate more effective clustering.
4. **Clustering Execution**: The dataset is clustered using different algorithms. Each method's results are visualized and analyzed to determine the most meaningful customer segmentation.
5. **Results Visualization**: Clusters are plotted using 3D scatter plots to visualize the segmentation in the reduced dimensional space.

## Running the Script
Execute the script from your command line by navigating to the project directory and running:
```
python analysis_script.py
```

## Contributing
Contributions to this project are welcome! If you have suggestions for improving the analysis or encounter any issues, please feel free to fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

