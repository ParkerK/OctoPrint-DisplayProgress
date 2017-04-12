# OctoPrint-DisplayProgress

Displays the print progress on the printer's display.

![Example](http://i.imgur.com/F4m2QlB.jpg)

![Settings](https://i.imgur.com/j1ZCnEm.png)

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/OctoPrint/OctoPrint-DisplayProgress/archive/master.zip

## Configuration

You can customize the progress bar characters and preview the styling from the plugin settings page.

You can also configure it directly by modifying the `yaml` file
``` yaml
plugins:
  displayprogress:
    # The message to display. Placeholders:
    # - bar: a progress bar, e.g. [######    ]
    # - progress: the current progress as an integer between 1 and 100
    message: '{bar} {progress:>3}%%'
```
