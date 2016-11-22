# Visualization Resources

## Some visualization guidelines 

#### Preface

A fundamental consideration for any visualization is the target audience, specifically what they already know about the topic to be visualized, and what they want to know. Having a clear understanding of these two notions will assist in creating a visual analysis that is interesting, comprehensible and free of bias. To ensure the visualization is understandable for the audience, consider whether the data and message of the visualization are better suited for a more immediately recognizable form of static chart or graph, or a more complex, interactive or animated visualization. For many types of quantitative visual communications, a line graph, bar chart, scatter plot or pie chart is preferable. When choosing to forgo the familiarity of these standards, there must be a significant reward for the audience. Knowing the purpose of the visualization can be immensely helpful in resolving the accessibility versus complexity tradeoff. Generally, visualizations meant for presentation should be more directly recognizable, with only a small number of highlighted visual narratives. Conversely, visualizations and visual apps meant for exploration and discovery may be highly complex, interactive, animated or any combination thereof. When choosing to construct an interactive visual app, the interactive functionality should support the audience’s analytic goals. Common interactive capabilities the audience may expect include: selecting data, reorganizing data, zooming and data filtering. Animation in visualization is typically used for multi-dimensional analyses involving time, to increase audience engagement, or to emphasize trends, patterns or outliers. Two dimensional problem domains with time as the independent variable can typically be expressed clearly using a static line chart. The method of Small Multiples, or a series of small charts having similar axes within the same larger graphic, is often employed for multi-dimensional analysis where animation may be inappropriate.

Accuracy and engagement are also important aspects of purpose. If the infographic is meant to display the analyzed data as accurately as possible, care should be taken to ensure all graphic attributes are to scale, that aesthetic
complexity is uniform throughout the image(s), and that all information contained in the data, or an explicitly defined subset, is displayed. If the purpose of the visualization is to increase or motivate the audience’s engagement with the portrayed data or topic, then a less rigorous and more aesthetically focused approach may be warranted, provided any artistic distortions to the character of the data are noted. While many enhancement techniques and effects can be applied to digital images at an analyst’s discretion, simply dropping less critical information from a visualization and increasing the aesthetic detail of more critical information can suffice to increase audience ngagement.

Below are a few good rules for not confusing your audience. 

#### Keep dimensionality as low as possible

* Keep dimensionality low, both in terms of audience perspective and data dimensions. 
* Avoid 3-D plots except when natural or intuitive to the data, and do not attempt to display more than seven variables within the same visualization. 
* Even when displaying a smaller number of variables, the combination of hue, luminance, and texture (e.g. size, orientation or dot density) for attributes must be carefully chosen to maximize visual differences between dissimilar data records. 
* The small multiples technique can aid in clearly displaying several variables in the same image.	
 	
#### Keep axes honest 

* In an already complex visualization, tampering with audience expectations of scale is typically undesirable. 
* Inconsistent ranges for the axes of small multiples are a common source of data misinterpretation.	
 	
#### Color and texture are easily recognizable for most audience members. 

* When choosing how to communicate different types of information about a given attribute in an image, the easiest variations for most audience members to recognize visually are, in order:
  * Color Hue
  * Color Luminance
  * Texture (e.g. Size, Orientation or Dot Density)

* Although hue attribute differences tend to be the most immediately distinguishable, schemes including red and green may cause difficulty for red-green color blind audience members.	
 	
#### Avoid Common Visual Pratfalls. 

* Both general audience members and analysts are susceptible to limited memory for visual detail and limited attentional focus, known as Change Blindness and Inattentional Blindness respectively. 
  * Change Blindness can occur when users experience difficulty in making analytical decisions based on graphics on separate pages or in separate windows. 
  * Inattentional Blindness can occur when a user’s full attention is fully deployed on a demanding task within a visualization, and they fail to notice other important features.

###### Source: http://support.sas.com/resources/papers/proceedings12/275-2012.pdf

## Common visualization libraries

* [d3 (Javascript)](https://d3js.org/)
* [matplotlib (Python)](http://matplotlib.org/)
* [ggplot2 (R)](https://cran.r-project.org/web/packages/ggplot2/)
* [shiny (R)](https://cran.r-project.org/web/packages/shiny/)

#### List of libraries and other resources
[awesome-dataviz](https://github.com/fasouto/awesome-dataviz)

## Data visualization galleries

#### d3
* [Block](https://bl.ocks.org/)
* [d3 gallery](https://github.com/d3/d3/wiki/Gallery)

#### R
* [R graph gallery](http://www.r-graph-gallery.com/)
* [Shiny gallery](http://shiny.rstudio.com/gallery/)

## Free visualization apps 

* [Google Trends - Search terms over time](http://www.google.com/trends/)
* [Statsilk - Maps and other data visualization](http://www.statsilk.com/)
* [Raw - Web visualizations from CSV or Excel files](http://raw.densitydesign.org/)
* [Color Brewer - Color advice for maps](http://colorbrewer2.org/)
* [Wordle - Word clouds](http://www.wordle.net/)
* [Gephi - Visualizing complex networks](http://gephi.github.io/)
* [Circos - Circular format plots](http://circos.ca/software/)

## Sites for inspiration

* [FlowingData](http://flowingdata.com/)
* [Jer Thorpe's blprnt blog](http://blog.blprnt.com/)
* [Information is Beautiful](http://www.informationisbeautiful.net/)
* [The NYT Upshot](http://www.nytimes.com/section/upshot)
* [The Data Visualization Catalogue](http://www.datavizcatalogue.com/)