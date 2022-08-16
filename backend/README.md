# Backend connection
To run the backend connection without processing the frame can achieved by running
```shell
node ./backend/server.js <in_path> <out_path> <total_frames> <batch_size> [start_frame]
```

| ARGS | Details |
| :--- | :--- |
| in_path | the input directory or the latex file directory. Use full path. Ex: __/mnt/d/Documents/Project05/out_latex/default__
| out_path | the output png directory. Use full path. Ex : __/mnt/d/Documents/Project05/out_png/default__
| total_frames | total frames that want to be rendered in desmos |
| batch_size | total block of latex file that sent to the front end |
| start_frame(optional) | Specify which frame is the starting frame. Default is 1.|

## Notes : Please make sure directory specify in in_path and out_path exist. If not, error will occur. 
