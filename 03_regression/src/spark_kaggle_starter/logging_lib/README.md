<h1> Logging Library </h1>

<b>Summary</b>: This package is designed to make logging easy and clean from an environment where one isn't watching a terminal screen for the output and doesn't want to deal with ugly stdout (for example: using steps to submit jobs on AWS EMR). This library will allow one to log both strings and matplotlib images during execution. After one sees that all their jobs has finished they can run another function to create markdown files with all the logs and plots ordered. S3 is used as a storage solution for this library.

<h1>Code examples</h1>

<h2>LoggingController</h2>

<b>Summary</b>: This class should be instantiated once and only once from the spark or other application you'd like to log from.

| Required parameters for LoggingController |
|---|
| profile_name: Define IAM profile name ('aws configure' cli command uses 'default')(see: http://boto3.readthedocs.io/en/latest/guide/configuration.html)  |
| s3_bucket: S3 Bucket to use for storage |

<b>Usage:</b> the function log_string() will log a string value. The function log_matplotlib_plot() will take a matplotlib plot and export the image and display it inline on your markdown file.

<b>[Code:](LoggingController.py)</b>
```
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
N = 5
menMeans = (20, 35, 30, 35, 27)
womenMeans = (25, 32, 34, 20, 25)
menStd = (2, 3, 4, 1, 2)
womenStd = (3, 5, 2, 3, 3)
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence
p1 = plt.bar(ind, menMeans, width, color='#d62728', yerr=menStd)
p2 = plt.bar(ind, womenMeans, width,
             bottom=menMeans, yerr=womenStd)
plt.ylabel('Scores')
plt.title('Scores by group and gender')
plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
plt.yticks(np.arange(0, 81, 10))
plt.legend((p1[0], p2[0]), ('Men', 'Women'))


from LoggingController import LoggingController
controller = LoggingController()
controller.profile_name = 'default'
controller.s3_bucket = 'emr-related-files'
controller.log_string('first')
controller.log_matplotlib_plot(plt)
controller.log_string('third')
```

<h2>MarkdownBuilder</h2>

<b>Usage:</b> Run this code after all your steps have been completed on the EMR cluster to save built logs both locally and on S3 as a backup. Note: if you run this while any jobs are partially complete you will have a partially built log file and will have to manually repair it (no data will be lost, however. Data is only moved on S3 never deleted.)

| Required parameters for MarkdownBuilder |
|---|
| profile_name: Define IAM profile name ('aws configure' cli command uses 'default')(see: http://boto3.readthedocs.io/en/latest/guide/configuration.html) |
| s3_bucket: S3 Bucket to use for storage |
| path_to_save_logs_local: A path to save all the built logs on your local machine. |

<b>[Code:](MarkdownBuilder.py)</b>
```
from MarkdownBuilder import MarkdownBuilder
builder = MarkdownBuilder()
builder.profile_name = 'default'
builder.s3_bucket = 'emr-related-files'
builder.path_to_save_logs_local = 'logs'
builder.build_markdowns()

```
<h1>Additional Considerations</h1>

<b>Gotcha</b> You will need to set this specific mathplotlib command after importing and before generating a plot to avoid a display error. This is because servers don't have a display attached to show the plots.

```
import matplotlib
matplotlib.use('Agg')
```
