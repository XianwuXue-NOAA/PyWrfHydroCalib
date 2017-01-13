# Main calling program to initiate a spinup for calibration of the National
# Water Model. This program can either be used to initiate or restart a 
# spinup if it has crashed unexpectedly. The user will need to provide 
# a unique Job ID that is stored in the database.

# Logan Karsten
# National Center for Atmospheric Research
# Research Applications Laboratory
# karsten@ucar.edu
# 303-497-2693

import sys
import argparse
#import getpass
import os
#import subprocess
#import pandas as pd
import pwd

# Set the Python path to include package specific functions.
sys.path.insert(0,'./lib/Python')

import warnings
warnings.filterwarnings("ignore")

import statusMod
import dbMod
#import errMod
#import calibIoMod

def main(argv):
    # Parse arguments. User must input a job name.
    parser = argparse.ArgumentParser(description='Main program to start or restart ' + \
             'calibration spinup for the National Water Model')
    parser.add_argument('jobID',metavar='jobID',type=str,nargs='+',
                        help='Job ID specific to calibration spinup.')
    
    args = parser.parse_args()
    
    # Get current user who is running this program.
    userTmp = pwd.getpwuid(os.getuid()).pw_name
    
    # Initialize object to hold status and job information
    jobData = statusMod.statusMeta()
    jobData.jobID = args.jobID
    
    # Lookup database username/login credentials based on username
    # running program.
    #try:
    #    uNameTmp = raw_input('Enter Database Username: ')
    #    pwdTmp = getpass.getpass('Enter Database Password: ')
    #    jobData.dbUName= str(uNameTmp)
    #    jobData.dbPwd = str(pwdTmp)
    #except:
    #    print "ERROR: Unable to authenticate credentials for database."
    #    sys.exit(1)
    
    jobData.dbUName = 'NWM_Calib_rw'
    jobData.dbPwd = 'IJustWannaCalibrate'    
    # Establish database connection.
    db = dbMod.Database(jobData)
    try:
        db.connect(jobData)
    except:
        print jobData.errMsg
        sys.exit(1)
        
    # Extract job data from database
    db.jobStatus(jobData)
    #try:
    #    db.jobStatus(jobData)
    #except:
    #    print jobData.errMsg
    #    sys.exit(1)
    
    print jobData.jobID
    print jobData.jobDir
    print jobData.nGages
    print jobData.gages
    print jobData.gageIDs
    print jobData.bSpinDate
    print jobData.eSpinDate
    print jobData.spinComplete
    print jobData.bCalibDate
    print jobData.eCalibDate
    print jobData.calibIter
    print jobData.calibComplete
    print jobData.bValidDate
    print jobData.eValidDate
    print jobData.validComplete
    print jobData.nIter
    print jobData.nCores
    print jobData.acctKey
    print jobData.exe
    print jobData.errMsg
    print jobData.dbUName
    print jobData.dbPwd
    print jobData.owner
    print jobData.email
    print jobData.slChan
    print jobData.slToken
    print jobData.slUser
    
    ## Check gages in directory to match what's in the database
    #jobData.checkGages(db)
    
    ## Extract active jobs for job owner
    #calibIoMod.checkYsJobs(jobData)
    
    ## Some house keeping here. If the spinup is already complete, throw an error. 
    ## also, if this is a re-initiation under a different user, require the new
    ## user to enter a new contact that will be unpdated in the database. 
    #if int(jobData.spinComplete) == 1:
    #    jobData.errMsg = "ERROR: Spinup for job ID: " + str(jobData.jobID) + \
    #                     " has already completed."
    #    errMod.errOut(jobData)
        
    #if userTmp != jobData.owner:
    #    print "User: " + userTmp + " is requesting to takeover jobID: " + \
    #          str(jobData.jobID) + " from owner: " + str(jobData.owner)
    #    strTmp = "Please enter new email/Slack conact (LEAVE BLANK IF " + \
    #             "NO CHANGE IN CONTACT DESIRED)"
    #    newContact = raw_input(strTmp)
    #    if len(newContact) == 0:
    #        newContact = str(jobData.email)
            
    #    try:
    #        db.updateJobOwner(jobData,userTmp,newContact)
    #    except:
    #        errMod.errOut(jobData)
            
    ## Walk through spinup directory for each basin. Determine the status of
    ## the model runs by the files available. If restarting, modify the 
    ## namelist files appropriately. Then, restart the model. Once all
    ## basins have been accounted for, fire off the monitoring program through
    ## nohup to keep track of the models. If anything goes wrong, notifications
    ## will either be emailed per the user's info, or piped to Slack for group
    ## notification.
    #for basin in range(0,len(jobData.gages)):
    #    runDir = jobData.jobDir + "/" + jobData.gages[basin] + "/RUN.SPINUP"
        
    #    if not os.path.isdir(runDir):
    #        jobData.errMsg = "ERROR: " + runDir + " not found."
    #        errMod.errOut(jobData)
            
        
        
    
if __name__ == "__main__":
    main(sys.argv[1:])