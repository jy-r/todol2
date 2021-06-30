# todol2


todol2 is a simple terminal-based to-do task manager and tracker. 
Tasks are saved in a JSON file named with the date of their creation, ensuring easy synchronisation among different devices.

![screenshot](https://user-images.githubusercontent.com/23253593/123917586-4070a780-d983-11eb-8b28-0141098117d1.png)

## Features

- `add [TEXT]` add new to-do task for today, for interactive mode use `add --f`
- `delete [ID]` delete a task with ID
- `done [ID]`/`undone [ID]` mark a task done/undone
- `edit [ID]` edit a message, deadline or tag of a task
- `p` print unfinished tasks, to print all regardless of their state use `p --all`
- `readd [ID]` add an older task into today's to-do list
- `search` search for tasks that contains `--word` or `--tag`
 
For more information see `--help` 

## Install 

```
git clone https://github.com/jy-r/todol2
cd todol2
pip install -e ./
```

Change the path in `todol2/todol/config.json` to the directory where to-do lists should be saved.
