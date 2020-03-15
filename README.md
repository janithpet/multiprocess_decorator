# Multiprocess Decorators
Decorators that allow functions to be run using multiprocessing

This contains some decorators that will allow a function defined under it to run in a parallel fashion by forking multiple processes.

It is meant to remove boilerplate code when trying to do this; as such, the use cases might be limited. 
That being said, I have tried to write the different decorators to be as general as possible. 

As a first step, have a look at `tests/returnable.py`. Here we run a function that doubles a variable `x`. It is wrapped by a `joinable_returable_process_manager` and a `returnable_standard_worker`. When setting `joinable_returable_process_manager`, you can define the number of workers that will be run in parallel. These will automatically close once there aren't any tasks for them to complete.

To run the function, enter a list of arguments and keyword arguments; each element here will be constitute a single task. We see that we can run 12 tasks in about 2s when we use 10 processes.
