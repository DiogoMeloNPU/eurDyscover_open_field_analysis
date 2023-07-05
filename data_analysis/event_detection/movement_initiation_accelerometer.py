# to access the general use module you need to add the parent folder to the path
import sys
sys.path.append("C:\\Users\\Administrador\\DystoniaAnalysis")

# import module with functions to access database
import general_use_functions as guf

# load dystonia database
dystonia_database = guf.load_dystonia_database()
print(dystonia_database)

# access all acceleration files
print(dystonia_database[''])




# establish a treshold for movement initiation using acceleration (accelerometer palced in the head)

# study the distribution of acceleration within session and across sessions

# load dystonia database


# across session and take the mean 

    # single plot with all sessions in a specific time point overlayed in the same plot

    # check mean

# join all values from all files and check disctribution (what could we consider if there was a clear binomial distribution? could we use that treshold?)


# try opening one of the created files with values and timestamps and plot 